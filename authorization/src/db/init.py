import logging
from flask import Flask

from models import RoleModel
from services.role import RoleService
from .orm import db_engine

logger = logging.getLogger()


def init_db(app: Flask):
    db_engine.init_app(app)
    app.app_context().push()

    db_engine.create_all()
    create_init_roles()
    db_engine.session.commit()


def create_init_roles():
    model = RoleModel()
    db_admin_role = model.query.filter_by(name='admin').first()
    if not db_admin_role:
        role_service = RoleService()
        role_service.create('admin', '00000000-0000-0000-0000-000000000000')
        logger.info("The initial 'admin' role created")
        db_engine.session.commit()
