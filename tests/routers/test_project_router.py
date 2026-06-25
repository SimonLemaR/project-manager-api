from fastapi.testclient import TestClient
from unittest.mock import Mock

from app.main import app
from app.core.dependencies import (
    get_current_user,
    get_project_service,
)
from tests.builders.project_service_builder import ProjectServiceTestBuilder

client = TestClient(app)


def test_create_project_success():
    # Arrange
    builder = ProjectServiceTestBuilder()

    mock_user = builder.create_user()
    mock_user.id = 1

    mock_service = Mock()

    created_project = builder.create_project()

    mock_service.create_project.return_value = created_project
    app.dependency_overrides[get_current_user] = lambda: mock_user

    app.dependency_overrides[get_project_service] = lambda: mock_service

    # Act
    response = client.post(
        "/api/v1/projects",
        json={
            "name": "Test Project",
            "description": "Test Description",
        },
    )

    # Assert
    assert response.status_code == 201
    mock_service.create_project.assert_called_once()

    app.dependency_overrides.clear()
