from pymongo import MongoClient
from pymongo.database import Database
from app.core.config import settings

client = MongoClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]

def get_db() -> Database:
    return db