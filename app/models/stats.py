from pydantic import BaseModel
from app.models.transaction import Transaction

class StatsBase(BaseModel):
    total_number_of_loans: int | None
    total_loan_amount: float | None
    average_loan_amount: float | None
    loan_with_lowest_amount: Transaction | None
    loan_with_highest_amount: Transaction | None
    
class Stats(StatsBase):
    class Config:
        from_attributes = True