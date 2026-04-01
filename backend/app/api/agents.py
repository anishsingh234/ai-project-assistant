from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.agent_service import run_background_agent
from app.db.repositories import project_repo
from app.db.repositories import agent_repo

router = APIRouter()

@router.post("/{project_id}/run-agent", response_model=dict)
async def trigger_agent(project_id: str, background_tasks: BackgroundTasks):
    # Check project exists
    project = project_repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Create agent run record in DB with status: pending
    run = agent_repo.create_agent_run(project_id)
    if not run:
        raise HTTPException(status_code=400, detail="Failed to create agent run")

    # Trigger background task (non-blocking)
    background_tasks.add_task(
        run_background_agent,
        run_id=run["id"],
        project_id=project_id
    )

    return {
        "message": "Agent started",
        "run_id": run["id"],
        "status": "pending"
    }

@router.get("/agent-runs/{run_id}", response_model=dict)
def get_agent_status(run_id: str):
    run = agent_repo.get_agent_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Agent run not found")
    return run