from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, Base, IDMixin


class Document(Base, AuditMixin, IDMixin):
    __tablename__ = "document"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE"),
        nullable=False
    )

    file_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    file_path: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    file_type: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    project = relationship("Project",back_populates="documents")