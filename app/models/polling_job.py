from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import JSON
from app.core.database import Base
from datetime import datetime
import uuid

class PollingJob(Base):
    __tablename__ = "polling_jobs"

    job_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbols = Column(JSON)  # stores list of symbols
    interval = Column(Integer)
    provider = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
