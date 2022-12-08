from db.orm import db_engine
from models.role import RoleModel


class RoleService:
    def create(self, role_name, client_service_id):
        new_role = RoleModel(name=role_name,
                             client_service_id=client_service_id)
        db_engine.session.add(new_role)
        db_engine.session.commit()
        return new_role

    def get(self, user_id) -> RoleModel:
        return RoleModel.query.get(user_id)
