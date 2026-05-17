from faker import Faker
import random
import uuid
from datetime import datetime

fake = Faker()

PAYMENT_STATUSES = [
    "succeeded",
    "failed",
    "pending"
]

CURRENCIES = ["usd", "inr", "eur"]

REPORTING_CATEGORIES = [
    "charge",
    "refund",
    "payout",
    "fee",
    "dispute"
]


def generate_transaction():

    amount = round(random.uniform(10, 5000), 2)
    fee = round(amount * 0.029, 2)

    transaction = {
        "event_id": str(uuid.uuid4()),
        "transaction_id": f"txn_{uuid.uuid4().hex[:24]}",
        "customer_id": f"cus_{uuid.uuid4().hex[:14]}",
        "merchant_id": f"mer_{uuid.uuid4().hex[:14]}",
        "amount": amount,
        "fee": fee,
        "net": round(amount - fee, 2),
        "currency": random.choice(CURRENCIES),
        "payment_status": random.choice(PAYMENT_STATUSES),
        "reporting_category": random.choice(REPORTING_CATEGORIES),
        "payment_method": random.choice([
            "card",
            "bank_transfer",
            "wallet"
        ]),
        "created_at": datetime.utcnow().isoformat(),
        "description": fake.sentence()
    }

    return transaction


from app.kafka.producer import route_event

if __name__ == "__main__":

    for _ in range(10):
        event = generate_transaction()
        route_event(event)