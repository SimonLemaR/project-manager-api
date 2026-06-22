from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.project_member import ProjectMember


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_project(self, name: str, description: str | None) -> Project:
        new_project = Project(name=name, description=description)
        self.db.add(new_project)
        self.db.flush()
        return new_project

    def get_projects_by_user_id(
        self, user_id: int
    ) -> list[tuple[Project, ProjectMember]]:
        return (
            self.db.query(Project, ProjectMember)
            .join(ProjectMember, ProjectMember.project_id == Project.id)
            .filter(ProjectMember.user_id == user_id)
            .all()
        )

    def get_project_by_id(self, project_id: int) -> Project | None:
        return self.db.query(Project).filter(Project.id == project_id).first()

    def update_project(
        self, project: Project, name: str, description: str | None
    ) -> Project:
        project.name = name
        project.description = description
        self.db.add(project)
        return project

    def delete_project(self, project: Project) -> None:
        self.db.delete(project)
