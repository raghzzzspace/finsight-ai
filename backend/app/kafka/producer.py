import json
from kafka import KafkaProducer
from app.kafka.topics import (
    TRANSACTIONS_TOPIC
)

KAFKA_BROKER = "localhost:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


def send_event(topic: str, event: dict):
    producer.send(topic, value=event)
    producer.flush()
    print(f"[Kafka] Sent to {topic}: {event['event_id']}")


def route_event(event: dict):
    send_event(TRANSACTIONS_TOPIC, event)