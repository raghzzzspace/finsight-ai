from sqlalchemy import Column, String, Float, DateTime
from datetime import datetime
from app.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    event_id = Column(String, primary_key=True)
    transaction_id = Column(String)
    customer_id = Column(String)
    merchant_id = Column(String)

    amount = Column(Float)
    fee = Column(Float)
    net = Column(Float)

    currency = Column(String)
    payment_status = Column(String)
    reporting_category = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)