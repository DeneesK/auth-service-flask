from http import HTTPStatus

from flask import Blueprint, jsonify, make_response, request, url_for
from schemas.user import user_data
from services.user import UserService

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['POST'])
def create():
    """
        Create new user
        ---
        tags:
          - user
        parameters:
          - in: body
            name: body
            schema:
              id: UserService
              required:
                - login
                - password
              properties:
                login:
                  type: string
                  description: The user's username.
                  default: "JohnDoe"
                password:
                  type: string
                  description: The user's password.
                  default: "Qwerty123"
        responses:
          201:
            description: Message that user was created
            schema:
              properties:
                id:
                  type: string
                  description: id of created user
                  default: null
                login:
                  type: string
                  description: login
                  default: null
          400:
            description: Bad request response
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: False
                data:
                  type: array
                  description: Response data
                  items:
                    type: object
                    default: ...
                  default: []
                errors:
                  type: array
                  description: Data with error validation messages
                  items:
                    type: object
                    default: ...
                  default: []
                message:
                  type: string
                  description: Response message
    """
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
