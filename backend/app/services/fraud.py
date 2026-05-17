from sqlalchemy import text
from app.db.database import SessionLocal


def detect_anomalies():
    db = SessionLocal()

    # 1. High amount anomalies (outliers)
    high_amount_query = text("""
        SELECT *
        FROM transactions
        WHERE amount > (
            SELECT AVG(amount) + 2 * STDDEV(amount)
            FROM transactions
        )
        ORDER BY amount DESC
        LIMIT 10
    """)

    high_amounts = db.execute(high_amount_query).fetchall()


    # 2. Refund abuse (too many refunds)
    refund_query = text("""
        SELECT customer_id, COUNT(*) as refund_count
        FROM transactions
        WHERE reporting_category = 'refund'
        GROUP BY customer_id
        HAVING COUNT(*) > 3
    """)

    refund_abuse = db.execute(refund_query).fetchall()


    # 3. Failed payment spikes
    failed_query = text("""
        SELECT customer_id, COUNT(*) as failed_count
        FROM transactions
        WHERE payment_status = 'failed'
        GROUP BY customer_id
        HAVING COUNT(*) > 3
    """)

    failed_spikes = db.execute(failed_query).fetchall()

    db.close()

    return {
        "high_amount_anomalies": [
            {
                "transaction_id": r.transaction_id,
                "amount": r.amount,
                "customer_id": r.customer_id
            }
            for r in high_amounts
        ],

        "refund_abuse": [
            {
                "customer_id": r.customer_id,
                "refund_count": r.refund_count
            }
            for r in refund_abuse
        ],

        "failed_payment_spikes": [
            {
                "customer_id": r.customer_id,
                "failed_count": r.failed_count
            }
            for r in failed_spikes
        ]
    }