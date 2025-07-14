from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status, Form, Path
from typing import List, Optional
from datetime import datetime
import json
import uuid
import traceback
import os

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

@router.post("/")
async def create_resume(
    file: UploadFile = File(...),
    db = Depends(get_db)
):
    """Upload and process a new resume"""
    try:
        # Read file content
        content = await file.read()
        
        # Store file name for better name extraction
        resume_parser.current_file_name = os.path.splitext(file.filename)[0]
        
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
        
        # Ensure all required fields are present with default values
        if "name" not in resume_data or not resume_data["name"] or resume_data["name"] == "Unknown":
            # Try to extract name from filename
            filename = os.path.splitext(file.filename)[0]
            name_from_file = filename.replace('_', ' ').replace('-', ' ')
            resume_data["name"] = name_from_file or "Unknown"
            
        if "education" not in resume_data or not resume_data["education"]:
            resume_data["education"] = []
            
        if "experience" not in resume_data or not resume_data["experience"]:
            resume_data["experience"] = []
            
        # Validate and fill missing fields in education entries
        for edu in resume_data.get("education", []):
            if "institution" not in edu or not edu["institution"]:
                edu["institution"] = "Unknown Institution"
            if "degree" not in edu or not edu["degree"]:
                edu["degree"] = "Unknown Degree"
        
        # Validate and fill missing fields in experience entries
        for exp in resume_data.get("experience", []):
            if "company" not in exp or not exp["company"]:
                exp["company"] = "Unknown Company"
            if "title" not in exp or not exp["title"]:
                exp["title"] = "Unknown Title"
        
        # Create resume object with validated data
        resume = {
            "id": str(uuid.uuid4()),
            "name": resume_data.get("name", "Unknown"),
            "email": resume_data.get("email"),
            "phone": resume_data.get("phone"),
            "summary": resume_data.get("summary", ""),
            "skills": resume_data.get("skills", []),
            "education": resume_data.get("education", []),
            "experience": resume_data.get("experience", []),
            "raw_text": resume_data.get("raw_text", ""),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # Vectorize resume text
        if resume["raw_text"]:
            try:
                vector = vectorizer.vectorize(resume["raw_text"])
                resume["vector"] = vector.tolist()
            except Exception as e:
                print(f"Error vectorizing resume: {str(e)}")
                resume["vector"] = []
        
        # Save to database
        db.resumes.insert_one(resume)
        
        # Clean up to help with memory usage
        if hasattr(resume_parser, 'current_file_name'):
            del resume_parser.current_file_name

        resume.pop('_id', None)  # Remove MongoDB's _id field if present
        return resume
    
    except Exception as e:
        print(f"Error processing resume: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing resume: {str(e)}"
        )

@router.get("/")
async def get_resumes(db = Depends(get_db)):
    """Get all resumes"""
    resumes = list(db.resumes.find())
    for resume in resumes:
        resume["id"] = str(resume.get("id", ""))
        resume.pop("_id", None)  # Remove MongoDB's _id field
    return resumes

@router.delete("/{resume_id}")
async def delete_resume(resume_id: str, db = Depends(get_db)):
    """Delete a resume by ID"""
    result = db.resumes.delete_one({"id": resume_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"message": "Resume deleted successfully"}