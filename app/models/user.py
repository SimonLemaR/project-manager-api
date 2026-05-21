import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import AuditMixin, Base, IDMixin


class User(Base, AuditMixin, IDMixin):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    full_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )