from sqlalchemy import select, func
from app.database.db import database, transactions
from app.models.transaction import Transaction, TransactionCreate
from app.models.stats import Stats
from datetime import datetime
from fastapi import HTTPException

tiers_mapping = {1: 100000, 2: 50000, 3: 10000}


# create a new transaction
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


# generate loan stats based on filters
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

    avg_query = select(
        [func.avg(transactions.c.total_loan_amount).label("average_loan_amount")]
    )
    avg_query = apply_filters(avg_query, start_date, end_date, broker)
    avg_results = await database.fetch_one(avg_query)

    lowest_query = (
        select([transactions]).order_by(transactions.c.total_loan_amount.asc()).limit(1)
    )
    lowest_query = apply_filters(lowest_query, start_date, end_date, broker)
    lowest_results = await database.fetch_one(lowest_query)

    highest_query = (
        select([transactions])
        .order_by(transactions.c.total_loan_amount.desc())
        .limit(1)
    )
    highest_query = apply_filters(highest_query, start_date, end_date, broker)
    highest_results = await database.fetch_one(highest_query)

    stats = Stats(
        total_number_of_loans=total_results["total_number_of_loans"],
        total_loan_amount=total_results["total_loan_amount"],
        average_loan_amount=avg_results["average_loan_amount"],
        loan_with_lowest_amount=Transaction(**lowest_results),
        loan_with_highest_amount=Transaction(**highest_results),
    )

    return stats

def apply_broker_filter(query, broker):
    if broker and broker.strip():
        query = query.where(transactions.c.broker == broker)
    return query

# generate report based on filters
async def get_report(broker, period):
    if "," in period:
        period = period.split(",")
    else:
        period = [period]
    report = {}

    for p in period:
        if p not in ["daily", "weekly", "monthly"]:
            raise HTTPException(status_code=400, detail=f"Invalid period: {p}")

        if p == "daily":
            query = select(
                [
                    transactions.c.settlement_date,
                    func.max(transactions.c.total_loan_amount).label(
                        "max_total_loan_amount"
                    ),
                    func.min(transactions.c.total_loan_amount).label(
                        "min_total_loan_amount"
                    ),
                    func.sum(transactions.c.total_loan_amount).label(
                        "sum_total_loan_amount"
                    ),
                ]
            ).group_by(transactions.c.settlement_date)
            query = apply_broker_filter(query, broker)
            result = await database.fetch_all(query)
            report["daily"] = [
                {
                    res.settlement_date.strftime("%Y-%m-%d"): {
                        "max_total_loan_amount": res.max_total_loan_amount,
                        "min_total_loan_amount": res.min_total_loan_amount,
                        "sum_total_loan_amount": res.sum_total_loan_amount,
                    }
                }
                for res in result
            ]

        if p == "weekly":
            query = select(
                [
                    func.date_trunc("week", transactions.c.settlement_date).label(
                        "week_start"
                    ),
                    func.max(transactions.c.total_loan_amount).label(
                        "max_total_loan_amount"
                    ),
                    func.min(transactions.c.total_loan_amount).label(
                        "min_total_loan_amount"
                    ),
                    func.sum(transactions.c.total_loan_amount).label(
                        "sum_total_loan_amount"
                    ),
                ]
            ).group_by("week_start")
            query = apply_broker_filter(query, broker)
            result = await database.fetch_all(query)
            
            report["weekly"] = [
                {
                    res.week_start.strftime("%Y-%m-%d"): {
                        "max_total_loan_amount": res.max_total_loan_amount,
                        "min_total_loan_amount": res.min_total_loan_amount,
                        "sum_total_loan_amount": res.sum_total_loan_amount,
                    }
                }
                for res in result
            ]
            
        if p == "monthly":
            query = select(
                [
                    func.date_trunc("month", transactions.c.settlement_date).label(
                        "month_start"
                    ),
                    func.max(transactions.c.total_loan_amount).label(
                        "max_total_loan_amount"
                    ),
                    func.min(transactions.c.total_loan_amount).label(
                        "min_total_loan_amount"
                    ),
                    func.sum(transactions.c.total_loan_amount).label(
                        "sum_total_loan_amount"
                    ),
                ]
            ).group_by("month_start")
            query = apply_broker_filter(query, broker)
            result = await database.fetch_all(query)
            report["monthly"] = [
                {
                    res.month_start.strftime("%Y-%m-%d"): {
                        "max_total_loan_amount": res.max_total_loan_amount,
                        "min_total_loan_amount": res.min_total_loan_amount,
                        "sum_total_loan_amount": res.sum_total_loan_amount,
                    }
                }
                for res in result
            ]
            
    return report


def get_max_transaction_for_period(p):
    if p == "daily":
        return select(
            [
                transactions.c.settlement_date,
                func.max(transactions.c.total_loan_amount).label(
                    "max_total_loan_amount"
                ),
            ]
        ).group_by(transactions.c.settlement_date)

    elif p == "weekly":
        return select(
            [
                transactions.c.settlement_date,
                func.max(transactions.c.total_loan_amount).label(
                    "max_total_loan_amount"
                ),
            ]
        ).group_by(func.date_trunc("week", transactions.c.settlement_date))

    # elif p == 'monthly':
    #     # Group by each month's start date
    #     grouped_rows = await database.execute(
    #         select([transactions]).group_by(func.date_trunc('month', transactions.c.settlement_date), transactions.c.id)
    #     ).fetchall()
    # else:
    #     raise ValueError(f"Invalid period: {period}")


# async def get_transaction(transaction_id: int):
#     query = select(transaction).where(transactions.c.id == transaction_id)
#     return await database.fetch_one(query)

# async def get_transaction(skip: int = 0, limit: int = 10):
#     query = select(transaction).offset(skip).limit(limit)
#     return await database.fetch_all(query)

# async def update_transaction(transaction_id: int, transaction: TransactionCreate):
#     query = transactions.update().where(transactions.c.id == transaction_id).values(
#         name=transaction.name, description=transaction.description
#     )
#     await database.execute(query)
#     return {**transaction.dict(), "id": transaction_id}

# async def delete_transaction(transaction_id: int):
#     query = transactions.delete().where(transactions.c.id == transaction_id)
#     return await database.execute(query)
