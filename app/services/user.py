from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserRegister
from app.core.security import hash_password

class UserService():
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def create_user(self, user_data: UserRegister) -> User:
        # validar usuario existente
        existing_user = self.user_repo.get_user_by_email(user_data.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
)
        
        password_hash = hash_password(user_data.password)

        # crear usuario
        new_user =self.user_repo.create_user(user_data, password_hash)
        return new_user
    
    