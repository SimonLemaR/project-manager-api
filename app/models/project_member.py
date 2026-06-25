from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, Base, IDMixin


class ProjectMember(Base, AuditMixin, IDMixin):
    __tablename__ = "project_member"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE"), nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("role.id", ondelete="CASCADE"), nullable=False
    )

    project = relationship("Project", back_populates="members")

    user = relationship("User", back_populates="project_members")

    role = relationship(
        "Role",
    )

    __table_args__ = (UniqueConstraint("project_id", "user_id"),)
