"""An example to use roles and resources."""
from db.orm import db_engine
from flask import Flask
from models.resource import ResourceModel
from models.resource_role import ResourceRoleModel
from models.role import RoleModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://app:<password>@localhost/auth'

db_engine.init_app(app)
app.app_context().push()

role1 = RoleModel(name='role1', client_service_id='eweq')
role2 = RoleModel(name='role2', client_service_id='eweq')

db_engine.session.add(role1)
db_engine.session.add(role2)
db_engine.session.commit()  # <- don't forget it to get id-s for the roles

res = ResourceModel(name='resource1')
db_engine.session.add(res)
p1 = ResourceRoleModel(resource=res, role_id=role1.id)
p2 = ResourceRoleModel(resource=res, role_id=role2.id)
db_engine.session.add(p1)
db_engine.session.add(p2)
db_engine.session.commit()
