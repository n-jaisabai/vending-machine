from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api.deps import get_db

router = APIRouter()


@router.post("", response_model=schemas.TransactionResponse)
def create_transaction(*, db: Session = Depends(get_db), transaction_in: schemas.TransactionCreate) -> Any:
    """
    Create new transaction.
    """
    product = crud.product.get(db, model_id=transaction_in.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The product does not exist in the system.",
        )
    
    if product.stock > 0:
        coin = crud.coin.first(db)
        if not coin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The coin does not exist in the system.",
            )
        coin.total = total(coin.one_coin, coin.five_coin, coin.ten_coin, coin.twenty_banknote, coin.fifty_banknote, coin.hundred_banknote, coin.five_hundred_banknote, coin.thousand_banknote)

        if coin.total >= product.price:
            machine = crud.machine.first(db)
            if not machine:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The machine does not exist in the system.",
                )
            
            change: float = coin.total - product.price
            change_dict = has_change(change, {
                "one_coin": coin.one_coin + machine.one_coin,
                "five_coin": coin.five_coin + machine.five_coin,
                "ten_coin": coin.ten_coin + machine.ten_coin,
                "twenty_banknote": coin.twenty_banknote + machine.twenty_banknote,
                "fifty_banknote": coin.fifty_banknote + machine.fifty_banknote,
                "hundred_banknote": coin.hundred_banknote + machine.hundred_banknote,
                "five_hundred_banknote": coin.five_hundred_banknote + machine.five_hundred_banknote,
                "thousand_banknote": coin.thousand_banknote + machine.thousand_banknote
            })
            if change_dict:
                # update product stock
                product_update = {
                    "id": product.id,
                    "stock": product.stock - 1
                }
                product = crud.product.update(db, db_obj=product, obj_in=product_update)

                # update machine coin
                machine_update = {
                    "id": machine.id,
                    "one_coin": coin.one_coin + machine.one_coin - change_dict["one_coin"],
                    "five_coin": coin.five_coin + machine.five_coin - change_dict["five_coin"],
                    "ten_coin": coin.ten_coin + machine.ten_coin - change_dict["ten_coin"],
                    "twenty_banknote": coin.twenty_banknote + machine.twenty_banknote - change_dict["twenty_banknote"],
                    "fifty_banknote": coin.fifty_banknote + machine.fifty_banknote - change_dict["fifty_banknote"],
                    "hundred_banknote": coin.hundred_banknote + machine.hundred_banknote - change_dict["hundred_banknote"],
                    "five_hundred_banknote": coin.five_hundred_banknote + machine.five_hundred_banknote - change_dict["five_hundred_banknote"],
                    "thousand_banknote": coin.thousand_banknote + machine.thousand_banknote - change_dict["thousand_banknote"]
                }
                machine = crud.machine.update(db, db_obj=machine, obj_in=machine_update)

                # reset coin to 0 after transaction
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

                return {
                    "product_id": product.id,
                    "product_name": product.name,
                    "change": change_dict
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The machine does not has enough coin for change.",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The coin does not has enough for this product.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The product stock is empty.",
        )


@router.post("/cancel", response_model=schemas.TransactionResponse)
def cancel(*, db: Session = Depends(get_db)) -> Any:
    """
    Cancel transaction.
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

def has_change(change: float, coin: schemas.TransactionChange) -> Any:
    change_dict: schemas.TransactionChange = {
        "one_coin": 0,
        "five_coin": 0,
        "ten_coin": 0,
        "twenty_banknote": 0,
        "fifty_banknote": 0,
        "hundred_banknote": 0,
        "five_hundred_banknote": 0,
        "thousand_banknote": 0
    }

    while change > 0:
        if change >= 1000 and coin["thousand_banknote"] > 0:
            change_dict["thousand_banknote"] += 1
            coin["thousand_banknote"] -= 1
            change -= 1000
        elif change >= 500 and coin["five_hundred_banknote"] > 0:
            change_dict["five_hundred_banknote"] += 1
            coin["five_hundred_banknote"] -= 1
            change -= 500
        elif change >= 100 and coin["hundred_banknote"] > 0:
            change_dict["hundred_banknote"] += 1
            coin["hundred_banknote"] -= 1
            change -= 100
        elif change >= 50 and coin["fifty_banknote"] > 0:
            change_dict["fifty_banknote"] += 1
            coin["fifty_banknote"] -= 1
            change -= 50
        elif change >= 20 and coin["twenty_banknote"] > 0:
            change_dict["twenty_banknote"] += 1
            coin["twenty_banknote"] -= 1
            change -= 20
        elif change >= 10 and coin["ten_coin"] > 0:
            change_dict["ten_coin"] += 1
            coin["ten_coin"] -= 1
            change -= 10
        elif change >= 5 and coin["five_coin"] > 0:
            change_dict["five_coin"] += 1
            coin["five_coin"] -= 1
            change -= 5
        elif change >= 1 and coin["one_coin"] > 0:
            change_dict["one_coin"] += 1
            coin["one_coin"] -= 1
            change -= 1
        else:
            return False
    
    change_dict["total"] = total(change_dict["one_coin"], change_dict["five_coin"], change_dict["ten_coin"], change_dict["twenty_banknote"], change_dict["fifty_banknote"], change_dict["hundred_banknote"], change_dict["five_hundred_banknote"], change_dict["thousand_banknote"])
    
    return change_dict