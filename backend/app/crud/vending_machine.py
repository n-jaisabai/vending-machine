from app.crud.base import CRUDBase
from app.models.vending_machine import VendingMachine
from app.schemas import VendingMachineCreate, VendingMachineUpdate
from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional


class CRUDVendingMachine(CRUDBase[VendingMachine, VendingMachineCreate, VendingMachineUpdate]):
    # Declare model specific CRUD operation methods.
    def first(self, db: Session) -> Optional[VendingMachine]:
        return db.query(self.model).first()

    pass


machine = CRUDVendingMachine(VendingMachine)
