from uuid import uuid4
from datetime import datetime
from app.services.kafka_producer import produce_price_event

produce_price_event({
    "symbol": "AAPL",
    "price": 195.98,
    "timestamp": datetime.utcnow().isoformat(),
    "source": "yfinance",
    "raw_response_id": str(uuid4())
})
