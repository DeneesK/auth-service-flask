from uuid import uuid4

from db.orm import db_engine
from models.history import HistoryModel


class HistoryService:
    def store_history(self, user_id: uuid4, device: str) -> bool:
        record = self._create_record(user_id, device)
        db_engine.session.add(record)
        db_engine.session.commit()

    def _create_record(self, user_id: uuid4, device: str) -> HistoryModel:
        access_record = HistoryModel(
            user_id=user_id,
            device=device,
        )
        return access_record

    def get_history(self, user_id: uuid4) -> list:
        history = HistoryModel.query.filter_by(user_id=user_id).all()
        return history
