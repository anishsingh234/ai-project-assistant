from fastapi import APIRouter, HTTPException
from app.models.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.db.repositories import project_repo

router = APIRouter()

@router.post("/", response_model=dict)
def create_project(data: ProjectCreate):
    project = project_repo.create_project(data.model_dump())
    if not project:
        raise HTTPException(status_code=400, detail="Failed to create project")
    return project

@router.get("/", response_model=list)
def list_projects():
    return project_repo.get_all_projects()

@router.get("/{project_id}", response_model=dict)
def get_project(project_id: str):
    project = project_repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=dict)
def update_project(project_id: str, data: ProjectUpdate):
    updated = project_repo.update_project(
        project_id,
        {k: v for k, v in data.model_dump().items() if v is not None}
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated

@router.delete("/{project_id}")
def delete_project(project_id: str):
    project_repo.delete_project(project_id)
    return {"message": "Project deleted successfully"}