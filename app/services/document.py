from fastapi import HTTPException, status

from app.models.document import Document
from app.models.user import User
from app.repositories.document import DocumentRepository
from app.repositories.project_member import ProjectMemberRepository


class DocumentService:
    def __init__(
        self,
        document_repo: DocumentRepository,
        project_member_repo: ProjectMemberRepository,
    ):
        self.document_repo = document_repo
        self.project_member_repo = project_member_repo  
          
    def get_document_for_download(
        self,
        document_id: int,
        current_user: User,
    ) -> Document:
        
        document = self.document_repo.get_document_by_id(document_id)


        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )

        project_member = self.project_member_repo.get_project_member(
            project_id=document.project_id,
            user_id=current_user.id,
        )

        if not project_member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="document not found",
            )

        return document