from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from app.routers.transactions import router as transaction_router
from app.database.db import database
from alembic import command
from alembic.config import Config as AlembicConfig
import time

app = FastAPI()

app.include_router(transaction_router)

# app.add_middleware(PayloadParsingMiddleware)

# @app.middleware("http")
# async def log_request_payload(request: Request, call_next):
#     try:
#         body = await request.body()
#         print('Request Payload:', body)
#     except Exception as e:
#         print(f'Error reading request payload: {e}')

#     response = await call_next(request)
#     return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    alembic_config = AlembicConfig("alembic.ini")
    command.upgrade(alembic_config, "head")
    await database.connect()
    
    yield
    
    await database.disconnect()
    
