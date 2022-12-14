
import click
from flask.cli import with_appcontext
from main import app
from models import RoleModel, UserRoleModel

from services.role import RoleService
from services.user import UserService
from db.orm import db_engine


@app.cli.command("create-superuser")
@with_appcontext
@click.argument("login")
def create_superuser(login):
    """The password will be promted"""
    user_service = UserService()
    password = input("Input password:")  # TODO Hide letters
    user = user_service.create(login, password)
    # TODO make a transaction. How to get user.id within one transaction?
    model = RoleModel()
    db_admin_role = model.query.filter_by(name='admin').first()
    print("admin role", db_admin_role)
    assert db_admin_role
    user_role = UserRoleModel(user_id=user.id, role_id=db_admin_role.id)
    db_engine.session.add(user_role)
    db_engine.session.commit()


def create_role(role_name, client_id):
    service = RoleService()
    role = service.create(role_name, client_id)
    return role


app.cli.add_command(create_superuser)
