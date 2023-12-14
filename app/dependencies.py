
from app.database.db import database

async def get_database():
    try:
        await database.connect()
        yield database
    finally:
        await database.disconnect()
