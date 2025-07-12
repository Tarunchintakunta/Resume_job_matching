from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class Job(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    company: str
    description: str
    requirements: List[str] = []
    qualifications: List[str] = []
    skills_required: List[str] = []
    experience_required: Optional[int] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    salary_range: Optional[str] = None
    vector: Optional[List[float]] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)