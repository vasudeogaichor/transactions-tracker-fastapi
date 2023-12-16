from sqlalchemy import select,func
from app.database.db import database, transactions
from app.models.transaction import Transaction, TransactionCreate
from app.models.stats import Stats
from datetime import datetime

tiers_mapping = {1: 100000, 2: 50000, 3: 10000}


async def create_transaction(transaction: TransactionCreate):
    tier = next(
        (t for t, val in tiers_mapping.items() if transaction.total_loan_amount > val),
        None,
    )

    query = (
        transactions.insert()
        .values(
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
            upfront_incl_gst=transaction.upfront_incl_gst,
            tier=tier,
        )
        .returning(transactions)
    )

    last_txn = await database.fetch_one(query)
    response = dict(last_txn)

    return response

def apply_filters(query, start_date, end_date, broker):
    if broker and broker.strip():
        query = query.where(transactions.c.broker == broker)
    if start_date:
        query = query.where(transactions.c.settlement_date >= start_date)
    if end_date:
        query = query.where(transactions.c.settlement_date <= end_date)

    return query

async def get_loan_stats(start_date, end_date, broker):
    if start_date:
        start_date = datetime.strptime(start_date, "%d-%m-%Y").date()

    if end_date:
        end_date = datetime.strptime(end_date, "%d-%m-%Y").date()

    total_query = select(
        [
            func.count().label("total_number_of_loans"),
            func.sum(transactions.c.total_loan_amount).label("total_loan_amount"),
        ]
    )
    total_query = apply_filters(total_query, start_date, end_date, broker)
    total_results = await database.fetch_one(total_query)
    
    avg_query = select([func.avg(transactions.c.total_loan_amount).label("average_loan_amount")])
    avg_query = apply_filters(avg_query, start_date, end_date, broker)
    avg_results = await database.fetch_one(avg_query)
    
    lowest_query = select([transactions]).order_by(transactions.c.total_loan_amount.asc()).limit(1)
    lowest_query = apply_filters(lowest_query, start_date, end_date, broker)
    lowest_results = await database.fetch_one(lowest_query)
    
    highest_query = select([transactions]).order_by(transactions.c.total_loan_amount.desc()).limit(1)
    highest_query = apply_filters(highest_query, start_date, end_date, broker)
    highest_results = await database.fetch_one(highest_query)
    
    stats = Stats(
            total_number_of_loans=total_results["total_number_of_loans"],
            total_loan_amount=total_results["total_loan_amount"],
            average_loan_amount=avg_results["average_loan_amount"],
            loan_with_lowest_amount=Transaction(**lowest_results),
            loan_with_highest_amount=Transaction(**highest_results)
        )

    return stats
        
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
