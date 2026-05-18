from fastapi import APIRouter
from app.api.trino_client import get_trino_conn

router = APIRouter()

@router.get("/")
def get_transactions(limit: int = 50):
    conn = get_trino_conn()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT *
        FROM transactions
        ORDER BY created_at DESC
        LIMIT {limit}
    """)

    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()

    return [dict(zip(columns, row)) for row in rows]