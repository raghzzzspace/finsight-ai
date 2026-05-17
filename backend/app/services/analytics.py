from sqlalchemy import text
from app.db.database import SessionLocal


def get_daily_revenue(date: str):
    db = SessionLocal()

    query = text("""
        SELECT
            DATE(created_at) as day,
            SUM(amount) as total_amount,
            SUM(fee) as total_fees,
            SUM(net) as total_net
        FROM transactions
        WHERE DATE(created_at) = :date
        GROUP BY DATE(created_at)
    """)

    result = db.execute(query, {"date": date}).fetchone()
    db.close()

    if result:
        return {
            "date": str(result.day),
            "total_amount": float(result.total_amount),
            "total_fees": float(result.total_fees),
            "total_net": float(result.total_net)
        }

    return {"message": "No data found"}


def get_category_summary():
    db = SessionLocal()

    query = text("""
        SELECT
            reporting_category,
            COUNT(*) as count,
            SUM(amount) as total_amount
        FROM transactions
        GROUP BY reporting_category
    """)

    rows = db.execute(query).fetchall()
    db.close()

    return [
        {
            "category": r.reporting_category,
            "count": r.count,
            "total_amount": float(r.total_amount)
        }
        for r in rows
    ]


def get_fee_summary():
    db = SessionLocal()

    query = text("""
        SELECT
            SUM(fee) as total_fees,
            AVG(fee) as avg_fee
        FROM transactions
    """)

    result = db.execute(query).fetchone()
    db.close()

    return {
        "total_fees": float(result.total_fees or 0),
        "average_fee": float(result.avg_fee or 0)
    }