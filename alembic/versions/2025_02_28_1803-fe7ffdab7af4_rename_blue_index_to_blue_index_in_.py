"""rename blue-index to blue_index in index_state table

Revision ID: fe7ffdab7af4
Revises: bc10ad1e9871
Create Date: 2025-02-28 18:03:42.056653+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe7ffdab7af4'
down_revision: Union[str, None] = 'bc10ad1e9871'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        'index_state',
        'blue-index',
        new_column_name='blue_index',
        existing_type=sa.String(),  # or sa.VARCHAR() if you prefer
        existing_nullable=True
    )


def downgrade():
    op.alter_column(
        'index_state',
        'blue_index',
        new_column_name='blue-index',
        existing_type=sa.String(),
        existing_nullable=True
    )
