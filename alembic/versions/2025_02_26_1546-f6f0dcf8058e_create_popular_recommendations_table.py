"""create popular_recommendations table

Revision ID: f6f0dcf8058e
Revises: 15e9a79af6d2
Create Date: 2025-02-26 15:46:27.756159+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6f0dcf8058e'
down_revision: Union[str, None] = '15e9a79af6d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'popular_recommendations',
        sa.Column('isbn13', sa.BigInteger(), primary_key=True, nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('average_rating', sa.Float(), nullable=True),
        sa.Column('ratings_count', sa.Float(), nullable=True)
    )


def downgrade():
    op.drop_table('popular_recommendations')