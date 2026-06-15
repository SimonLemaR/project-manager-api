from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserRegister


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user_data: UserRegister, password_hash: str) -> User:
        new_user = User(email=user_data.email, full_name=user_data.full_name, 
                        password_hash=password_hash)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user