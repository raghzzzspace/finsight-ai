from app.db.database import SessionLocal
from app.db.models import Transaction

def write_to_postgres_batch(df, epoch_id=None):

    db = SessionLocal()

    try:
        rows = df.collect()

        for row in rows:
            txn = Transaction(
                event_id=row.event_id,
                transaction_id=row.transaction_id,
                customer_id=row.customer_id,
                merchant_id=row.merchant_id,
                amount=row.amount,
                fee=row.fee,
                net=row.net,
                currency=row.currency,
                payment_status=row.payment_status,
                reporting_category=row.reporting_category,
                created_at=row.created_at,
                fraud_score=getattr(row, "fraud_score", 0)
            )

            db.add(txn)

        db.commit()
        print(f"[DB] Saved batch of {len(rows)} rows")

    except Exception as e:
        print("[DB ERROR]", e)
        db.rollback()

    finally:
        db.close()