"""add_url_to_committees

Revision ID: c3e31d4ee6bb
Revises: 5dd83fc0e2a9
Create Date: 2024-12-24 16:37:48.210575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3e31d4ee6bb'
down_revision: Union[str, None] = '5dd83fc0e2a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('committees', sa.Column('url', sa.String(500), nullable=True))

def downgrade() -> None:
    op.drop_column('committees', 'url')