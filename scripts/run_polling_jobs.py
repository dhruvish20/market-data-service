import time
from datetime import datetime, timedelta
from app.models.raw_market_data import RawMarketData
from app.core.database import SessionLocal
from app.models.polling_job import PollingJob
from app.services.providers.yfinance_provider import YFinanceProvider
from app.services.kafka_producer import produce_price_event
import uuid
import json

last_run_map = {}

def should_run(job_id, interval):
    now = datetime.utcnow()
    last_run = last_run_map.get(job_id)
    if last_run is None or (now - last_run) >= timedelta(seconds = interval):
        last_run_map[job_id] = now
        return True
    return False

def run():
    db = SessionLocal()
    provider = YFinanceProvider()
    try:
        while True:
            print("Checking for polling jobs")

            jobs = db.query(PollingJob).all()

            for job in jobs:
                if should_run(job.job_id, job.interval):
                    print(f"Running job {job.job_id} for symbols {job.symbols} with provider {job.provider}")

                    for symbol in job.symbols:
                        try:
                            price_data = provider.get_price(symbol)
                            print(f"Fetched data for {symbol}: {price_data}")

                            raw_json_str = json.dumps(price_data, default = str)

                            raw_record = RawMarketData(
                                id = str(uuid.uuid4()),
                                symbol = price_data['symbol'],
                                provider = job.provider,
                                timestamp = price_data['timestamp'],
                                raw_json = raw_json_str
                            )

                            db.add(raw_record)
                            db.commit()

                            produce_price_event({
                                "symbol": price_data['symbol'],
                                "price": price_data['price'],
                                "timestamp": price_data['timestamp'].isoformat(),
                                "source": price_data['provider'],
                                "raw_response_id": str(raw_record.id)
                            })

                            print(f"Produced price event for {symbol}")

                        except Exception as e:
                            print(f"Error fetching data for {symbol}: {e}")
                else:
                    print(f"Skipping job {job.job_id}, not time yet")
            time.sleep(5)
    except Exception as e:
        print(f"Error in polling job runner: {e}")
    finally:
        db.close()
        print("Database session closed")


if __name__ == "__main__":
    run()