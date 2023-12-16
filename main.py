from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from app.routers.transactions import router as transaction_router
from app.database.db import database
from alembic import command
from alembic.config import Config as AlembicConfig

app = FastAPI()

app.include_router(transaction_router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    alembic_config = AlembicConfig("alembic.ini")
    command.upgrade(alembic_config, "head")
    await database.connect()
    
    yield
    
    await database.disconnect()
    
