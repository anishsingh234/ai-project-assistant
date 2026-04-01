from app.db.supabase_client import supabase

def save_memory(project_id: str, key: str, value: str):
    # upsert = insert or update if key already exists
    res = supabase.table("memory_entries").upsert({
        "project_id": project_id,
        "key": key,
        "value": value,
        "updated_at": "now()"
    }, on_conflict="project_id,key").execute()
    return res.data[0] if res.data else None

def get_memory(project_id: str, key: str):
    res = supabase.table("memory_entries").select("*").eq("project_id", project_id).eq("key", key).execute()
    return res.data[0] if res.data else None

def get_all_memory(project_id: str):
    res = supabase.table("memory_entries").select("*").eq("project_id", project_id).execute()
    return res.data

def delete_memory(project_id: str, key: str):
    res = supabase.table("memory_entries").delete().eq("project_id", project_id).eq("key", key).execute()
    return res.data