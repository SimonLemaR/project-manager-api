from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import LoginRequest, TokenResponse, UserRegister
from app.core.security import create_access_token, hash_password, verify_password


class UserService:
    def __init__(self, db: Session, user_repo: UserRepository):
        self.user_repo = user_repo
        self.db = db

    def create_user(self, user_data: UserRegister) -> User:
        # validar usuario existente
        existing_user = self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
            )

        password_hash = hash_password(user_data.password)

        # crear usuario
        new_user = self.user_repo.create_user(user_data, password_hash)
        self.db.commit()
        return new_user

    def login_user(self, data: LoginRequest):
        user = self.user_repo.get_user_by_email(data.email)

        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        access_token = create_access_token(data={"sub": user.email, "user_id": user.id})

        return TokenResponse(access_token=access_token)
