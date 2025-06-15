from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.price_point import PricePoint
from app.api.deps import get_db
from app.schemas.price_points import PricePointResponse
from app.schemas.polling_job import PollingJobRequest, PollingJobResponse
from app.models.polling_job import PollingJob
from uuid import uuid4
from app.services.providers.yfinance_provider import YFinanceProvider
from app.models.raw_market_data import RawMarketData
from app.services.kafka_producer import produce_price_event
import json
from datetime import datetime

def default_converter(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

router = APIRouter()

@router.get("/latest")
async def get_prices(symbol: str, provider: str = None, db: Session = Depends(get_db)):
    query = db.query(PricePoint).filter(PricePoint.symbol == symbol)
    if provider:
        query = query.filter(PricePoint.provider == provider)
    
    result = query.order_by(PricePoint.timestamp.desc()).first()
    if not result:
        raise HTTPException(status_code=404, detail="Price point not found")
    
    return result 

@router.post("/poll", response_model=PollingJobResponse)
async def create_polling_job(
    payload: PollingJobRequest,
    db: Session = Depends(get_db)
):
    job_id = uuid4()

    job = PollingJob(
        job_id=job_id,
        symbols=payload.symbols,
        interval=payload.interval,
        provider=payload.provider
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    provider_service = YFinanceProvider()
    for symbol in payload.symbols:
        try:
            price_data = provider_service.get_price(symbol)

            raw_entry = RawMarketData(
                id = uuid4(),
                symbol=price_data['symbol'],
                provider = price_data['provider'],
                timestamp = price_data['timestamp'],
                raw_json=json.loads(json.dumps(price_data, default=default_converter))
                
            )

            db.add(raw_entry)
            db.commit()
            db.refresh(raw_entry)


            produce_price_event({
                "symbol": price_data['symbol'],
                "price": price_data['price'],
                "timestamp": price_data['timestamp'].isoformat(),
                "source": price_data['provider'],
                "raw_response_id": str(raw_entry.id)
            })

            print(f"Produced price event for {price_data['symbol']} at {price_data['timestamp']}") 

        except Exception as e:
            print(f"Error processing symbol {symbol}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    return {
        "job_id": job.job_id,
        "status": "accepted",
        "config": payload
    }


@router.get("/test-db")
async def test_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "connected"}
    except Exception as e:
        return {"status": "error", "details": str(e)}

