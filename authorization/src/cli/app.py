from getpass import getpass
from uuid import uuid4

import click
from flask.cli import with_appcontext
from main import app
from models import RoleModel, UserRoleModel

from services.user import UserService
from db.orm import db_engine


@app.cli.command("create-superuser")
@with_appcontext
@click.argument("login")
def create_superuser(login):
    """The password will be promted"""
    user_service = UserService()
    password = getpass("Input password:")

    with db_engine.session.begin():
        user = user_service.create(login, password, commit=False)
        user.id = uuid4()
        model = RoleModel()
        db_admin_role = model.query.filter_by(name='admin').first()
        assert db_admin_role
        user_role = UserRoleModel(user_id=user.id, role_id=db_admin_role.id)
        db_engine.session.add(user_role)


app.cli.add_command(create_superuser)
