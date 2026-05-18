from fastapi import APIRouter
from app.api.trino_client import get_trino_conn

router = APIRouter()

@router.get("/revenue")
def revenue():
    conn = get_trino_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT SUM(net) AS total_revenue
        FROM transactions
    """)

    return {"total_revenue": cur.fetchone()[0]}

@router.get("/currency")
def by_currency():
    conn = get_trino_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT currency,
               COUNT(*) AS txn_count,
               SUM(amount) AS total_amount
        FROM transactions
        GROUP BY currency
    """)

    rows = cur.fetchall()

    return [
        {"currency": r[0], "count": r[1], "amount": r[2]}
        for r in rows
    ]