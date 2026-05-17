from fastapi import FastAPI
from app.db.database import engine, Base
from app.db import models
from app.services import analytics
from app.services import fraud
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "FinSight AI Running"}


@app.get("/analytics/daily-revenue")
def daily_revenue(date: str):
    return analytics.get_daily_revenue(date)


@app.get("/analytics/categories")
def category_summary():
    return analytics.get_category_summary()


@app.get("/analytics/fees")
def fee_summary():
    return analytics.get_fee_summary()

@app.get("/fraud/detect")
def fraud_detection():
    return fraud.detect_anomalies()