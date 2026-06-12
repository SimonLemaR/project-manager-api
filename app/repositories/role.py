from sqlalchemy.orm import Session

from app.models.role import Role

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_role_by_name(self, role_name: str) -> Role:
        return self.db.query(Role).filter(Role.name == role_name).first()