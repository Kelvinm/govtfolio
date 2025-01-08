from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, DECIMAL, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from src.database import Base

class TradeType(PyEnum):
    BUY = "BUY"
    SELL = "SELL"
    EXCHANGE = "EXCHANGE"
    RECEIVE = "RECEIVE"

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    legislator_id = Column(Integer, ForeignKey("legislators.id"))
    security_ticker = Column(String(20), nullable=True)
    trade_date = Column(Date, nullable=True)
    disclosure_date = Column(Date, nullable=True)
    trade_type = Column(Enum(TradeType), nullable=False)
    amount_range = Column(String(50))
    volume = Column(Integer)
    price_per_share = Column(DECIMAL(10, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    legislator = relationship("Legislator", back_populates="trades")