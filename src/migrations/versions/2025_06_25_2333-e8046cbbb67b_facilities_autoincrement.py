"""facilities autoincrement

Revision ID: e8046cbbb67b
Revises: 35fdb3e14d14
Create Date: 2025-06-25 23:33:35.311959

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e8046cbbb67b"
down_revision: Union[str, None] = "35fdb3e14d14"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "facilities", "description", existing_type=sa.VARCHAR(length=255), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "facilities",
        "description",
        existing_type=sa.VARCHAR(length=255),
        nullable=False,
    )
    # ### end Alembic commands ###
