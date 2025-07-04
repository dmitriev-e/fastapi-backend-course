"""rooms change number to str

Revision ID: 8dbe113b1f4c
Revises: ffebaa9e0b7d
Create Date: 2025-06-23 21:53:35.050202

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8dbe113b1f4c"
down_revision: Union[str, None] = "ffebaa9e0b7d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "rooms",
        "number",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=10),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "rooms",
        "number",
        existing_type=sa.String(length=10),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
