from typing import Optional

from pydantic import BaseModel


class TransactionChange(BaseModel):
    one_coin: Optional[int]
    five_coin: Optional[int]
    ten_coin: Optional[int]
    twenty_banknote: Optional[int]
    fifty_banknote: Optional[int]
    hundred_banknote: Optional[int]
    five_hundred_banknote: Optional[int]
    thousand_banknote: Optional[int]
    total: Optional[float]

class TransactionBase(BaseModel):
    product_id: Optional[int]
    product_name: Optional[str]
    change: Optional[TransactionChange]


class TransactionCreate(BaseModel):
    product_id: int


class TransactionResponse(TransactionBase):
    class Config:
        orm_mode = True
