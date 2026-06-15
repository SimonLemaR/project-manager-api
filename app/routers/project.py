from fastapi import APIRouter, status
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_project_service
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectDetailResponse, ProjectResponse
from app.schemas.project_member import ProjectMemberDetailResponse
from app.services.project import ProjectService
from app.core.database import get_db

project_router = APIRouter()

@project_router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project_data: ProjectCreate, current_user: User = Depends(get_current_user),
                         project_service: ProjectService = Depends(get_project_service)):
    new_project = project_service.create_project(project_data, current_user)
    return new_project

@project_router.get("/", response_model=list[ProjectMemberDetailResponse], status_code=status.HTTP_200_OK)
async def get_user_projects(current_user: User = Depends(get_current_user),
                            project_service: ProjectService = Depends(get_project_service)):
    return project_service.get_user_projects(current_user)
