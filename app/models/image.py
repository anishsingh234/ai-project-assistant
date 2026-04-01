from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ImageGenerateRequest(BaseModel):
    prompt: str

class ImageResponse(BaseModel):
    id: str
    project_id: str
    prompt: str
    url: str
    analysis_result: Optional[str]
    created_at: datetime

class ImageAnalyzeRequest(BaseModel):
    image_id: str
    question: Optional[str] = "Describe this image in detail"