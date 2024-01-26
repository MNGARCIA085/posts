from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = "mongodb://localhost:27017"
DB_NAME = "mydatabase"

async def get_database():
    client = AsyncIOMotorClient(MONGODB_URL)
    try:
        database = client[DB_NAME]
        yield database
    finally:
        client.close()
