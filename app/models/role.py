from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import AuditMixin, Base, IDMixin


class Role(Base, AuditMixin, IDMixin):
    __tablename__ = "role"

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )