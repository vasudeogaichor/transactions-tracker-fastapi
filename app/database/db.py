from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "transactions")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_HOST = os.getenv("DB_HOST", "db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

database = Database(DATABASE_URL)

metadata = MetaData()

transactions = Table(
    "transactions",
    metadata,
    Column("id", Integer, primary_key=True, index=True, autoIncrement=True),
    Column("app_id", Integer),
    Column("xref", String),
    Column("settlement_date", String),
    Column("broker", String),
    Column("sub_broker", String),
    Column("borrower_name", String),
    Column("total_loan_amount", Float),
    Column("comm_rate", Float),
    Column("upfront", Float),
    Column("upfront_incl_gst", Float),
)

engine = create_engine(DATABASE_URL)
metadata.create_all(bind=engine)
