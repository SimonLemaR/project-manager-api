"""seed default roles

Revision ID: ebf1b81e9044
Revises: 14a7244eef7f
Create Date: 2026-06-12 04:40:06.264812

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "ebf1b81e9044"
down_revision: Union[str, Sequence[str], None] = "14a7244eef7f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO role (name)
        VALUES
            ('owner'),
            ('participant')
        ON CONFLICT (name) DO NOTHING;
        """
    )


def downgrade() -> None:
    raise NotImplementedError("Default system roles should not be removed.")
