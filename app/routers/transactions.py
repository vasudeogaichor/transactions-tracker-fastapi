from fastapi import APIRouter, HTTPException, Depends
from app.models.transaction import Transaction, TransactionCreate
from app.services.transaction_service import create_transaction #, get_transaction, update_transaction, delete_transaction, list_transactions
from app.dependencies import get_database

router = APIRouter()

@router.post("/transactions/", response_model=Transaction, dependencies=[Depends(get_database)])
async def create_transaction_route(transaction: TransactionCreate):
    try:
        created_transaction = await create_transaction(transaction)
        return created_transaction 
    except Exception as e:
        print('Error - ', e)
        raise HTTPException(status_code=500, detail="Error while creating new transaction")

# @router.get("/transactions/{transaction_id}", response_model=Transaction)
# async def get_transaction_route(transaction_id: int):
#     transaction = await get_transaction(transaction_id)
#     if transaction is None:
#         raise HTTPException(status_code=404, detail="Transaction not found")
#     return transaction

# @router.get("/transactions/", response_model=list[Transaction])
# async def list_transactions_route(page: int = 0, limit: int = 10):
#     return await list_transactions(page, limit)

# @router.put("/transactions/{transaction_id}", response_model=Transaction)
# async def update_transaction_route(transaction_id: int, transaction: TransactionCreate):
#     return await update_transaction(transaction_id, transaction)

# @router.delete("/transactions/{transaction_id}", response_model=Transaction)
# async def delete_transaction_route(transaction_id: int):
#     return await delete_transaction(transaction_id)