from app.crud.base import CRUDBase
from app.models.pending_coin import PendingCoin
from app.schemas import PendingCoinCreate, PendingCoinUpdate
from sqlalchemy.orm import Session
from typing import Optional


class CRUDPendingCoin(CRUDBase[PendingCoin, PendingCoinCreate, PendingCoinUpdate]):
    # Declare model specific CRUD operation methods.
    def first(self, db: Session) -> Optional[PendingCoin]:
        return db.query(self.model).first()

    pass


coin = CRUDPendingCoin(PendingCoin)
