from fastapi import FastAPI
from app.routers.user import user_router
from app.routers.project import project_router
from app.routers.document import document_router

from app.models.user import User
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.document import Document
from app.models.role import Role

app = FastAPI()


@app.get("/")
def root():
    return {"message": "API running"}

app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(project_router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(document_router, prefix="/api/v1/documents", tags=["Documents"])