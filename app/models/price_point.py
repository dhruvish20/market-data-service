from sqlalchemy import Column, Integer, String, Float, DateTime, Index, func
from app.core.database import Base



class PricePoint(Base):
    __tablename__ = "price_points"  

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    timestamp = Column(DateTime, default=func.now())
    provider = Column(String)

    __table_args__ = (
        Index("ix_symbol_timestamp", "symbol", "timestamp"),
    )