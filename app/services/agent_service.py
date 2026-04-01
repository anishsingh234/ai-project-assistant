from google import genai
from app.config import settings
from app.db.repositories import (
    agent_repo,
    image_repo,
    memory_repo
)
from app.db.repositories import message_repo
from app.db.repositories import project_repo

client = genai.Client(api_key=settings.gemini_api_key)

async def run_background_agent(run_id: str, project_id: str):
    agent_repo.update_agent_status(run_id, "running")
    try:
        project = project_repo.get_project(project_id)
        if not project:
            agent_repo.update_agent_status(run_id, "failed", error="Project not found")
            return

        conversations = message_repo.get_project_conversations(project_id)
        all_messages = []
        for conv in conversations:
            msgs = message_repo.get_conversation_messages(conv["id"])
            all_messages.extend(msgs)

        images = image_repo.get_project_images(project_id)
        existing_memory = memory_repo.get_all_memory(project_id)

        prompt = f"""
You are a project knowledge organizer. Analyze the following project data.

PROJECT BRIEF:
Title: {project.get('title')}
Description: {project.get('description')}
Goals: {project.get('goals')}
Tags: {project.get('tags')}
Reference Links: {project.get('reference_links')}
Status: {project.get('status')}

CONVERSATION HISTORY ({len(all_messages)} messages):
{_format_messages(all_messages)}

GENERATED IMAGES ({len(images)} total):
{_format_images(images)}

EXISTING MEMORY:
{_format_memory(existing_memory)}

Respond ONLY in this exact format, one per line:
KEY: value

Extract these keys:
- project_summary
- main_goals
- key_decisions
- image_themes
- progress_notes
- next_steps
- important_links
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        raw_text = response.text
        parsed = _parse_key_value(raw_text)

        for key, value in parsed.items():
            memory_repo.save_memory(project_id, key, value)

        agent_repo.update_agent_status(
            run_id, "completed",
            result=f"Organized {len(parsed)} memory entries successfully"
        )

    except Exception as e:
        agent_repo.update_agent_status(run_id, "failed", error=str(e))


def _format_messages(messages):
    if not messages:
        return "No messages yet"
    return "\n".join(f"{m['role'].upper()}: {m['content'][:200]}" for m in messages[-20:])

def _format_images(images):
    if not images:
        return "No images yet"
    return "\n".join(f"- {img['prompt']}" for img in images)

def _format_memory(memory):
    if not memory:
        return "No existing memory"
    return "\n".join(f"- {m['key']}: {m['value'][:100]}" for m in memory)

def _parse_key_value(text):
    result = {}
    for line in text.strip().split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip().lower().replace(" ", "_").replace("-","")
            value = value.strip()
            if key and value:
                result[key] = value
    return result