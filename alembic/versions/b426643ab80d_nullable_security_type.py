"""nullable security type

Revision ID: b426643ab80d
Revises: eecbcf8f8542
Create Date: 2024-12-26 18:22:09.225758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b426643ab80d'
down_revision: Union[str, None] = 'eecbcf8f8542'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.alter_column('trades', 'trade_date', nullable=True)
    op.alter_column('trades', 'disclosure_date', nullable=True)

def downgrade() -> None:
    op.alter_column('trades', 'trade_date', nullable=False)
    op.alter_column('trades', 'disclosure_date', nullable=True)