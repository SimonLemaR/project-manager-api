from fastapi import APIRouter, status
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_project_service
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project import ProjectService
from app.core.database import get_db

project_router = APIRouter()

@project_router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project_data: ProjectCreate, current_user: User = Depends(get_current_user),
                         project_service: ProjectService = Depends(get_project_service)):
    new_project = project_service.create_project(project_data, current_user)
    return new_project
