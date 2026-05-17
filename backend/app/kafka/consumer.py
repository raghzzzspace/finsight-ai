import json
from kafka import KafkaConsumer
from app.db.database import SessionLocal
from app.db.models import Transaction

KAFKA_BROKER = "localhost:9092"

consumer = KafkaConsumer(
    "payment-events",
    "refund-events",
    "payout-events",
    "fee-events",
    "fraud-events",
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True
)


def save_to_db(event):
    db = SessionLocal()

    try:
        txn = Transaction(
            event_id=event["event_id"],
            transaction_id=event["transaction_id"],
            customer_id=event["customer_id"],
            merchant_id=event["merchant_id"],
            amount=event["amount"],
            fee=event["fee"],
            net=event["net"],
            currency=event["currency"],
            payment_status=event["payment_status"],
            reporting_category=event["reporting_category"],
        )

        db.add(txn)
        db.commit()
        print(f"[DB] Saved {event['event_id']}")

    except Exception as e:
        print("[DB ERROR]", e)
        db.rollback()

    finally:
        db.close()


def start_consumer():
    print("[Kafka] Consumer started...")

    for message in consumer:
        event = message.value
        save_to_db(event)


if __name__ == "__main__":
    start_consumer()