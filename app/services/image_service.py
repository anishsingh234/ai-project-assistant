from app.tools.image_tools import generate_image, analyze_image
from app.db.repositories import image_repo

def generate_project_image(project_id: str, prompt: str):
    return generate_image(project_id, prompt)

def analyze_project_image(image_id: str, question: str):
    return analyze_image(image_id, question)

def get_project_images(project_id: str):
    return image_repo.get_project_images(project_id)