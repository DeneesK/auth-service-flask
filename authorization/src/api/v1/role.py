from http import HTTPStatus
from flask import Blueprint, jsonify, make_response, request, url_for

from schemas.role import role_data
from services.role import RoleService


bp = Blueprint('role', __name__, url_prefix='/role')


@bp.route('/create', methods=['POST'])
def create():
    role_service = RoleService()
    print('001')
    try:
        print('hasattr', hasattr(request, 'get_json'))
        print('get_data', request.get_data())
        data = request.get_json()
        role_name = data['role_name']
        client_service_id = data['client_service_id']
        role_obj = role_service.create(role_name=role_name, client_service_id=client_service_id)
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

    response = make_response(jsonify(role_data.dump(role_obj)), HTTPStatus.CREATED)
    response.location = url_for('.get_role', role_id=role_obj.id, _external=True)
    return response


@bp.route('/<role_id>', methods=['GET'])
def get_role(role_id):
    role = RoleService().get(role_id)
    if role is None:
        return '', HTTPStatus.NOT_FOUND
    else:
        return jsonify(role_data.dump(role)), HTTPStatus.OK
