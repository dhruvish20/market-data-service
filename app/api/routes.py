from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.price_point import PricePoint
from app.api.deps import get_db
from app.schemas.price_points import PricePointResponse
from app.schemas.polling_job import PollingJobRequest, PollingJobResponse
from app.models.polling_job import PollingJob
from uuid import uuid4

router = APIRouter()

@router.get("/latest")
async def get_prices(symbol: str, provider: str = None, db: Session = Depends(get_db)):
    query = db.query(PricePoint).filter(PricePoint.symbol == symbol)
    if provider:
        query = query.filter(PricePoint.provider == provider)
    
    result = query.order_by(PricePoint.timestamp.desc()).first()
    if result:
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

    return {
        "job_id": job_id,
        "status": "accepted",
        "config": payload
    }


@router.get("/test-db")
async def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Run a lightweight query
        db.execute(text("SELECT 1"))
        return {"status": "connected"}
    except Exception as e:
        return {"status": "error", "details": str(e)}
