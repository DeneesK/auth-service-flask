from http import HTTPStatus

from flasgger.utils import swag_from
from flask import Blueprint, jsonify, make_response, request, url_for
from schemas.user import user_data
from services.history import HistoryService
from services.user import UserService
from sqlalchemy.exc import IntegrityError

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['POST'])
@swag_from('../docs/user_creation.yml', methods=['Post'])
def create():
    service = UserService()
    data = request.get_json()
    try:
        user = service.create(data['login'], data['password'])
    except IntegrityError as er:
        return jsonify({'message': str(er.orig)}), HTTPStatus.INTERNAL_SERVER_ERROR

    response = make_response(jsonify(user_data.dump(user)), HTTPStatus.CREATED)
    response.location = url_for('.get_user', user_id=user.id, _external=True)
    return response


@bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService().get(user_id)
    if user is None:
        return '', HTTPStatus.NOT_FOUND
    else:
        return jsonify(user_data.dump(user)), HTTPStatus.OK


@bp.route('/<user_id>', methods=['DELETE'])
@swag_from('../docs/user_remove.yml', methods=['Delete'])
def remove_user(user_id):
    service = UserService()
    result = service.delete(user_id)
    if result:
        return jsonify({'message': f'User with id {user_id} deleted'}), HTTPStatus.OK
    return (
        jsonify({'message': f'User with id {user_id} not found'}),
        HTTPStatus.NOT_FOUND,
    )


@bp.route('/<user_id>/history', methods=['GET'])
def get_history(user_id):
    service = HistoryService()
    history = service.get_history(user_id)
    if history:
        return (
            jsonify(
                {
                    'user_history': [
                        {'date': str(x.access_date), 'device': x.device}
                        for x in history
                    ]
                }
            ),
            HTTPStatus.OK,
        )
    return (
        jsonify({'message': 'User or user history not found'}),
        HTTPStatus.NOT_FOUND,
    )
