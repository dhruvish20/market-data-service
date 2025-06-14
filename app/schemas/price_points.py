from pydantic import BaseModel
from datetime import datetime

class PricePointResponse(BaseModel):
    symbol: str
    price: float
    timestamp: datetime

    class Config:
        orm_mode = True