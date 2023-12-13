from sqlalchemy import select
from app.database.db import database, transactions
from app.models.transaction import Transaction, TransactionCreate
from datetime import datetime

tiers_mapping = {1: 100000, 2: 50000, 3: 10000}

async def create_transaction(transaction: TransactionCreate):
    try:
        await database.connect()
        tier = next((t for t, val in tiers_mapping.items() if transaction.total_loan_amount > val), None)
        print('tier - ', tier)
        
        # input_date = datetime.strptime(transaction.settlement_date, "%d/%m/%Y")
        transaction.settlement_date = transaction.settlement_date.strftime("%Y-%m-%d")
        print('transaction - ', transaction)    
        query = transactions.insert().values(
            app_id=transaction.app_id,
            xref=transaction.xref,
            # settlement_date=transaction.settlement_date,
            broker=transaction.broker,
            sub_broker=transaction.sub_broker,
            borrower_name=transaction.borrower_name,
            description=transaction.description,
            total_loan_amount=transaction.total_loan_amount,
            comm_rate=transaction.comm_rate,
            upfront=transaction.upfront,
            upfront_incl_gst=transaction.upfront_incl_gst,
            tier=tier
            ).returning(transactions)
        print(query)
        last_txn = await database.fetch_one(query)
        print('last_txn - ', dict(last_txn))
        response = dict(last_txn)

        return response
    except Exception as e:
        print('e - ', e)
        return {"Error: Unable to create new transaction"}


# async def get_item(item_id: int):
#     query = select(items).where(items.c.id == item_id)
#     return await database.fetch_one(query)

# async def get_items(skip: int = 0, limit: int = 10):
#     query = select(items).offset(skip).limit(limit)
#     return await database.fetch_all(query)

# async def update_item(item_id: int, item: ItemCreate):
#     query = items.update().where(items.c.id == item_id).values(
#         name=item.name, description=item.description
#     )
#     await database.execute(query)
#     return {**item.dict(), "id": item_id}

# async def delete_item(item_id: int):
#     query = items.delete().where(items.c.id == item_id)
#     return await database.execute(query)