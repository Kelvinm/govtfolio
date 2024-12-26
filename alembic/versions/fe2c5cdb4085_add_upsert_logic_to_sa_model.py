"""add_upsert_logic_to_sa_model

Revision ID: fe2c5cdb4085
Revises: c3e31d4ee6bb
Create Date: 2024-12-24 18:01:29.627483

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe2c5cdb4085'
down_revision: Union[str, None] = 'c3e31d4ee6bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # 1) Set a server default (but keep nullable=True for now so it won't fail on existing nulls).
    op.alter_column(
        'committees',
        'updated_at',
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.text('now()'),
        existing_nullable=True  # keep this True for now
    )
    # 2) Backfill existing NULL values using an UPDATE statement.
    op.execute("UPDATE committees SET updated_at = now() WHERE updated_at IS NULL")
    # 3) Now that no rows have NULL, we can make it NOT NULL safely.
    op.alter_column(
        'committees',
        'updated_at',
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()')
    )

    # Repeat the same steps for other tables if needed:
    # For legislators:
    op.alter_column(
        'legislators',
        'updated_at',
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.text('now()'),
        existing_nullable=True
    )
    op.execute("UPDATE legislators SET updated_at = now() WHERE updated_at IS NULL")
    op.alter_column(
        'legislators',
        'updated_at',
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()')
    )

    # For committee_memberships:
    op.alter_column(
        'committee_memberships',
        'updated_at',
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.text('now()'),
        existing_nullable=True
    )
    op.execute("UPDATE committee_memberships SET updated_at = now() WHERE updated_at IS NULL")
    op.alter_column(
        'committee_memberships',
        'updated_at',
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()')
    )

    # For trades:
    op.alter_column(
        'trades',
        'updated_at',
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.text('now()'),
        existing_nullable=True
    )
    op.execute("UPDATE trades SET updated_at = now() WHERE updated_at IS NULL")
    op.alter_column(
        'trades',
        'updated_at',
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()')
    )


def downgrade():
    # You can optionally revert these changes. For example:
    op.alter_column(
        'trades',
        'updated_at',
        existing_type=sa.DateTime(timezone=True),
        nullable=True,
        server_default=None
    )
    op.alter_column(
        'committee_memberships',
        'updated_at',
        existing_type=sa.DateTime(timezone=True),
        nullable=True,
        server_default=None
    )
    op.alter_column(
        'legislators',
        'updated_at',
        existing_type=sa.DateTime(timezone=True),
        nullable=True,
        server_default=None
    )
    op.alter_column(
        'committees',
        'updated_at',
        existing_type=sa.DateTime(timezone=True),
        nullable=True,
        server_default=None
    )
