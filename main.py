# project_root/main.py

from fastapi import FastAPI
# from app.routers.item import router as item_router
# from app.database.db import database

app = FastAPI()

# Include the routers
# app.include_router(item_router, prefix="/v1")

# Check if the database is connected before starting the server
@app.on_event("startup")
async def startup_db_client():
    # await database.connect()
    print('db connected')

@app.on_event("shutdown")
async def shutdown_db_client():
    # await database.disconnect()
    print('db disconnected')