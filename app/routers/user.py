from fastapi import APIRouter, status
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserRegister, UserResponse
from app.services.user import UserService
from app.core.database import get_db

user_router = APIRouter()


@user_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    new_user = user_service.create_user(user_data)
    return new_user
