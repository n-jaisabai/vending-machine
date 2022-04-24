from typing import Optional

from pydantic import BaseModel


class VendingMachineBase(BaseModel):
    id: Optional[int]
    name: Optional[str]
    one_coin: Optional[int]
    five_coin: Optional[int]
    ten_coin: Optional[int]
    twenty_banknote: Optional[int]
    fifty_banknote: Optional[int]
    hundred_banknote: Optional[int]
    five_hundred_banknote: Optional[int]
    thousand_banknote: Optional[int]


class VendingMachineCreate(VendingMachineBase):
    name: str
    one_coin: int
    five_coin: int
    ten_coin: int
    twenty_banknote: int
    fifty_banknote: int
    hundred_banknote: int
    five_hundred_banknote: int
    thousand_banknote: int

class VendingMachineUpdate(VendingMachineBase):
    id: int
    pass


class VendingMachineResponse(VendingMachineBase):
    class Config:
        orm_mode = True
