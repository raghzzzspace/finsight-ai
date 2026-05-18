from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import transactions, analytics, fraud

app = FastAPI(title="FinSight API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(fraud.router, prefix="/fraud", tags=["Fraud"])


@app.get("/")
def root():
    return {"message": "FinSight API Running with Trino 🚀"}