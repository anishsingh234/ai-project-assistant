from app.db.supabase_client import supabase
from datetime import datetime, timezone

def create_agent_run(project_id: str):
    res = supabase.table("agent_runs").insert({
        "project_id": project_id,
        "status": "pending"
    }).execute()
    return res.data[0] if res.data else None

def get_agent_run(run_id: str):
    res = supabase.table("agent_runs").select("*").eq("id", run_id).execute()
    return res.data[0] if res.data else None

def update_agent_status(run_id: str, status: str, result: str = None, error: str = None):
    data = {"status": status}
    if status == "running":
        data["started_at"] = datetime.now(timezone.utc).isoformat()
    if status in ("completed", "failed"):
        data["completed_at"] = datetime.now(timezone.utc).isoformat()
    if result:
        data["result"] = result
    if error:
        data["error"] = error

    res = supabase.table("agent_runs").update(data).eq("id", run_id).execute()
    return res.data[0] if res.data else None
