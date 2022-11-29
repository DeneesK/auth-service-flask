from flask import Blueprint, request
from services.user import UserService

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/create', methods=['POST'])  # TODO Use POST method here
# TODO Log shows the password!
def create():
    msg = 'Create user from blueprint \n{0} \nresult:{1}'
    # args = '\n'.join(f'{k}:{v}' for k, v in request.args.items())
    service = UserService()
    data = request.get_json()
    result, result_ex = service.create_new(data['login'], data['password'])
    msg1 = msg.format(result, result_ex)
    return msg1, 201
