from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import agents, chat
from app.api import images
from app.api import projects

app = FastAPI(
    title="AI Project Assistant",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(chat.router, prefix="/projects", tags=["Chat"])
app.include_router(images.router, prefix="/projects", tags=["Images"])
app.include_router(agents.router, prefix="/projects", tags=["Agents"])

@app.get("/")
def root():
    return {"message": "AI Project Assistant is running"}