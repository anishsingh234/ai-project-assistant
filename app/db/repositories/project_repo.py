from app.db.supabase_client import supabase

def create_project(data: dict):
    res = supabase.table("projects").insert(data).execute()
    return res.data[0] if res.data else None

def get_project(project_id: str):
    res = supabase.table("projects").select("*").eq("id", project_id).execute()
    return res.data[0] if res.data else None

def get_all_projects():
    res = supabase.table("projects").select("*").order("created_at", desc=True).execute()
    return res.data

def update_project(project_id: str, data: dict):
    res = supabase.table("projects").update(data).eq("id", project_id).execute()
    return res.data[0] if res.data else None

def delete_project(project_id: str):
    res = supabase.table("projects").delete().eq("id", project_id).execute()
    return res.data