from fastapi import APIRouter, status
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project import ProjectService
from app.core.database import get_db

project_router = APIRouter()

@project_router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    project_service = ProjectService(db)
    new_project = project_service.create_project(project_data)
    return new_project