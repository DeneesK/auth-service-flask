from datetime import datetime
from http import HTTPStatus

import jwt
from flasgger.utils import swag_from
from flask import Blueprint, current_app, jsonify, request
from marshmallow.exceptions import ValidationError
from schemas.user import user_data
from services.history import HistoryService
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

    tokens = gen_tokens(user, current_app.config['TOKEN_SECRET_KEY'])
    current_app.extensions['redis'].set(
        'refresh:{0}'.format(tokens['refresh']),
        1,
        ex=current_app.config['TOKEN_REFRESH_TTL'],
    )

    device = request.headers.get('sec-ch-ua-platform')
    if not device:
        device = request.headers.get('User_Agent')
    history_service = HistoryService()
    history_service.store_history(user.id, device)

    return tokens, HTTPStatus.OK


@bp.route('/refresh', methods=['POST'])
def token_refresh():
    data = request.get_json()
    token = data.get('refresh')
    response = current_app.extensions['redis'].get('refresh:{0}'.format(token))

    if response:
        current_app.extensions['redis'].delete('refresh:{0}'.format(token))
        user_data = jwt.decode(
            token,
            current_app.config['TOKEN_SECRET_KEY'],
            algorithms='HS256',
        )
        user = UserService().get(user_data['id'])
        if user:
            tokens = gen_tokens(user, current_app.config['TOKEN_SECRET_KEY'])
            current_app.extensions['redis'].set(
                'refresh:{0}'.format(tokens['refresh']),
                1,
                ex=current_app.config['TOKEN_REFRESH_TTL'],
            )

            return tokens, HTTPStatus.OK

    return '', HTTPStatus.FORBIDDEN


@bp.route('/logout', methods=['POST'])
def logout():
    tokens = request.get_json()
    response = current_app.extensions['redis'].get(
        'refresh:{0}'.format(tokens['refresh'])
    )

    if response:
        current_app.extensions['redis'].delete('refresh:{0}'.format(tokens['refresh']))
        current_app.extensions['redis'].set(
            'invalidated_access:{0}'.format(tokens['access']),
            0,
            ex=current_app.config['TOKEN_ACCESS_TTL'],
        )

        return '', HTTPStatus.OK

    return '', HTTPStatus.NO_CONTENT


@bp.route('/logout-all', methods=['POST'])
def logout_all():
    tokens = request.get_json()
    user_data = jwt.decode(
        tokens['refresh'], current_app.config['TOKEN_SECRET_KEY'], algorithms='HS256'
    )
    time_now = datetime.timestamp(datetime.now())
    current_app.extensions['redis'].set(
        'logout_all: {0}'.format(user_data['id']),
        time_now,
        ex=current_app.config['TOKEN_REFRESH_TTL'],
    )
    return '', HTTPStatus.OK


@bp.route('/access-check', methods=['POST'])
def access_token_check():
    data = request.get_json()
    token = data.get('access')
    user_data = jwt.decode(
        token,
        current_app.config['TOKEN_SECRET_KEY'],
        algorithms='HS256',
    )

    time_now = int(datetime.timestamp(datetime.now()))
    token_exp = int(user_data['exp'])
    is_invalidated = current_app.extensions['redis'].get(
        'invalidated_access:{0}'.format(token)
    )
    is_logout_all = current_app.extensions['redis'].get(
        'logout_all: {0}'.format(user_data['id'])
    )

    if is_logout_all:
        logout_all_time = float(is_logout_all)
        token_iat = int(user_data['iat'])
        if logout_all_time < token_iat and time_now < token_exp and not is_invalidated:
            return '', HTTPStatus.OK

    elif time_now < token_exp and not is_invalidated:
        return '', HTTPStatus.OK

    return '', HTTPStatus.FORBIDDEN
