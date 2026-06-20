from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from app.core.dependencies import get_current_user, get_document_service, get_project_service
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.services.document import DocumentService

document_router = APIRouter()

@document_router.get(
    "/{document_id}"
)
async def download_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service),
):
    
    document = document_service.get_document_by_id(document_id, current_user)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    return FileResponse(
        path=document.file_path,
        media_type="application/octet-stream",
        filename=document.file_name,
    )

@document_router.put(
    "/{document_id}",
    response_model=DocumentResponse,
)
async def update_document(
    document_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service),
):
    return document_service.update_document(
        document_id=document_id,
        file=file,
        current_user=current_user,
    )

@document_router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service),
):
    document_service.delete_document(
        document_id=document_id,
        current_user=current_user,
    )