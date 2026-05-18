from fastapi import APIRouter
from app.api.trino_client import get_trino_conn

router = APIRouter()

@router.get("/alerts")
def fraud_alerts():
    conn = get_trino_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM transactions
        WHERE fraud_score = 1
        ORDER BY created_at DESC
    """)

    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()

    return [dict(zip(columns, row)) for row in rows]