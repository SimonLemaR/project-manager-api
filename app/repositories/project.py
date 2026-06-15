from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_project(self, name: str, description: str | None) -> Project:
        new_project = Project(name=name, description=description)
        self.db.add(new_project)
        self.db.flush()
        return new_project
        