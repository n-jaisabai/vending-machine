from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api.deps import get_db

router = APIRouter()


@router.get("", response_model=schemas.VendingMachineResponse)
def read_machine(db: Session = Depends(get_db)) -> Any:
    """
    Retrieve machine.
    """
    machine = crud.machine.first(db)
    if not machine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The machine does not exist in the system.",
        )

    return machine


@router.post("", response_model=schemas.VendingMachineResponse)
def create_machine(*, db: Session = Depends(get_db), machine_in: schemas.VendingMachineCreate) -> Any:
    """
    Create new machines.
    """
    machine = crud.machine.first(db)
    if machine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The machine does exist in the system.",
        )
    machine = crud.machine.create(db, obj_in=machine_in)
    return machine


@router.put("", response_model=schemas.VendingMachineResponse)
def update_machine(*, db: Session = Depends(get_db), machine_in: schemas.VendingMachineUpdate) -> Any:
    """
    Update existing machines.
    """
    machine = crud.machine.first(db)
    if not machine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The machine does not exist in the system.",
        )
    machine = crud.machine.update(db, db_obj=machine, obj_in=machine_in)
    return machine


@router.delete("", response_model=schemas.Message)
def delete_machine(*, db: Session = Depends(get_db)) -> Any:
    """
    Delete existing machine.
    """
    machine = crud.machine.first(db)
    if not machine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The machine does not exist in the system.",
        )
    crud.machine.remove(db, model_id=machine.id)
    return {"message": f"Machine deleted."}
