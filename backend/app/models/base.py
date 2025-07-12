from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class MongoBaseModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)