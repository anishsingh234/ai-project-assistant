from fastapi import APIRouter, HTTPException
from app.models.image import ImageGenerateRequest, ImageAnalyzeRequest, ImageResponse
from app.services.image_service import (
    generate_project_image,
    analyze_project_image,
    get_project_images
)
from app.db.repositories import project_repo

router = APIRouter()

@router.post("/{project_id}/images/generate", response_model=dict)
def generate_image(project_id: str, data: ImageGenerateRequest):
    project = project_repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = generate_project_image(project_id, data.prompt)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result

@router.post("/images/analyze", response_model=dict)
def analyze_image(data: ImageAnalyzeRequest):
    result = analyze_project_image(data.image_id, data.question)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result

@router.get("/{project_id}/images", response_model=list)
def list_images(project_id: str):
    return get_project_images(project_id)