from db.orm import db_engine
from models.history import HistoryModel, UserHistory


class UserHistoryService:
    def add_record_user_history(self, user_id, device):
        access_record = self._create_record(device)
        new_record = UserHistory(user_id=user_id, access_history_id=access_record.id)
        db_engine.session.add(new_record)
        db_engine.session.commit()
        return True

    def _create_record_access_history(self, device):
        access_record = HistoryModel(device=device)
        db_engine.session.add(access_record)
        db_engine.session.commit()
        return access_record
