from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
import json

from app.core.database import get_db
from app.models.resume import Resume
from app.services.resume_parser import ResumeParser
from app.services.vectorizer import ResumeJobVectorizer
from app.services.text_processor import TextProcessor

router = APIRouter()

# Initialize services
# Note: In production, you would load this from a database
with open("data/skills_database.json", "r") as f:
    skills_database = json.load(f)

resume_parser = ResumeParser(skills_database)
vectorizer = ResumeJobVectorizer("models/tfidf_vectorizer.pkl")
text_processor = TextProcessor()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Resume)
async def create_resume(
    file: UploadFile = File(...),
    db = Depends(get_db)
):
    """Upload and process a new resume"""
    try:
        # Read file content
        content = await file.read()
        
        # Parse resume based on file type
        if file.filename.endswith(".pdf"):
            resume_data = resume_parser.parse_pdf(content)
        elif file.filename.endswith(".json"):
            resume_data = resume_parser.parse_json(content)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file format. Please upload PDF or JSON."
            )
        
        # Create resume object
        resume = Resume(
            name=resume_data.get("name", "Unknown"),
            email=resume_data.get("email"),
            phone=resume_data.get("phone"),
            summary=resume_data.get("summary"),
            skills=resume_data.get("skills", []),
            education=resume_data.get("education", []),
            experience=resume_data.get("experience", []),
            raw_text=resume_data.get("raw_text", "")
        )
        
        # Vectorize resume text
        if resume.raw_text:
            vector = vectorizer.vectorize(resume.raw_text)
            resume.vector = vector.tolist()
        
        # Save to database
        resume_dict = resume.dict()
        db.resumes.insert_one(resume_dict)
        
        return resume
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing resume: {str(e)}"
        )

@router.get("/", response_model=List[Resume])
async def get_resumes(
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_db)
):
    """Get list of resumes"""
    resumes = list(db.resumes.find().skip(skip).limit(limit))
    return resumes

@router.get("/{resume_id}", response_model=Resume)
async def get_resume(
    resume_id: str,
    db = Depends(get_db)
):
    """Get a specific resume by ID"""
    resume = db.resumes.find_one({"id": resume_id})
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    return resume

@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: str,
    db = Depends(get_db)
):
    """Delete a resume"""
    result = db.resumes.delete_one({"id": resume_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    return None