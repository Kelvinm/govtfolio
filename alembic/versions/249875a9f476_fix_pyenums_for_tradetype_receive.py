"""fix pyenums for tradeType receive

Revision ID: 249875a9f476
Revises: 46ad84d5335c
Create Date: 2024-12-26 18:15:32.694046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '249875a9f476'
down_revision: Union[str, None] = '46ad84d5335c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Rename the existing enum type
    op.execute("ALTER TYPE tradetype RENAME TO tradetype_old")
    
    # Create a new enum type with the additional value
    op.execute("CREATE TYPE tradetype AS ENUM ('BUY', 'SELL', 'EXCHANGE', 'RECEIVE')")
    
    # Update the trades table to use the new enum type
    op.execute("""
        ALTER TABLE trades
        ALTER COLUMN trade_type TYPE tradetype
        USING trade_type::text::tradetype
    """)
    
    # Drop the old enum type
    op.execute("DROP TYPE tradetype_old")


def downgrade() -> None:
    # Rename the existing enum type
    op.execute("ALTER TYPE tradetype RENAME TO tradetype_new")
    
    # Recreate the original enum type
    op.execute("CREATE TYPE tradetype AS ENUM ('BUY', 'SELL', 'EXCHANGE')")
    
    # Update the trades table to use the original enum type
    op.execute("""
        ALTER TABLE trades
        ALTER COLUMN trade_type TYPE tradetype
        USING trade_type::text::tradetype
    """)
    
    # Drop the new enum type
    op.execute("DROP TYPE tradetype_new")