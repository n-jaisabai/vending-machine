from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from h11 import SWITCHED_PROTOCOL
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api.deps import get_db

router = APIRouter()


@router.get("", response_model=schemas.PendingCoinResponse)
def read_coin(db: Session = Depends(get_db)) -> Any:
    """
    Retrieve coin.
    """
    coin = crud.coin.first(db)
    if not coin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The coin does not exist in the system.",
        )
    
    coin.total = total(coin.one_coin, coin.five_coin, coin.ten_coin, coin.twenty_banknote, coin.fifty_banknote, coin.hundred_banknote, coin.five_hundred_banknote, coin.thousand_banknote)
    return coin


@router.post("", response_model=schemas.PendingCoinResponse)
def create_coin(*, db: Session = Depends(get_db), coin_in: schemas.PendingCoinCreate) -> Any:
    """
    Create new coins.
    """
    coin = crud.coin.first(db)
    if coin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The coin does exist in the system.",
        )
    coin = crud.coin.create(db, obj_in=coin_in)
    return coin


@router.post("/reset", response_model=schemas.PendingCoinResponse)
def reset_coin(*, db: Session = Depends(get_db)) -> Any:
    """
    Reset coins.
    """
    coin = crud.coin.first(db)
    if not coin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The coin does not exist in the system.",
        )
    
    coin_update = {
        "id": coin.id,
        "one_coin": 0,
        "five_coin": 0,
        "ten_coin": 0,
        "twenty_banknote": 0,
        "fifty_banknote": 0,
        "hundred_banknote": 0,
        "five_hundred_banknote": 0,
        "thousand_banknote": 0
    }

    coin = crud.coin.update(db, db_obj=coin, obj_in=coin_update)
    coin.total = 0
    return coin


@router.put("", response_model=schemas.PendingCoinResponse)
def update_coin(*, db: Session = Depends(get_db), coin_in: schemas.PendingCoinUpdate) -> Any:
    """
    Update existing coins.
    """
    coin = crud.coin.first(db)
    if not coin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The coin does not exist in the system.",
        )
    
    coin_update = { "id": coin.id }
    if coin_in.coin_type == "one_coin":
        coin_update["one_coin"] = coin.one_coin + 1
    elif coin_in.coin_type == "five_coin":
        coin_update["five_coin"] = coin.five_coin + 1
    elif coin_in.coin_type == "ten_coin":
        coin_update["ten_coin"] = coin.ten_coin + 1
    elif coin_in.coin_type == "twenty_banknote":
        coin_update["twenty_banknote"] = coin.twenty_banknote + 1
    elif coin_in.coin_type == "fifty_banknote":
        coin_update["fifty_banknote"] = coin.fifty_banknote + 1
    elif coin_in.coin_type == "hundred_banknote":
        coin_update["hundred_banknote"] = coin.hundred_banknote + 1
    elif coin_in.coin_type == "five_hundred_banknote":
        coin_update["five_hundred_banknote"] = coin.five_hundred_banknote + 1
    elif coin_in.coin_type == "thousand_banknote":
        coin_update["thousand_banknote"] = coin.thousand_banknote + 1
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The coin type does not exist in the system.",
        )

    coin = crud.coin.update(db, db_obj=coin, obj_in=coin_update)
    coin.total = total(coin.one_coin, coin.five_coin, coin.ten_coin, coin.twenty_banknote, coin.fifty_banknote, coin.hundred_banknote, coin.five_hundred_banknote, coin.thousand_banknote)
    return coin


@router.delete("", response_model=schemas.Message)
def delete_coin(*, db: Session = Depends(get_db)) -> Any:
    """
    Delete existing coin.
    """
    coin = crud.coin.first(db)
    if not coin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The coin does not exist in the system.",
        )
    crud.coin.remove(db, model_id=coin.id)
    return {"message": f"Coin deleted."}

def total(
    one_coin: int, 
    five_coin: int, 
    ten_coin: int, 
    twenty_banknote: int, 
    fifty_banknote: int, 
    hundred_banknote: int, 
    five_hundred_banknote: int, 
    thousand_banknote: int) -> int:
    return one_coin*1 + five_coin*5 + ten_coin*10 + twenty_banknote*20 + fifty_banknote*50 + hundred_banknote*100 + five_hundred_banknote*500 + thousand_banknote*1000
