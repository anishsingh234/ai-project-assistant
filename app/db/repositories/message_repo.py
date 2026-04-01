from app.db.supabase_client import supabase

def create_conversation(project_id: str, title: str = "New Conversation"):
    res = supabase.table("conversations").insert({
        "project_id": project_id,
        "title": title
    }).execute()
    return res.data[0] if res.data else None

def get_conversation(conversation_id: str):
    res = supabase.table("conversations").select("*").eq("id", conversation_id).execute()
    return res.data[0] if res.data else None

def get_project_conversations(project_id: str):
    res = supabase.table("conversations").select("*").eq("project_id", project_id).order("created_at", desc=True).execute()
    return res.data

def save_message(conversation_id: str, role: str, content: str, tool_calls: dict = None):
    res = supabase.table("messages").insert({
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
        "tool_calls": tool_calls
    }).execute()
    return res.data[0] if res.data else None

def get_conversation_messages(conversation_id: str):
    res = supabase.table("messages").select("*").eq("conversation_id", conversation_id).order("created_at").execute()
    return res.data