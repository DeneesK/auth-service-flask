from http import HTTPStatus

from flask import Blueprint, jsonify, make_response, request, url_for
from flasgger.utils import swag_from
from schemas.user import user_data
from services.user import UserService

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['POST'])
@swag_from('docs/user_creation.yml', methods=['Post'])
def create():
    service = UserService()
    data = request.get_json()
    user = service.create_new(data['login'], data['password'])
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
