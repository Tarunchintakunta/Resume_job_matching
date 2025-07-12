import json
import pymongo
from pymongo import MongoClient
import uuid
from datetime import datetime

def setup_mongodb():
    """Set up MongoDB collections and indexes"""
    print("Setting up MongoDB...")
    
    try:
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["resume_matching"]
        
        # Check connection
        client.admin.command('ping')
        print("MongoDB connection successful!")
        
        # Create collections if they don't exist
        collection_names = db.list_collection_names()
        if "resumes" not in collection_names:
            print("Creating resumes collection...")
            db.create_collection("resumes")
        
        if "jobs" not in collection_names:
            print("Creating jobs collection...")
            db.create_collection("jobs")
        
        if "matches" not in collection_names:
            print("Creating matches collection...")
            db.create_collection("matches")
        
        # Create indexes
        print("Creating indexes...")
        db.resumes.create_index("id", unique=True)
        db.jobs.create_index("id", unique=True)
        db.matches.create_index([("job_id", 1), ("resume_id", 1)], unique=True)
        
        print("MongoDB setup completed!")
        return db
    except Exception as e:
        print(f"Error setting up MongoDB: {str(e)}")
        print("Make sure MongoDB is installed and running.")
        return None

def load_sample_data(db):
    """Load sample data into MongoDB"""
    if db is None:
        print("Database connection is None. Cannot load sample data.")
        return
        
    print("Loading sample data...")
    
    # Load processed data
    try:
        with open("data/processed_resumes.json", "r") as f:
            resumes = json.load(f)
        
        with open("data/processed_jobs.json", "r") as f:
            jobs = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        print("Processed data files not found. Run prepare_data.py first.")
        return
    
    # Insert resumes
    resume_count = 0
    for resume in resumes[:50]:  # Insert first 50 resumes
        resume_id = str(uuid.uuid4())
        
        # Prepare resume document
        resume_doc = {
            "id": resume_id,
            "name": resume.get("name", "Unknown"),
            "email": resume.get("email", ""),
            "phone": resume.get("phone", ""),
            "summary": resume.get("summary", ""),
            "skills": resume.get("skills", []),
            "education": resume.get("education", []),
            "experience": resume.get("experience", []),
            "raw_text": resume.get("summary", "") + " " + " ".join([exp.get("description", "") for exp in resume.get("experience", [])]),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # Insert resume
        try:
            result = db.resumes.update_one(
                {"id": resume_id},
                {"$set": resume_doc},
                upsert=True
            )
            if result.upserted_id or result.modified_count:
                resume_count += 1
        except Exception as e:
            print(f"Error inserting resume: {str(e)}")
    
    # Insert jobs
    job_count = 0
    for job in jobs[:10]:  # Insert first 10 jobs
        job_id = str(uuid.uuid4())
        
        # Prepare job document
        job_doc = {
            "id": job_id,
            "title": job.get("title", ""),
            "company": job.get("company", ""),
            "description": job.get("description", ""),
            "requirements": job.get("requirements", []),
            "qualifications": job.get("qualifications", []),
            "skills_required": job.get("skills_required", []),
            "location": job.get("location", ""),
            "job_type": job.get("job_type", ""),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # Insert job
        try:
            result = db.jobs.update_one(
                {"id": job_id},
                {"$set": job_doc},
                upsert=True
            )
            if result.upserted_id or result.modified_count:
                job_count += 1
        except Exception as e:
            print(f"Error inserting job: {str(e)}")
    
    print(f"Successfully loaded {resume_count} resumes and {job_count} jobs")

def main():
    """Main function to set up MongoDB and load sample data"""
    db = setup_mongodb()
    if db is not None:
        load_sample_data(db)
    else:
        print("Could not set up MongoDB. Exiting.")

if __name__ == "__main__":
    main()