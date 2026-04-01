from app.db.supabase_client import supabase

def save_image(project_id: str, prompt: str, url: str):
    res = supabase.table("images").insert({
        "project_id": project_id,
        "prompt": prompt,
        "url": url
    }).execute()
    return res.data[0] if res.data else None

def get_image(image_id: str):
    res = supabase.table("images").select("*").eq("id", image_id).execute()
    return res.data[0] if res.data else None

def get_project_images(project_id: str):
    res = supabase.table("images").select("*").eq("project_id", project_id).order("created_at", desc=True).execute()
    return res.data

def update_image_analysis(image_id: str, analysis: str):
    res = supabase.table("images").update({
        "analysis_result": analysis
    }).eq("id", image_id).execute()
    return res.data[0] if res.data else None