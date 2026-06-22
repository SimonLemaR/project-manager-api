from unittest.mock import Mock

from fastapi import HTTPException
import pytest

from app.schemas.project import ProjectCreate
from app.services.project import ProjectService
from tests.builders.project_service_builder import ProjectServiceTestBuilder


def test_create_project_success():
    # Arrange
    builder = ProjectServiceTestBuilder()
    user = builder.create_user()
    role = builder.create_owner_role()
    builder.role_repo.get_role_by_name.return_value = role

    created_project = builder.create_project()

    builder.project_repo.create_project.return_value = created_project

    result = builder.service.create_project(
        ProjectCreate(
            name="test project",
            description="test description",
        ),
        user,
    )

    # Assert
    assert result == created_project

    builder.role_repo.get_role_by_name.assert_called_once_with("owner")

    builder.project_repo.create_project.assert_called_once_with(
        name="test project", description="test description"
    )

    builder.project_member_repo.create_project_member.assert_called_once_with(
        project_id=created_project.id, user_id=user.id, role_id=role.id
    )

    builder.db.commit.assert_called_once()


def test_create_project_rollback_on_exception():
    # Arrange
    db = Mock()
    project_repo = Mock()
    project_member_repo = Mock()
    role_repo = Mock()
    document_repo = Mock()
    storage_service = Mock()
    user_repo = Mock()

    project_data = ProjectCreate(
        name="testproject", description="test project description"
    )

    role = Mock()
    role.id = 1
    role.name = "owner"

    role_repo.get_role_by_name.return_value = role

    project_repo.create_project.side_effect = Exception("Database Error")

    service = ProjectService(
        db=db,
        project_repo=project_repo,
        project_member_repo=project_member_repo,
        role_repo=role_repo,
        document_repo=document_repo,
        storage_service=storage_service,
        user_repo=user_repo,
    )

    user = Mock()
    user.id = 1

    # Act
    with pytest.raises(Exception):
        service.create_project(project_data, user)

    # Assert
    db.rollback.assert_called_once()

    db.commit.assert_not_called()


def test_get_user_projects_success():
    # Arrange
    builder = ProjectServiceTestBuilder()

    user = builder.create_user()

    projects = [
        Mock(),
        Mock(),
    ]

    builder.project_member_repo.get_project_members_by_user_id.return_value = projects

    # Act
    result = builder.service.get_user_projects(user)

    # Assert
    assert result == projects

    builder.project_member_repo.get_project_members_by_user_id.assert_called_once_with(
        user.id
    )


def test_get_project_by_id_success():
    # Arrange
    builder = ProjectServiceTestBuilder()

    user = builder.create_user()

    project = builder.create_project()

    project_member = Mock()
    project_member.project = project

    builder.project_member_repo.get_project_member.return_value = project_member

    # Act
    result = builder.service.get_project_by_id(
        project_id=project.id,
        current_user=user,
    )

    # Assert
    assert result == project_member

    builder.project_member_repo.get_project_member.assert_called_once_with(
        project_id=project.id,
        user_id=user.id,
    )


def test_get_project_by_id_not_found():
    # Arrange
    builder = ProjectServiceTestBuilder()

    user = builder.create_user()

    builder.project_member_repo.get_project_member.return_value = None

    # Act
    with pytest.raises(HTTPException) as exc_info:
        builder.service.get_project_by_id(
            project_id=1,
            current_user=user,
        )
    # Assert
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Project not found"

    builder.project_member_repo.get_project_member.assert_called_once_with(
        project_id=1,
        user_id=user.id,
    )
