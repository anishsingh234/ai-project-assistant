from app.db.repositories import project_repo
from app.db.repositories import image_repo

def get_project_brief(project_id: str) -> dict:
    """Get the full brief of a project including title, description, goals and links"""
    project = project_repo.get_project(project_id)
    if not project:
        return {"error": "Project not found"}
    return project

def list_project_images(project_id: str) -> dict:
    """List all images generated for a project"""
    images = image_repo.get_project_images(project_id)
    return {"images": images, "count": len(images)}