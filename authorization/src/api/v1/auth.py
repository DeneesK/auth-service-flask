from http import HTTPStatus

import jwt
from db.redis import redis_connection
from flask import Blueprint, jsonify, request
from flasgger.utils import swag_from
from marshmallow.exceptions import ValidationError
from schemas.user import user_data
from services.user import UserService
from models.user import UserModel
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

    return '', HTTPStatus.FORBIDDEN