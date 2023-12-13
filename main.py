from contextlib import asynccontextmanager
from fastapi import FastAPI
# from app.routers.item import router as item_router
from app.database.db import database
from alembic import command
from alembic.config import Config as AlembicConfig

app = FastAPI()

# Include the routers
# app.include_router(item_router, prefix="/v1")

@asynccontextmanager
async def lifespan(app: FastAPI):
    alembic_config = AlembicConfig("alembic.ini")
    command.upgrade(alembic_config, "head")
    await database.connect()
    
    yield
    
    await database.disconnect()
    
