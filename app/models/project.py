from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import AuditMixin, Base, IDMixin


class Project(Base, AuditMixin, IDMixin):
    __tablename__ = "project"

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )