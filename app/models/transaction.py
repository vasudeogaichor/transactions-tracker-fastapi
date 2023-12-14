from pydantic import BaseModel, validator
from typing import Optional
from datetime import date, datetime


class TransactionBase(BaseModel):
    app_id: int
    xref: int
    settlement_date: date | str
    broker: str
    sub_broker: Optional[str] = None
    borrower_name: str
    description: str
    total_loan_amount: float | str
    comm_rate: float | str
    upfront: float | str
    upfront_incl_gst: float | str


class TransactionCreate(TransactionBase):
    app_id: int
    xref: int
    settlement_date: date | str
    broker: str
    sub_broker: Optional[str] = None
    borrower_name: str
    description: str
    total_loan_amount: float | str
    comm_rate: float | str
    upfront: float | str
    upfront_incl_gst: float | str

    @validator("settlement_date")
    def parse_settlement_date(cls, value: str) -> date:
        try:
            return datetime.strptime(value, "%d/%m/%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Expected format: DD/MM/YYYY")

    @validator("total_loan_amount", "comm_rate", "upfront", "upfront_incl_gst")
    def parse_float_fields(cls, value: str) -> float:
        try:
            return float(str(value).replace(",", ""))
        except ValueError:
            raise ValueError("Invalid float format")


class Transaction(TransactionBase):
    id: int
    tier: int
    created_at: datetime | None

    class Config:
        from_attributes = True
