from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    id: int
    file_name: str
    file_path: str
    file_type: str

    model_config = ConfigDict(from_attributes=True)


class FailedUploadResponse(BaseModel):
    file_name: str
    error: str


class UploadDocumentsResponse(BaseModel):
    uploaded: list[DocumentResponse]
    failed: list[FailedUploadResponse]

class DocumentDeleteResponse(BaseModel):
    message : str