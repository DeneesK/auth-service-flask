from db.orm import db_engine
from models.history import HistoryModel
from sqlalchemy.dialects.postgresql import UUID


class HistoryService:
    def store_history(self, user_id: UUID, device: str) -> bool:
        record = self._create_record(user_id, device)
        db_engine.session.add(record)
        db_engine.session.commit()

    def _create_record(self, user_id: UUID, device: str) -> HistoryModel:
        access_record = HistoryModel(
            user_id=user_id,
            device=device,
        )
        return access_record

    def get_history(self, user_id: UUID) -> list[HistoryModel]:
        history = HistoryModel.query.filter_by(user_id=user_id).limit(10)
        return history
