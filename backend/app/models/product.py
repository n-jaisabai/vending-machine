from platform import machine
from sqlalchemy import Column, Integer, String, Float

from app.database.base_class import Base


class Product(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
