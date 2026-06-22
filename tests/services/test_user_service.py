from unittest.mock import Mock, patch

from fastapi import HTTPException
import pytest

from app.repositories.user import UserRepository
from app.schemas.user import LoginRequest, UserRegister
from app.services.user import UserService


def test_create_user_success():
    # Arrange
    db = Mock()
    user_repo = Mock()

    user_data = UserRegister(
        email="test@test.com",
        full_name="Test User",
        password="Password123",
        repeat_password="Password123",
    )

    user_repo.get_user_by_email.return_value = None

    created_user = Mock()
    user_repo.create_user.return_value = created_user

    service = UserService(
        db=db,
        user_repo=user_repo,
    )

    # Act
    result = service.create_user(user_data)

    # Assert
    assert result == created_user

    user_repo.get_user_by_email.assert_called_once_with(user_data.email)

    user_repo.create_user.assert_called_once()

    db.commit.assert_called_once()


def test_create_user_user_already_exists():
    # Arrange
    db = Mock()
    user_repo = Mock()

    user_data = UserRegister(
        email="test@test.com",
        full_name="Test User",
        password="Password123",
        repeat_password="Password123",
    )

    existing_user = Mock()
    user_repo.get_user_by_email.return_value = existing_user
    service = UserService(
        db=db,
        user_repo=user_repo,
    )

    # Act
    with pytest.raises(HTTPException) as exc_info:
        service.create_user(user_data)

    # Assert
    assert exc_info.value.status_code == 409

    assert exc_info.value.detail == "Email already registered"

    user_repo.create_user.assert_not_called()

    db.commit.assert_not_called()


def test_login_user_success():
    db = Mock()
    user_repo = Mock(spec=UserRepository)

    login_data = LoginRequest(
        email="test@test.com",
        password="Password123",
    )

    user = Mock()
    user.id = 1
    user.email = "test@test.com"
    user.password_hash = "hashed_password"

    user_repo.get_user_by_email.return_value = user

    service = UserService(
        db=db,
        user_repo=user_repo,
    )

    with (
        patch("app.services.user.verify_password") as mock_verify_password,
        patch("app.services.user.create_access_token") as mock_create_access_token,
    ):
        mock_verify_password.return_value = True
        mock_create_access_token.return_value = "fake_jwt"

        # Act
        result = service.login_user(login_data)

    # Assert
    assert result.access_token == "fake_jwt"

    user_repo.get_user_by_email.assert_called_once_with(login_data.email)

    mock_verify_password.assert_called_once_with(
        login_data.password,
        user.password_hash,
    )

    mock_create_access_token.assert_called_once_with(
        data={
            "sub": user.email,
            "user_id": user.id,
        }
    )


def test_login_user_wrong_password():
    db = Mock()
    user_repo = Mock(spec=UserRepository)

    login_data = LoginRequest(
        email="test@test.com",
        password="Password123",
    )

    user = Mock()
    user.id = 1
    user.email = "test@test.com"
    user.password_hash = "hashed_password"

    user_repo.get_user_by_email.return_value = user

    service = UserService(
        db=db,
        user_repo=user_repo,
    )

    with (
        patch("app.services.user.verify_password") as mock_verify_password,
        patch("app.services.user.create_access_token") as mock_create_access_token,
    ):
        mock_verify_password.return_value = False
        mock_create_access_token.return_value = "fake_jwt"

        # Act
        with pytest.raises(HTTPException) as exc_info:
            service.login_user(login_data)

    # Assert
    assert exc_info.value.status_code == 401

    assert exc_info.value.detail == "Invalid email or password"

    mock_create_access_token.assert_not_called()
