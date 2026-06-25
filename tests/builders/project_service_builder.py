from unittest.mock import Mock

from app.services.project import ProjectService


class ProjectServiceTestBuilder:
    def __init__(self):
        self.db = Mock()
        self.project_repo = Mock()
        self.project_member_repo = Mock()
        self.role_repo: Mock = Mock()
        self.document_repo = Mock()
        self.storage_service = Mock()
        self.user_repo = Mock()

        self.service = ProjectService(
            db=self.db,
            project_repo=self.project_repo,
            project_member_repo=self.project_member_repo,
            role_repo=self.role_repo,
            document_repo=self.document_repo,
            storage_service=self.storage_service,
            user_repo=self.user_repo,
        )

    def create_user(self):
        user = Mock()
        user.id = 1
        user.email = "test@test.com"
        return user

    def create_owner_role(self):
        role = Mock()
        role.id = 1
        role.name = "owner"
        return role

    def create_project(self):
        project = Mock()
        project.id = 10
        project.name = "testproject"
        project.description = "test description"
        return project
