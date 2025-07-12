from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List, Optional

from app.core.database import get_db
from app.models.match import MatchRequest, MatchResult
from app.services.matcher import ResumeMatcher

router = APIRouter()

# Initialize matcher
matcher = ResumeMatcher()

@router.post("/calculate", response_model=List[MatchResult])
async def calculate_matches(
    request: MatchRequest = Body(...),
    db = Depends(get_db)
):
    """Calculate matches between a job and resumes"""
    try:
        # Get job posting
        job = db.jobs.find_one({"id": request.job_id})
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Get resumes
        if request.resume_ids:
            # Match with specific resumes
            resumes = list(db.resumes.find({"id": {"$in": request.resume_ids}}))
        else:
            # Match with all resumes
            resumes = list(db.resumes.find())
        
        if not resumes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No resumes found to match"
            )
        
        # Calculate matches
        match_results = matcher.rank_resumes(job, resumes)
        
        # Save matches to database
        for result in match_results:
            db.matches.update_one(
                {
                    "job_id": result["job_id"],
                    "resume_id": result["resume_id"]
                },
                {"$set": result},
                upsert=True
            )
        
        return match_results
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating matches: {str(e)}"
        )

@router.get("/job/{job_id}", response_model=List[MatchResult])
async def get_matches_for_job(
    job_id: str,
    db = Depends(get_db)
):
    """Get matches for a specific job"""
    matches = list(db.matches.find({"job_id": job_id}).sort("rank", 1))
    return matches

@router.get("/resume/{resume_id}", response_model=List[MatchResult])
async def get_matches_for_resume(
    resume_id: str,
    db = Depends(get_db)
):
    """Get matches for a specific resume"""
    matches = list(db.matches.find({"resume_id": resume_id}).sort("score", -1))
    return matches