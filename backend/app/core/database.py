from pymongo import MongoClient
from pymongo.database import Database
from app.core.config import settings
from fastapi import Depends

# Create a MongoDB client
client = MongoClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]

def get_db() -> Database:
    """
    Dependency to get MongoDB database connection
    """
    return db

def get_resume_collection():
    """
    Dependency to get resumes collection
    """
    return db.resumes

def get_job_collection():
    """
    Dependency to get jobs collection
    """
    return db.jobs

def get_match_collection():
    """
    Dependency to get matches collection
    """
    return db.matches