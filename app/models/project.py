from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    goals: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    reference_links: Optional[List[str]] = []

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    goals: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    reference_links: Optional[List[str]] = None
    status: Optional[str] = None

class ProjectResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    goals: Optional[List[str]]
    tags: Optional[List[str]]
    reference_links: Optional[List[str]]
    status: str
    created_at: datetime
    updated_at: datetime