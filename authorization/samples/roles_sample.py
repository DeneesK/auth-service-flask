"""An example to use roles and resources."""
from db.orm import db_engine
import datetime
from flask import Flask


from models import UserRoleModel
from services.user import UserService

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://app:<password>@localhost/auth'

db_engine.init_app(app)
app.app_context().push()
from models.role import RoleModel
from models.resource import ResourceModel
from models.resource_role import ResourceRoleModel
# from schemas.resource import ResourceData  # <- to execute 'permission' set

random_mark = str(datetime.datetime.now())

client_service_id = 'ddfsd'+ random_mark
role1 = RoleModel(name='role1'+random_mark, client_service_id=client_service_id)
role2 = RoleModel(name='role2'+random_mark, client_service_id=client_service_id)

db_engine.session.add(role1)
db_engine.session.add(role2)
db_engine.session.commit()  # <- don't forget it to get id-s for the roles

res = ResourceModel(name='resource1')
db_engine.session.add(res)
p1 = ResourceRoleModel(resource=res, role_id=role1.id, action='VIEW')
p2 = ResourceRoleModel(resource=res, role_id=role2.id, action='DELETE')
db_engine.session.add(p1)
db_engine.session.add(p2)
db_engine.session.commit()


user = UserService().create('Ivan' + random_mark, '123')
ur1 = UserRoleModel(user_id=user.id, role_id=role1.id)
ur2 = UserRoleModel(user_id=user.id, role_id=role2.id)
db_engine.session.add(ur1)
db_engine.session.add(ur2)
db_engine.session.commit()
print(user.roles)
print(role1.user_role)
print(role2.user_role)

# region check user rights
roles_to_resource_and_action = ResourceRoleModel.query.filter_by(resource_id=res.id,
                                                                 action='VIEW')
# ^ Here are roles for resource and action
permission_record = UserRoleModel.query.filter_by(user_id=user.id)
# ^ Here are roles for the user
resource_roles_set = set(res_role.role_id for res_role in roles_to_resource_and_action)
user_role_set = set(user_role.role_id for user_role in permission_record)
print(resource_roles_set & user_role_set)
# endregion