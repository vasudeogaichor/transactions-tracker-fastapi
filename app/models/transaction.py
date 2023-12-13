from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    app_id: int
    xref:int
    settlement_date: str
    broker: str
    sub_broker: Optional[str] = None
    borrower_name: str
    description: str
    total_loan_amount: str
    comm_rate: str
    upfront: str
    upfront_incl_gst: str

class TransactionCreate(TransactionBase):
    app_id: int
    xref:int
    settlement_date: str
    broker: str
    sub_broker: Optional[str] = None
    borrower_name: str
    description: str
    total_loan_amount: str
    comm_rate: str
    upfront: str
    upfront_incl_gst: str

class Transaction(TransactionBase):
    id: int
    tier: int
    created_at: datetime
    class Config:
        from_attributes = True
