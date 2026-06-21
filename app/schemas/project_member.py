from pydantic import BaseModel, ConfigDict

from app.schemas.project import ProjectResponse
from app.schemas.role import RoleResponse
from app.schemas.user import UserResponse


class ProjectMemberDetailResponse(BaseModel):
    project: ProjectResponse
    user: UserResponse
    role: RoleResponse

    model_config = ConfigDict(from_attributes=True)