from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str
    description: str

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)
