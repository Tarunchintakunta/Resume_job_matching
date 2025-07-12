from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
import uuid

class MatchRequest(BaseModel):
    job_id: str
    resume_ids: Optional[List[str]] = None  # If None, match all resumes

class MatchDetail(BaseModel):
    vector_similarity: float
    skills_match_ratio: float
    matching_skills: List[str]
    missing_skills: List[str]

class MatchResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    job_id: str
    resume_id: str
    score: float
    details: MatchDetail
    rank: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.now)