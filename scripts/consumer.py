import os
from confluent_kafka import Consumer
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.symbol_average import SymbolAverage
from app.models.price_point import PricePoint
import json
from datetime import datetime
import uuid

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "price-events")

config = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': 'symbol-average-consumer-' + str(uuid.uuid4()),  
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(config)
consumer.subscribe([KAFKA_TOPIC])

def process_message(msg_value: dict, db: Session):
    symbol = msg_value['symbol']
    price = float(msg_value['price'])
    timestamp = datetime.fromisoformat(msg_value['timestamp'])
    provider = msg_value['source']

    price_point = PricePoint(
        symbol=symbol,
        price=price,
        timestamp=timestamp,
        provider=provider
    )
    db.add(price_point)
    print(f"Saved to PricePoint: {symbol} at {timestamp}")

    previous = (
        db.query(PricePoint)
        .filter(PricePoint.symbol == symbol)
        .order_by(PricePoint.timestamp.desc())
        .limit(4)
        .all()
    )

    prices = [price] + [p.price for p in previous]
    moving_average = sum(prices) / len(prices)

    average_record = SymbolAverage(
        symbol=symbol,
        timestamp=timestamp,
        moving_average=moving_average,
        provider=provider
    )
    db.merge(average_record)

    db.commit()
    print(f"Processed {symbol} at {timestamp} with moving average {moving_average}")


def consume():
    db = SessionLocal()
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"⚠️ Error: {msg.error()}")
                continue

            try:
                print("Raw Kafka message received:", msg.value())
                data = json.loads(msg.value().decode("utf-8"))
                print("Decoded message:", data)

                process_message(data, db)

            except Exception as e:
                print(f"Failed to process message: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    consume()