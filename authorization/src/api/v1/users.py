from http import HTTPStatus

from flasgger.utils import swag_from
from flask import Blueprint, make_response, request, url_for
from schemas.history import history_schema
from schemas.user import user_data
from services.history import HistoryService
from services.user import UserService
from sqlalchemy.exc import IntegrityError

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['GET'])
def get_users():
    service = UserService()
    users = service.all()
    return user_data.dump(users, many=True), HTTPStatus.OK


@bp.route('', methods=['POST'])
@swag_from('../docs/user_creation.yml', methods=['Post'])
def create():
    service = UserService()
    data = request.get_json()
    try:
        user = service.create(data['login'], data['password'])
    except IntegrityError as er:
        return {'message': str(er.orig)}, HTTPStatus.INTERNAL_SERVER_ERROR

    response = make_response(user_data.dump(user), HTTPStatus.CREATED)
    response.location = url_for('.get_user', user_id=user.id, _external=True)
    return response


@bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService().get(user_id)
    if user is None:
        return '', HTTPStatus.NOT_FOUND
    else:
        return user_data.dump(user), HTTPStatus.OK


@bp.route('/<user_id>', methods=['DELETE'])
@swag_from('../docs/user_remove.yml', methods=['Delete'])
def remove_user(user_id):
    service = UserService()
    result = service.delete(user_id)
    if result:
        return {'message': f'User with id {user_id} deleted'}, HTTPStatus.OK
    return {'message': f'User with id {user_id} not found'}, HTTPStatus.NOT_FOUND


@bp.route('/<user_id>/history', methods=['GET'])
def get_history(user_id):
    service = HistoryService()
    history = service.get_history(user_id)
    if history:
        user_history = history_schema.dump({'user_history': history})
        return user_history, HTTPStatus.OK
    return {'message': 'User or user history not found'}, HTTPStatus.NOT_FOUND


@bp.route('/<user_id>/сhange-password', methods=['POST'])
def change_password(user_id):
    data = request.get_json()
    old_password = data['old_password']
    service = UserService()
    user_login = service.get(user_id).login
    user = service.get_by_credentials(user_login, old_password)
    if user:
        new_password = data['new_password']
        service.change_password(user, new_password)
        return '', HTTPStatus.OK
    return '', HTTPStatus.FORBIDDEN
