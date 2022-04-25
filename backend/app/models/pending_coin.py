from sqlalchemy import Column, Integer, String

from app.database.base_class import Base


class PendingCoin(Base):
    __tablename__ = "pending_coin"

    id = Column(Integer, primary_key=True)
    one_coin = Column(Integer, nullable=False)
    five_coin = Column(Integer, nullable=False)
    ten_coin = Column(Integer, nullable=False)
    twenty_banknote = Column(Integer, nullable=False)
    fifty_banknote = Column(Integer, nullable=False)
    hundred_banknote = Column(Integer, nullable=False)
    five_hundred_banknote = Column(Integer, nullable=False)
    thousand_banknote = Column(Integer, nullable=False)
