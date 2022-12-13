from db.orm import db_engine
from models import ResourceRoleModel, UserModel, UserRoleModel
from models.role import RoleModel
from services.exceptions import ObjectNotFoundException


class RoleService:
    def create(self, role_name, client_id):
        new_role = RoleModel(name=role_name, client_service_id=client_id)
        db_engine.session.add(new_role)
        db_engine.session.commit()
        return new_role

    def update(self, **kwargs):
        db_engine.session.query(RoleModel).filter(RoleModel.id == kwargs['id']).update(
            values=kwargs
        )
        db_engine.session.commit()

    def get(self, role_id) -> RoleModel:
        obj = RoleModel.query.get(role_id)
        if not obj:
            raise ObjectNotFoundException('Role', role_id)
        return obj

    def all(self) -> list[UserModel]:
        return RoleModel.query.all()

    def delete(self, role_id):
        role = RoleModel.query.get(role_id)
        if role:
            db_engine.session.delete(role)
            db_engine.session.commit()
            return True
        else:
            return False

    def check_user_rights(self, user_id, resource_id, action) -> bool:
        # TODO Rewrite with one query with JOIN.
        roles_to_resource_and_action = ResourceRoleModel.query.filter_by(
            resource_id=resource_id, action=action
        )
        # ^ Here are roles for resource and action
        permission_record = UserRoleModel.query.filter_by(user_id=user_id)
        # ^ Here are roles for the user
        resource_roles_set = set(
            res_role.role_id for res_role in roles_to_resource_and_action
        )
        user_role_set = set(user_role.role_id for user_role in permission_record)
        return bool(resource_roles_set & user_role_set)
