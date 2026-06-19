from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.core.storage.local import LocalStorageStrategy
from app.repositories.document import DocumentRepository
from app.repositories.project import ProjectRepository
from app.repositories.project_member import ProjectMemberRepository
from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository
from app.services.project import ProjectService
from app.services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        user_repo = UserRepository(db)
        user = user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return user


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    project_repo = ProjectRepository(db)
    project_member_repo = ProjectMemberRepository(db)
    role_repo = RoleRepository(db)
    document_repo = DocumentRepository(db)
    if settings.STORAGE_PROVIDER == "local":
        storage_strategy = LocalStorageStrategy()
    return ProjectService(
        db,
        project_repo,
        project_member_repo,
        role_repo,
        document_repo,
        storage_strategy,
    )


def get_user_service(db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    return UserService(db, user_repo)
