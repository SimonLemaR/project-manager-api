from sqlalchemy.orm import Session

from app.models.project_member import ProjectMember


class ProjectMemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_project_member(self, project_id: int, user_id: int,role_id: int) -> ProjectMember:
        project_member = ProjectMember(project_id=project_id, user_id=user_id, role_id=role_id)

        self.db.add(project_member)

        return project_member