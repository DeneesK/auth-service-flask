from flask import Blueprint, request
from services.user import UserService


bp_user = Blueprint('user', __name__, url_prefix="/user")


@bp_user.route('/create', methods=['POST'])  # TODO Use POST method here
# TODO Log shows the password!
def create():
    msg = 'Create user from blueprint \n{0} \nresult:{1}'
    args = '\n'.join(f'{k}:{v}' for k, v in request.args.items())
    service = UserService()
    result, result_ex = service.create_new(request.args['login'], request.args['password'])
    msg1 = msg.format(args, (result, result_ex))
    return msg1
