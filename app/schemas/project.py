from pydantic import BaseModel, ConfigDict

from app.schemas.document import DocumentResponse
from app.schemas.role import RoleResponse
from app.schemas.user import UserResponse


class ProjectCreate(BaseModel):
    name: str
    description: str

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)

class ProjectUpdate(BaseModel):
    name: str
    description: str

class ProjectDeleteResponse(BaseModel):
    message: str