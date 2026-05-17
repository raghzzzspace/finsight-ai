import json
from kafka import KafkaProducer
from app.kafka.topics import (
    PAYMENT_TOPIC,
    PAYOUT_TOPIC,
    FRAUD_TOPIC,
    REFUND_TOPIC,
    FEE_TOPIC
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
    """
    Routes Stripe-like event to correct topic
    """
    category = event.get("reporting_category")

    if category == "charge":
        send_event(PAYMENT_TOPIC, event)

    elif category == "payout":
        send_event(PAYOUT_TOPIC, event)

    elif category == "refund":
        send_event(REFUND_TOPIC, event)

    elif category == "fee":
        send_event(FEE_TOPIC, event)

    elif category == "dispute":
        send_event(FRAUD_TOPIC, event)

    else:
        print("[Kafka] Unknown category:", category)