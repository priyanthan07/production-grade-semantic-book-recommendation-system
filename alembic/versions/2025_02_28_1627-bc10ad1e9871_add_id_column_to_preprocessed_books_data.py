"""add id column to preprocessed_books_data

Revision ID: bc10ad1e9871
Revises: eccb0d0bc2a9
Create Date: 2025-02-28 16:27:20.571713+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc10ad1e9871'
down_revision: Union[str, None] = 'eccb0d0bc2a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'preprocessed_books_data',
        sa.Column('id', sa.Integer(), nullable=True)
    )


def downgrade():
    op.drop_column('preprocessed_books_data', 'id')
