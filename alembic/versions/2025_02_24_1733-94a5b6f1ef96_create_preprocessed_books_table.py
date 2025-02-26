"""create preprocessed books table

Revision ID: 94a5b6f1ef96
Revises: c75dee1b5d41
Create Date: 2025-02-24 17:33:46.240642+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94a5b6f1ef96'
down_revision: Union[str, None] = 'c75dee1b5d41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.create_table(
        'preprocessed_books_data',
        sa.Column('isbn13', sa.BigInteger(), primary_key=True, nullable=False),
        sa.Column('isbn10', sa.String(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('authors', sa.String(), nullable=True),
        sa.Column('categories', sa.String(), nullable=True),
        sa.Column('thumbnail', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('published_year', sa.Float(), nullable=True),
        sa.Column('average_rating', sa.Float(), nullable=True),
        sa.Column('num_pages', sa.Float(), nullable=True),
        sa.Column('ratings_count', sa.Float(), nullable=True),
        sa.Column('title_and_subtitle', sa.String(), nullable=True),
        sa.Column('simple_categories', sa.String(), nullable=True)
    )

def downgrade():
    op.drop_table('preprocessed_books_data')
