from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    id: Optional[int]
    name: Optional[str]
    price: Optional[float]
    stock: Optional[int]


class ProductCreate(ProductBase):
    name: str
    price: float
    stock: int

class ProductUpdate(ProductBase):
    id: int
    pass


class ProductResponse(ProductBase):
    class Config:
        orm_mode = True
