from sqlalchemy import select
from app.database.db import database, transactions
from app.models.transaction import Transaction, TransactionCreate

tiers_mapping = {1: 100000, 2: 50000, 3: 10000}

def parse_transaction(transaction):
    transaction.total_loan_amount = float(transaction.total_loan_amount.replace(',', ''))
    transaction.comm_rate = float(transaction.comm_rate.replace(',', ''))
    transaction.upfront = float(transaction.upfront.replace(',', ''))
    transaction.upfront_incl_gst = float(transaction.upfront_incl_gst.replace(',', ''))
    return transaction

async def create_transaction(transaction: TransactionCreate):
    transaction = parse_transaction(transaction)
    tier = next((t for t, val in tiers_mapping.items() if transaction.total_loan_amount > val), None)
    print('tier - ', tier)
    query = transactions.insert().values(
        app_id=transaction.app_id,
        xref=transaction.xref,
        settlement_date=transaction.settlement_date,
        broker=transaction.broker,
        sub_broker=transaction.sub_broker,
        borrower_name=transaction.borrower_name,
        description=transaction.description,
        total_loan_amount=transaction.total_loan_amount,
        comm_rate=transaction.comm_rate,
        upfront=transaction.upfront,
        upfront_incl_gst=transaction.upfront_incl_gst
        )
    print(query)
    last_txn_id = await database.execute(query)
    response = {
        transaction.model_dump(),
        # "id": last_txn_id
        }
    print('response - ', response)
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