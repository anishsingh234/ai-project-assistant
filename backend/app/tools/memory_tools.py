from app.db.repositories import memory_repo

def search_memory(project_id: str, key: str) -> dict:
    """Search for a specific memory entry by key for a project"""
    entry = memory_repo.get_memory(project_id, key)
    if not entry:
        return {"found": False, "key": key, "value": None}
    return {"found": True, "key": key, "value": entry["value"]}

def get_all_memory(project_id: str) -> dict:
    """Get all memory entries stored for a project"""
    entries = memory_repo.get_all_memory(project_id)
    return {"memories": entries, "count": len(entries)}

def save_to_memory(project_id: str, key: str, value: str) -> dict:
    """Save or update a memory entry for a project"""
    result = memory_repo.save_memory(project_id, key, value)
    if result:
        return {"success": True, "key": key, "value": value}
    return {"success": False, "error": "Failed to save memory"}