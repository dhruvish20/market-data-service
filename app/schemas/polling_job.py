from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

class PollingJobRequest(BaseModel):
    symbols: List[str]
    interval: int
    provider: Optional[str] = None

class PollingJobResponse(BaseModel):
    job_id: UUID
    status: str = "accepted"
    config: PollingJobRequest

    class Config:
        orm_mode = True
