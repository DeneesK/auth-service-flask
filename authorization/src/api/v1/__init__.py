from api.v1.auth import bp as auth_bp
from api.v1.users import bp as users_bp
from api.v1.role import bp as roles_bp
from flask import Blueprint
# The following imports are needed to create the matching tables.
# TODO Move to API files later.

from schemas.resource import resource_data

bp = Blueprint('v1', __name__, url_prefix='/v1')

bp.register_blueprint(auth_bp)
bp.register_blueprint(users_bp)
bp.register_blueprint(roles_bp)
