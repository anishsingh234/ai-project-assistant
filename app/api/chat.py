from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.services.gemini_service import run_chat
from app.db.repositories import project_repo
from app.db.repositories import message_repo

router = APIRouter()

@router.post("/{project_id}/chat", response_model=ChatResponse)
def chat(project_id: str, data: ChatRequest):
    # Check project exists
    project = project_repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Create new conversation if not provided
    if not data.conversation_id:
        conversation = message_repo.create_conversation(project_id)
        conversation_id = conversation["id"]
    else:
        conversation_id = data.conversation_id

    # Save user message to DB
    message_repo.save_message(
        conversation_id=conversation_id,
        role="user",
        content=data.message
    )

    # Run Gemini chat with tool loop
    reply = run_chat(
        project_id=project_id,
        conversation_id=conversation_id,
        user_message=data.message
    )

    # Save assistant reply to DB
    message_repo.save_message(
        conversation_id=conversation_id,
        role="assistant",
        content=reply
    )

    return ChatResponse(
        conversation_id=conversation_id,
        reply=reply
    )

@router.get("/{project_id}/conversations")
def get_conversations(project_id: str):
    return message_repo.get_project_conversations(project_id)

@router.get("/{project_id}/conversations/{conversation_id}/messages")
def get_messages(project_id: str, conversation_id: str):
    return message_repo.get_conversation_messages(conversation_id)