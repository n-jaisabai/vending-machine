from typing import Optional

from pydantic import BaseModel


class PendingCoinBase(BaseModel):
    id: Optional[int]
    one_coin: Optional[int]
    five_coin: Optional[int]
    ten_coin: Optional[int]
    twenty_banknote: Optional[int]
    fifty_banknote: Optional[int]
    hundred_banknote: Optional[int]
    five_hundred_banknote: Optional[int]
    thousand_banknote: Optional[int]


class PendingCoinCreate(PendingCoinBase):
    one_coin: int
    five_coin: int
    ten_coin: int
    twenty_banknote: int
    fifty_banknote: int
    hundred_banknote: int
    five_hundred_banknote: int
    thousand_banknote: int

class PendingCoinUpdate(BaseModel):
    coin_type: str
    pass


class PendingCoinResponse(PendingCoinBase):
    total: int
    
    class Config:
        orm_mode = True
