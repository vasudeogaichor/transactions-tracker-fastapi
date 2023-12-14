from PyPDF2 import PdfReader
import os
from fastapi import HTTPException
from app.services.transaction_service import create_transaction
from app.models.transaction import Transaction, TransactionCreate
from app.database.db import database, transactions

async def insert_transactions_into_database(transactions, database):
    for transaction_data in transactions:
        transaction = TransactionCreate(**transaction_data)
        await create_transaction(transaction, database)

def extract_data_from_line(line):
    # Implement your logic to extract data from a line
    # This is just a placeholder, adjust it based on the actual PDF structure
    transaction_data = {
        "transaction_id": "123",
        "amount": 1000.0,
        "description": "Sample Transaction"
    }
    return transaction_data

def extract_transactions_from_text(text):
    transactions = []

    # Implement your logic to parse transactions from the text
    # This is just a placeholder, adjust it based on the actual PDF structure
    rows = text.strip().split('\n')
    print('rows - ', rows)
    return transactions

def extract_data_from_pdf(file_path):
    print('file_path - ', file_path)
    transactions = []

    with open(file_path, "rb") as file:
        pdf_reader = PdfReader(file)
        print('total pages - ', len(pdf_reader.pages))
        # Loop through each page in the PDF
        for page_num in range(len(pdf_reader.pages)):
            print('current_page_no - ', page_num)
            page = pdf_reader.pages[page_num]
            print('current_page - ', page)
            text = page.extract_text()
            print('text - ', text)
            text = text[:-6]
            print('text - ', text)
            transactions += extract_transactions_from_text(text)

    return transactions