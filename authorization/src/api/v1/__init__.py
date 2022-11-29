from api.v1.users import bp as users_bp
from flask import Blueprint

bp = Blueprint('v1', __name__, url_prefix='/v1')

bp.register_blueprint(users_bp)
