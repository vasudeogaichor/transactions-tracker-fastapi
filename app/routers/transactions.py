import os
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Query
from app.models.transaction import Transaction, TransactionCreate
from app.models.stats import Stats
from app.services.transaction_service import (
    create_transaction, get_loan_stats
)  # , get_transaction, update_transaction, delete_transaction, list_transactions
from app.services.file_service import (
    extract_data_from_pdf,
    insert_transactions_into_database,
)
from app.dependencies import get_database

router = APIRouter()

@router.post("/files/upload/")
async def upload_pdf_route(
    file: UploadFile = File(...), database=Depends(get_database)
):
    try:
        # Save the uploaded file temporarily
        file_path = f"temp/{file.filename}"
        with open(file_path, "wb") as pdf_file:
            pdf_file.write(file.file.read())

        # Extract data from the PDF
        transactions = extract_data_from_pdf(file_path)
        # Insert transactions into the database
        (
            total_successful_txns,
            unsuccessful_txns,
        ) = await insert_transactions_into_database(transactions)

        return {
            "message": f"No. of Successful transactions: {total_successful_txns}, Unsuccessful transactions: {unsuccessful_txns}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Clean up: Remove the temporary PDF file
        os.remove(file_path)


@router.post(
    "/transactions/", response_model=Transaction, dependencies=[Depends(get_database)]
)
async def create_transaction_route(transaction: TransactionCreate):
    try:
        created_transaction = await create_transaction(transaction)
        return created_transaction
    except Exception as e:
        print("Error - ", e)
        raise HTTPException(
            status_code=500, detail="Error while creating new transaction"
        )

@router.get(
    "/transactions/stats", response_model=Stats, dependencies=[Depends(get_database)]
)
async def create_get_stats_route(
    start_date: str = None,
    end_date: str = None,
    broker: str = None,
):
    try:
        stats = await get_loan_stats(start_date, end_date, broker)
        return stats
    except Exception as e:
        print('Error - ', e)
        raise HTTPException(
            status_code=500, detail="Error while getting stats"
        )

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
