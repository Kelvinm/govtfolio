"""fix pyenums for tradeType

Revision ID: 46ad84d5335c
Revises: de6b3731f8bb
Create Date: 2024-12-26 18:07:00.204269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '46ad84d5335c'
down_revision: Union[str, None] = 'de6b3731f8bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Rename the existing enum type
    op.execute("ALTER TYPE tradetype RENAME TO tradetype_old")
    
    # Create a new enum type with the additional value
    op.execute("CREATE TYPE tradetype AS ENUM ('BUY', 'SELL', 'EXCHANGE')")
    
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
    op.execute("CREATE TYPE tradetype AS ENUM ('BUY', 'SELL')")
    
    # Update the trades table to use the original enum type
    op.execute("""
        ALTER TABLE trades
        ALTER COLUMN trade_type TYPE tradetype
        USING trade_type::text::tradetype
    """)
    
    # Drop the new enum type
    op.execute("DROP TYPE tradetype_new")