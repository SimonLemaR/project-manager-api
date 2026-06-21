from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.storage.local import LocalStorageStrategy
from app.models.document import Document
from app.models.user import User
from app.repositories.document import DocumentRepository
from app.repositories.project_member import ProjectMemberRepository
from app.repositories.role import RoleRepository


class DocumentService:

    ALLOWED_EXTENSIONS = {".pdf",".docx",}
    ALLOWED_CONTENT_TYPES = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    def __init__(
        self,
        document_repo: DocumentRepository,
        project_member_repo: ProjectMemberRepository,
        storage_service: LocalStorageStrategy,
        db: Session,
    ):
        self.document_repo = document_repo
        self.project_member_repo = project_member_repo
        self.storage_service = storage_service
        self.db = db

    def upload_documents(
        self,
        project_id: int,
        files: list[UploadFile],
        current_user: User,
    ):
        project_member = self.project_member_repo.get_project_member(
            project_id=project_id, user_id=current_user.id
        )
        if not project_member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
            )

        uploaded_documents = []
        failed_uploads = []

        for file in files:

            self._validate_file(file)

            try:

                file_path = self.storage_service.save_file(
                    project_id=project_id,
                    file=file,
                )

                document = self.document_repo.create_document(
                    project_id=project_id,
                    file_name=file.filename,
                    file_path=file_path,
                    file_type=file.content_type,
                )

                uploaded_documents.append(document)

            except Exception as e:

                failed_uploads.append(
                    {
                        "file_name": file.filename,
                        "error": str(e),
                    }
                )

        self.db.commit()
        return {"uploaded": uploaded_documents, "failed": failed_uploads}
        
    def get_document_by_id(
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

    def update_document(
        self,
        document_id: int,
        file: UploadFile,
        current_user: User,
    ) -> Document:
        document = self.get_document_by_id(document_id, current_user)
        self._validate_file(file)
        old_file_path = document.file_path
        new_file_path = self.storage_service.save_file(
            project_id=document.project_id,
            file=file,
        )
        document.file_name = file.filename
        document.file_path = new_file_path
        document.file_type = file.content_type
        self.db.commit()
        self.db.refresh(document)
        Path(old_file_path).unlink(missing_ok=True)
        return document

    def delete_document(
        self,
        document_id: int,
        current_user: User,
    ) -> None:
        document = self.get_document_by_id(document_id, current_user)
        self.document_repo.delete_document(document)
        self.db.commit()
        self.storage_service.delete_file(document.file_path)

    def _validate_file(self, file: UploadFile) -> None:
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File name is required",
            )
        extension = Path(file.filename).suffix.lower()

        if (
            extension not in self.ALLOWED_EXTENSIONS
            or file.content_type not in self.ALLOWED_CONTENT_TYPES
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF and DOCX files are allowed",
            ) 