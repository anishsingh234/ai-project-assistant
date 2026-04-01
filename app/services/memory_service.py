from app.db.repositories import memory_repo

def save_project_memory(project_id: str, key: str, value: str):
    return memory_repo.save_memory(project_id, key, value)

def get_project_memory(project_id: str):
    return memory_repo.get_all_memory(project_id)

def delete_project_memory(project_id: str, key: str):
    return memory_repo.delete_memory(project_id, key)