from http import HTTPStatus
from json import dumps

from flask import Blueprint, make_response, request, url_for
from services.user import UserService
from utils import object_as_dict

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['POST'])
def create():
    service = UserService()
    data = request.get_json()
    user = service.create_new(data['login'], data['password'])
    response = make_response(dumps(object_as_dict(user)), HTTPStatus.CREATED)
    response.location = url_for('.get_user', user_id=user.id, _external=True)
    return response


@bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService().get(user_id)
    if user is None:
        return '', HTTPStatus.NOT_FOUND
    else:
        return dumps(object_as_dict(user)), HTTPStatus.OK
