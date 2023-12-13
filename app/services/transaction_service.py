from sqlalchemy import select
from app.database.db import database, trasactions
from app.models.transaction import Transaction, TransactionCreate

async def create_transaction(transaction: TransactionCreate):
    query = trasactions.insert().values(
        app_id=transaction.app_id,
        xref=transaction.xref,
        date=transaction.date,
        broker=transaction.broker,
        sub_broker=transaction.sub_broker,
        borrower_name=transaction.borrower_name,
        description=transaction.description,
        total_loan_amount=transaction.total_loan_amount,
        comm_rate=transaction.comm_rate,
        upfront=transaction.upfront,
        upfront_incl_gst=transaction.upfront_incl_gst
        )

    last_txn_id = await database.execute(query)
    return {**transaction.dict(), "id": last_txn_id}


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