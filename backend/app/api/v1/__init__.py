from fastapi import APIRouter

from app.api.v1 import products
from app.api.v1 import vending_machine
from app.api.v1 import pending_coin

api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(vending_machine.router, prefix="/machine", tags=["machine"])
api_router.include_router(pending_coin.router, prefix="/coin", tags=["coin"])
