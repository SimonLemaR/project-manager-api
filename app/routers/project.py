from fastapi import APIRouter, File, UploadFile, status
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_project_service
from app.models.user import User
from app.schemas.document import UploadDocumentsResponse
from app.schemas.project import ProjectCreate, ProjectResponse
from app.schemas.project_member import ProjectMemberDetailResponse
from app.services.project.project import ProjectService
from app.core.database import get_db

project_router = APIRouter()


@project_router.post(
    "/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED
)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
):
    new_project = project_service.create_project(project_data, current_user)
    return new_project


@project_router.get(
    "/",
    response_model=list[ProjectMemberDetailResponse],
    status_code=status.HTTP_200_OK,
)
async def get_user_projects(
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
):
    return project_service.get_user_projects(current_user)


@project_router.get(
    "/{project_id}", response_model=ProjectMemberDetailResponse, status_code=status.HTTP_200_OK
)
async def get_project_by_id(
    project_id: int,
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
):
    project = project_service.get_project_by_id(project_id, current_user)
    return project

@project_router.put(
    "/{project_id}", response_model=ProjectResponse, status_code=status.HTTP_200_OK
)
async def update_project(
    project_id: int,
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
):
    updated_project = project_service.update_project(project_id, project_data, current_user)
    return updated_project

@project_router.delete(
    "/{project_id}", status_code=status.HTTP_200_OK
)
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
):
    project_service.delete_project(project_id, current_user)
    return {"message": "Project deleted successfully"}

@project_router.post(
    "/{project_id}/documents",
    response_model=UploadDocumentsResponse,
)
async def upload_documents(
    project_id: int,
    files: list[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
):
    return project_service.upload_documents(
        project_id=project_id,
        files=files,
        current_user=current_user,
    )