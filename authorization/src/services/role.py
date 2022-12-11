from db.orm import db_engine
from models.role import RoleModel


class RoleService:
    def create(self, role_name, client_id):
        new_role = RoleModel(name=role_name,
                             client_service_id=client_id)
        db_engine.session.add(new_role)
        db_engine.session.commit()
        return new_role

    def get(self, role_id) -> RoleModel:
        return RoleModel.query.get(role_id)

    def delete(self, role_id):
        role = RoleModel.query.get(role_id)
        if role:
            db_engine.session.delete(role)
            db_engine.session.commit()
            return True
        else:
            return False
