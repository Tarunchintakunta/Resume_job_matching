import pymongo
from pymongo import MongoClient
import os

def setup_mongodb():
    """Set up MongoDB collections and indexes (no sample data inserted)"""
    print("Setting up MongoDB...")

    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")

    try:
        client = MongoClient(mongodb_url, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("MongoDB connection successful!")

        db = client["resume_matching"]

        # Create collections if they don't exist
        collection_names = db.list_collection_names()
        for col_name in ["resumes", "jobs", "matches"]:
            if col_name not in collection_names:
                print(f"Creating {col_name} collection...")
                db.create_collection(col_name)

        # Create indexes
        print("Creating indexes...")
        db.resumes.create_index("id", unique=True)
        db.jobs.create_index("id", unique=True)
        db.matches.create_index([("job_id", 1), ("resume_id", 1)], unique=True)

        print("MongoDB setup completed! (No sample data inserted - add your own resumes and jobs)")
        return db
    except Exception as e:
        print(f"Warning: Could not connect to MongoDB: {str(e)}")
        print("The app will still work - MongoDB will be set up when the server starts.")
        print("Make sure MongoDB is running before starting the backend server.")
        return None

def main():
    setup_mongodb()

if __name__ == "__main__":
    main()
