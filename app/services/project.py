from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.user import User
from app.repositories.project import ProjectRepository
from app.repositories.project_member import ProjectMemberRepository
from app.repositories.role import RoleRepository
from app.schemas.project import ProjectCreate
from app.schemas.role import RoleResponse
from app.schemas.user import UserResponse


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.project_repo = ProjectRepository(db)
        self.project_member_repo = ProjectMemberRepository(db)
        self.role_repo = RoleRepository(db)

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
        projects_member_data = self.project_member_repo.get_project_members_by_user_id(current_user.id)
        return projects_member_data