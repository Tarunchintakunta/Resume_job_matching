from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.job import Job
from app.services.vectorizer import ResumeJobVectorizer
from app.services.text_processor import TextProcessor

router = APIRouter()

# Initialize services
vectorizer = ResumeJobVectorizer("models/tfidf_vectorizer.pkl")
text_processor = TextProcessor()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Job)
async def create_job(
    job: Job = Body(...),
    db = Depends(get_db)
):
    """Create a new job posting"""
    try:
        # Generate job description text for vectorization
        job_text = f"{job.title} {job.description} {' '.join(job.requirements)} {' '.join(job.qualifications)}"
        
        # Vectorize job text
        vector = vectorizer.vectorize(job_text)
        job.vector = vector.tolist()
        
        # Save to database
        job_dict = job.dict()
        # Fill in defaults for missing fields
        job_dict.setdefault("requirements", [])
        job_dict.setdefault("qualifications", [])
        job_dict.setdefault("skills_required", [])
        job_dict.setdefault("experience_required", 0)
        job_dict.setdefault("location", "")
        job_dict.setdefault("job_type", "")
        job_dict.setdefault("salary_range", "")
        job_dict.setdefault("vector", [])
        job_dict.setdefault("created_at", datetime.now())
        job_dict.setdefault("updated_at", datetime.now())
        db.jobs.insert_one(job_dict)
        
        return job
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating job: {str(e)}"
        )

@router.get("/", response_model=List[Job])
async def get_jobs(
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_db)
):
    """Get list of job postings"""
    jobs = list(db.jobs.find().skip(skip).limit(limit))
    return jobs

@router.get("/{job_id}", response_model=Job)
async def get_job(
    job_id: str,
    db = Depends(get_db)
):
    """Get a specific job posting by ID"""
    job = db.jobs.find_one({"id": job_id})
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return job

@router.put("/{job_id}", response_model=Job)
async def update_job(
    job_id: str,
    job_update: Job = Body(...),
    db = Depends(get_db)
):
    """Update a job posting"""
    # Check if job exists
    existing_job = db.jobs.find_one({"id": job_id})
    if not existing_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Generate job description text for vectorization
    job_text = f"{job_update.title} {job_update.description} {' '.join(job_update.requirements)} {' '.join(job_update.qualifications)}"
    
    # Vectorize job text
    vector = vectorizer.vectorize(job_text)
    job_update.vector = vector.tolist()
    job_update.updated_at = datetime.now()
    
    # Update in database
    job_update_dict = job_update.dict()
    job_update_dict.setdefault("requirements", [])
    job_update_dict.setdefault("qualifications", [])
    job_update_dict.setdefault("skills_required", [])
    job_update_dict.setdefault("experience_required", 0)
    job_update_dict.setdefault("location", "")
    job_update_dict.setdefault("job_type", "")
    job_update_dict.setdefault("salary_range", "")
    job_update_dict.setdefault("vector", [])
    job_update_dict.setdefault("created_at", existing_job.get("created_at", datetime.now()))
    job_update_dict.setdefault("updated_at", datetime.now())
    db.jobs.update_one(
        {"id": job_id},
        {"$set": job_update_dict}
    )
    
    return job_update

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: str,
    db = Depends(get_db)
):
    """Delete a job posting"""
    result = db.jobs.delete_one({"id": job_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return None