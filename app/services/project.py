from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.storage.base import StorageStrategy
from app.core.storage.local import LocalStorageStrategy
from app.models.document import Document
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.user import User
from app.repositories.project import ProjectRepository
from app.repositories.project_member import ProjectMemberRepository
from app.repositories.role import RoleRepository
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.schemas.role import RoleResponse
from app.schemas.user import UserResponse
from app.repositories.document import DocumentRepository


class ProjectService:
    def __init__(
        self,
        db: Session,
        project_repo: ProjectRepository,
        project_member_repo: ProjectMemberRepository,
        role_repo: RoleRepository,
        document_repo: DocumentRepository,
        storage_service: StorageStrategy,
    ):
        self.db = db
        self.project_repo = project_repo
        self.project_member_repo = project_member_repo
        self.role_repo = role_repo
        self.document_repo = document_repo
        self.storage_service = storage_service

    def create_project(
        self, project_data: ProjectCreate, current_user: User
    ) -> Project:
        owner_role = self.role_repo.get_role_by_name("owner")
        try:
            project = self.project_repo.create_project(
                name=project_data.name, description=project_data.description
            )
            self.project_member_repo.create_project_member(
                project_id=project.id, user_id=current_user.id, role_id=owner_role.id
            )
            self.db.commit()
            return project

        except Exception:
            self.db.rollback()
            raise

    def get_user_projects(self, current_user: User) -> list[ProjectMember]:
        projects_member_data = self.project_member_repo.get_project_members_by_user_id(
            current_user.id
        )
        return projects_member_data

    def get_project_by_id(self, project_id: int, current_user: User) -> Project | None:
        project_member = self.project_member_repo.get_project_member(
            project_id=project_id, user_id=current_user.id
        )
        if not project_member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
            )

        return project_member

    def update_project(
        self, project_id: int, project_data: ProjectUpdate, current_user: User
    ) -> Project:
        project_member = self.project_member_repo.get_project_member(
            project_id=project_id, user_id=current_user.id
        )
        if not project_member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
            )

        updated_project = self.project_repo.update_project(
            project=project_member.project,
            name=project_data.name,
            description=project_data.description,
        )
        self.db.commit()
        return updated_project

    def delete_project(
        self,
        project_id: int,
        current_user: User,
    ) -> None:
        project_member = self.project_member_repo.get_project_member(
            project_id=project_id, user_id=current_user.id, role_name="owner"
        )
        if not project_member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
            )
        self.project_repo.delete_project(project_member.project)
        self.db.commit()

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

    def get_project_documents(
        self,
        project_id: int,
        current_user: User,
    ) -> list[Document]:

        project_member = self.project_member_repo.get_project_member(
            project_id=project_id,
            user_id=current_user.id,
        )

        if not project_member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        return self.document_repo.get_documents_by_project_id(project_id)