from flask import Blueprint

bp_user = Blueprint('user', __name__, url_prefix="/user")


@bp_user.route('/create')  # TODO Use POST method here
def create():
    return 'Create user from blueprint'
