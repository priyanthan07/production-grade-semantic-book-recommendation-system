"""add id column to books

Revision ID: eccb0d0bc2a9
Revises: f6f0dcf8058e
Create Date: 2025-02-26 17:17:47.580636+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eccb0d0bc2a9'
down_revision: Union[str, None] = 'f6f0dcf8058e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1) Create a sequence for the auto-increment behavior (PostgreSQL).
    op.execute("CREATE SEQUENCE IF NOT EXISTS books_id_seq")

    # 2) Add the new 'id' column as nullable initially but with a server default
    #    so existing rows receive a value. Using 'nextval(...)' references the sequence.
    op.add_column(
        'books',
        sa.Column(
            'id',
            sa.BigInteger(),
            server_default=sa.text("nextval('books_id_seq'::regclass)"),
            nullable=True
        )
    )

    # 3) Make the column NOT NULL now that every row has a default value.
    op.alter_column(
        'books',
        'id',
        existing_type=sa.BigInteger(),
        nullable=False
    )

    # 4) (Optional) If you want 'id' to be the new primary key instead of 'isbn13',
    #    you need to drop the old primary key constraint and create a new one.
    #    If 'books_pkey' is the name of the existing PK on 'isbn13', do this:
    op.drop_constraint('books_pkey', 'books', type_='primary')
    op.create_primary_key('books_pkey', 'books', ['id'])


def downgrade():
    # Reverse the steps:
    # 1) Drop the new primary key on 'id'
    op.drop_constraint('books_pkey', 'books', type_='primary')
    # 2) Recreate the old primary key on 'isbn13' if that was your original PK.
    op.create_primary_key('books_pkey', 'books', ['isbn13'])

    # 3) Drop the 'id' column
    op.drop_column('books', 'id')

    # 4) (Optional) Drop the sequence
    op.execute("DROP SEQUENCE IF EXISTS books_id_seq")