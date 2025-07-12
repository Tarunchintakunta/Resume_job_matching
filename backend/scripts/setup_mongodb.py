import json
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import uuid
from datetime import datetime

def setup_mongodb():
    """Set up MongoDB collections and indexes"""
    print("Setting up MongoDB...")
    
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["resume_matching"]
    
    # Create collections
    db.create_collection("resumes")
    db.create_collection("jobs")
    db.create_collection("matches")
    
    # Create indexes
    db.resumes.create_index("id", unique=True)
    db.jobs.create_index("id", unique=True)
    db.matches.create_index([("job_id", 1), ("resume_id", 1)], unique=True)
    
    print("MongoDB setup completed!")
    return db

def load_sample_data(db):
    """Load sample data into MongoDB"""
    print("Loading sample data...")
    
    # Load processed data
    try:
        with open("data/processed_resumes.json", "r") as f:
            resumes = json.load(f)
        
        with open("data/processed_jobs.json", "r") as f:
            jobs = json.load(f)
    except FileNotFoundError:
        print("Processed data files not found. Run prepare_data.py first.")
        return
    
    # Insert resumes
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
        db.resumes.update_one(
            {"id": resume_id},
            {"$set": resume_doc},
            upsert=True
        )
    
    # Insert jobs
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
        db.jobs.update_one(
            {"id": job_id},
            {"$set": job_doc},
            upsert=True
        )
    
    print(f"Loaded {db.resumes.count_documents({})} resumes and {db.jobs.count_documents({})} jobs")

def main():
    """Main function to set up MongoDB and load sample data"""
    db = setup_mongodb()
    load_sample_data(db)

if __name__ == "__main__":
    main()