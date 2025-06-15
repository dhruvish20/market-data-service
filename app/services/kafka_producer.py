from confluent_kafka import Producer
import json
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "price-events")

config = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS
}


producer = Producer(config)

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def produce_price_event(messaage: dict):
    producer.produce(
        topic = KAFKA_TOPIC,
        value = json.dumps(messaage),
        callback=delivery_report
    )
    producer.flush()