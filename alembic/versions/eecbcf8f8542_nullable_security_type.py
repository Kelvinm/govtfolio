"""nullable security type

Revision ID: eecbcf8f8542
Revises: 249875a9f476
Create Date: 2024-12-26 18:18:01.419803

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'eecbcf8f8542'
down_revision: Union[str, None] = '249875a9f476'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade() -> None:
    op.alter_column('trades', 'security_ticker', nullable=True)

def downgrade() -> None:
    op.alter_column('trades', 'security_ticker', nullable=False)