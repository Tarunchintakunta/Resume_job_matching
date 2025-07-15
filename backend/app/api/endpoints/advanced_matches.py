from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List, Optional, Dict, Any

from app.core.database import get_db
from app.models.match import MatchRequest, MatchResult
from app.services.advanced_matcher import AdvancedResumeMatcher
from app.services.performance_monitor import performance_monitor

router = APIRouter()

# Initialize advanced matcher
advanced_matcher = AdvancedResumeMatcher()

@router.post("/advanced/calculate", response_model=List[Dict[str, Any]])
@performance_monitor.monitor_performance("advanced_matching_endpoint")
async def calculate_advanced_matches(
    request: MatchRequest = Body(...),
    db = Depends(get_db)
):
    """Calculate advanced matches between a job and resumes with semantic matching and bias detection"""
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
        
        # Calculate advanced matches
        match_results = advanced_matcher.rank_resumes_advanced(job, resumes)
        
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
            detail=f"Error calculating advanced matches: {str(e)}"
        )

@router.post("/semantic/skills")
@performance_monitor.monitor_performance("semantic_skills_endpoint")
async def semantic_skills_matching(
    request: Dict[str, Any] = Body(...)
):
    """Perform semantic skill matching between resume and job skills"""
    try:
        resume_skills = request.get("resume_skills", [])
        job_skills = request.get("job_skills", [])
        
        if not resume_skills or not job_skills:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Both resume_skills and job_skills are required"
            )
        
        result = advanced_matcher.semantic_skill_matching(resume_skills, job_skills)
        
        return {
            "matching_skills": result["matching_skills"],
            "missing_skills": result["missing_skills"],
            "skills_match_ratio": result["skills_match_ratio"],
            "semantic_matches": result["semantic_matches"]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in semantic skills matching: {str(e)}"
        )

@router.post("/bias/detect")
@performance_monitor.monitor_performance("bias_detection_endpoint")
async def detect_bias(
    request: Dict[str, Any] = Body(...)
):
    """Detect potential bias in text"""
    try:
        text = request.get("text", "")
        
        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text is required for bias detection"
            )
        
        bias_result = advanced_matcher.detect_bias(text)
        
        return {
            "bias_detected": bias_result["bias_detected"],
            "bias_score": bias_result["bias_score"],
            "bias_types": bias_result["bias_types"],
            "details": bias_result["details"]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in bias detection: {str(e)}"
        )

@router.get("/performance/summary")
async def get_performance_summary():
    """Get performance monitoring summary"""
    try:
        return performance_monitor.get_performance_summary()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting performance summary: {str(e)}"
        )

@router.get("/performance/function/{function_name}")
async def get_function_performance(function_name: str):
    """Get performance metrics for a specific function"""
    try:
        return performance_monitor.get_function_performance(function_name)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting function performance: {str(e)}"
        )

@router.post("/performance/clear-cache")
async def clear_performance_cache():
    """Clear the performance monitoring cache"""
    try:
        performance_monitor.clear_cache()
        return {"message": "Cache cleared successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing cache: {str(e)}"
        )

@router.get("/performance/export")
async def export_performance_metrics():
    """Export performance metrics to file"""
    try:
        filename = performance_monitor.export_metrics()
        return {
            "message": "Performance metrics exported successfully",
            "filename": filename
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting metrics: {str(e)}"
        ) 