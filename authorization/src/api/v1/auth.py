from datetime import datetime
from http import HTTPStatus

import jwt
from db.redis import redis_connection
from flask import Blueprint, jsonify, request
from flasgger.utils import swag_from
from marshmallow.exceptions import ValidationError
from schemas.user import user_data
from services.user import UserService
from utils.tokens import gen_tokens, SECRET_KEY

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['POST'])
@swag_from('../docs/auth_login.yml', methods=['Post'])
def login():
    data = request.get_json()
    try:
        login_data = user_data.load(data)
    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.BAD_REQUEST

    user = UserService().get_by_credentials(**login_data)
    if user is None:
        return '', HTTPStatus.FORBIDDEN

    tokens = gen_tokens(user)
    redis_connection.set('refresh:{0}'.format(tokens['refresh']), 1, ex=604800)

    return tokens, HTTPStatus.OK


@bp.route('/refresh', methods=['POST'])
def token_refresh():
    data = request.get_json()
    token = data.get('refresh')
    response = redis_connection.get('refresh:{0}'.format(token))
    
    if response:
        redis_connection.delete('refresh:{0}'.format(token))
        user_data = jwt.decode(
        token,
        SECRET_KEY,
        algorithms='HS256',
    )
        user = UserService().get(user_data['id'])
        if user:
            tokens = gen_tokens(user)
            redis_connection.set('refresh:{0}'.format(tokens['refresh']), 1, ex=604800)

            return tokens, HTTPStatus.OK

    return '', HTTPStatus.FORBIDDEN


@bp.route('/logout', methods=['POST'])
def logout():
    tokens = request.get_json()
    response = redis_connection.get('refresh:{0}'.format(tokens['refresh']))
    
    if response:
        redis_connection.delete('refresh:{0}'.format(tokens['refresh']))
        redis_connection.set('invalidated_access:{0}'.format(tokens['access']), 0, ex=600)
        return '', HTTPStatus.OK
    
    return '', HTTPStatus.NO_CONTENT


@bp.route('/logout_all', methods=['POST'])
def logout_all():
    tokens = request.get_json()
    user_data = jwt.decode(tokens['refresh'],
    SECRET_KEY,
    algorithms='HS256',)
    time_now = datetime.timestamp(datetime.now())
    redis_connection.set('logout_all: {0}'.format(user_data['id']), time_now, ex=604800)
    return '', HTTPStatus.OK
