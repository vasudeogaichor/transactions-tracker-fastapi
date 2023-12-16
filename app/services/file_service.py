import tabula
import pandas as pd
from app.services.transaction_service import create_transaction
from app.models.transaction import TransactionCreate

async def insert_transactions_into_database(transactions):
    total_successful_txns = 0
    unsuccessful_txns = []
    for transaction_data in transactions:
        try:
            transaction = TransactionCreate(**transaction_data)
            successful_txn = await create_transaction(transaction)
            if successful_txn['id']:
                total_successful_txns += 1
        except:
            unsuccessful_txns.append(transaction_data)
            
    return total_successful_txns, unsuccessful_txns
        

def extract_data_from_pdf(file_path):
    tables = tabula.read_pdf(file_path,pages="all", pandas_options={"header": [0, 1]})

    # Using tabula and pandas, extract all tables from pdf as dataframes
    # Stack them vertically and convert the final dataframe to array of json objects
    dfs = []

    # Iterate through the extracted tables
    for i, table in enumerate(tables):
        # Convert each table to a pandas DataFrame
        df = pd.DataFrame(table)

        df = df.dropna(axis=1, how='all')
        df = df.reset_index(drop=True)
        df.columns = range(df.shape[1])

        dfs.append(df)

    # Merge DataFrames vertically
    merged_df = pd.concat(dfs, ignore_index=True)

    if 0 in merged_df.columns:
        new_columns = merged_df[0].str.split(expand=True)
        merged_df.insert(loc=1, column='app_id', value=new_columns[0])
        merged_df.insert(loc=2, column='xref', value=new_columns[1])
        merged_df.drop(columns=0, inplace=True)

    if 4 in merged_df.columns:
        new_columns = merged_df[4].str.split("Upfront Commission", expand=True)
        merged_df.insert(loc=6, column='borrower_name', value=new_columns[0])
        merged_df.insert(loc=7, column='description', value="Upfront Commission")
        merged_df.drop(columns=4, inplace=True)

    merged_df.columns = ['app_id', 'xref', 'settlement_date', 'broker', 'sub_broker', 'borrower_name',
                        'description', 'total_loan_amount', 'comm_rate', 'upfront', 'upfront_incl_gst']
    
    transactions = merged_df.to_dict(orient='records')
    
    for record in transactions:
        for key in list(record.keys()):
            if pd.isna(record[key]):
                del record[key]
    
    return transactions
