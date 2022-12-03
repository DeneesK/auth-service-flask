from http import HTTPStatus

from db.redis import redis_connection
from flask import Blueprint, jsonify, request
from flasgger.utils import swag_from
from marshmallow.exceptions import ValidationError
from schemas.user import user_data
from services.user import UserService
from utils.tokens import gen_tokens

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

    return tokens, 200
