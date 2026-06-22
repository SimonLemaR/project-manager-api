from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str = Field(max_length=5000)


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class ProjectUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str = Field(max_length=5000)


class ProjectDeleteResponse(BaseModel):
    message: str
