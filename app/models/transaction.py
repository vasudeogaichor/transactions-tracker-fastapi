from pydantic import BaseModel

class TransactionBase(BaseModel):
    id: int
    app_id: int
    xref:int
    settlement_date: str
    broker: str
    sub_broker: str
    borrower_name: str
    description: str
    total_loan_amount: float
    comm_rate: float
    upfront: float
    upfront_incl_gst: float

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    class Config:
        orm_mode = True
