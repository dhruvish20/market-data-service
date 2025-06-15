from sqlalchemy import Column, String, DateTime, Float
from app.core.database import Base
from datetime import datetime

class SymbolAverage(Base):
    __tablename__ = "symbol_averages"

    symbol = Column(String, primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    moving_average = Column(Float)
    provider = Column(String)
    