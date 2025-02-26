"""add sentiment analysis columns, tagged_description column and create index_state table

Revision ID: 15e9a79af6d2
Revises: 94a5b6f1ef96
Create Date: 2025-02-26 05:34:02.133669+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15e9a79af6d2'
down_revision: Union[str, None] = '94a5b6f1ef96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add sentiment analysis columns and tagged_description to preprocessed_books_data table
    op.add_column('preprocessed_books_data', sa.Column('anger', sa.Float(), nullable=True))
    op.add_column('preprocessed_books_data', sa.Column('disgust', sa.Float(), nullable=True))
    op.add_column('preprocessed_books_data', sa.Column('fear', sa.Float(), nullable=True))
    op.add_column('preprocessed_books_data', sa.Column('joy', sa.Float(), nullable=True))
    op.add_column('preprocessed_books_data', sa.Column('sadness', sa.Float(), nullable=True))
    op.add_column('preprocessed_books_data', sa.Column('surprise', sa.Float(), nullable=True))
    op.add_column('preprocessed_books_data', sa.Column('neutral', sa.Float(), nullable=True))
    op.add_column('preprocessed_books_data', sa.Column('tagged_description', sa.String(), nullable=True))

    # Create the index_state table with blue-index, green_index, and query_index columns.
    # Note: Because SQL identifiers cannot normally include dashes without quoting,
    # we are using the column name 'blue-index' exactly as specified.
    op.create_table(
        'index_state',
        sa.Column('blue-index', sa.String(), nullable=True),
        sa.Column('green_index', sa.String(), nullable=True),
        sa.Column('query_index', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('query_index')
    )


def downgrade():
    # Drop the index_state table
    op.drop_table('index_state')

    # Remove the added columns from preprocessed_books_data table
    op.drop_column('preprocessed_books_data', 'tagged_description')
    op.drop_column('preprocessed_books_data', 'neutral')
    op.drop_column('preprocessed_books_data', 'surprise')
    op.drop_column('preprocessed_books_data', 'sadness')
    op.drop_column('preprocessed_books_data', 'joy')
    op.drop_column('preprocessed_books_data', 'fear')
    op.drop_column('preprocessed_books_data', 'disgust')
    op.drop_column('preprocessed_books_data', 'anger')