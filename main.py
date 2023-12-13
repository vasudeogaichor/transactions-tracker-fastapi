from contextlib import asynccontextmanager
from fastapi import FastAPI
# from app.routers.item import router as item_router
from app.database.db import database

app = FastAPI()

# Include the routers
# app.include_router(item_router, prefix="/v1")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    print('db connected')
    yield
    await database.disconnect()
    print('db disconnected')
    