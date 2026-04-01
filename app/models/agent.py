from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AgentRunResponse(BaseModel):
    id: str
    project_id: str
    status: str
    result: Optional[str]
    error: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
