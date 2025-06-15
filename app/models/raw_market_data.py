import uuid
from sqlalchemy import Column , String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from datetime import datetime


class RawMarketData(Base):
    __tablename__ = "raw_market_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    raw_json = Column(JSON)
