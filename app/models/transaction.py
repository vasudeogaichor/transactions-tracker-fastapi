from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class TransactionBase(BaseModel):
    app_id: int
    xref:int
    settlement_date: date | None
    broker: str
    sub_broker: Optional[str] = None
    borrower_name: str
    description: str
    total_loan_amount: float
    comm_rate: float
    upfront: float
    upfront_incl_gst: float

class TransactionCreate(TransactionBase):
    app_id: int
    xref:int
    settlement_date: date
    broker: str
    sub_broker: Optional[str] = None
    borrower_name: str
    description: str
    total_loan_amount: float
    comm_rate: float
    upfront: float
    upfront_incl_gst: float

class Transaction(TransactionBase):
    id: int
    tier: int
    created_at: datetime | None
    class Config:
        orm_mode = True
