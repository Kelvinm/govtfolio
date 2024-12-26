"""fix pyenums

Revision ID: e721611714e1
Revises: 925f033d508d
Create Date: 2024-12-26 17:08:58.602741

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e721611714e1'
down_revision: Union[str, None] = '925f033d508d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE legislatorposition RENAME TO legislatorposition_old")
    op.execute("CREATE TYPE legislatorposition AS ENUM ('SENATE', 'HOUSE')")
    op.execute("""
        ALTER TABLE legislators 
        ALTER COLUMN position TYPE legislatorposition 
        USING (CASE position::text
            WHEN 'SENATOR' THEN 'SENATE'::legislatorposition
            WHEN 'REPRESENTATIVE' THEN 'HOUSE'::legislatorposition
            WHEN 'Senate' THEN 'SENATE'::legislatorposition
            WHEN 'House' THEN 'HOUSE'::legislatorposition
        END)
    """)
    op.execute("DROP TYPE legislatorposition_old")

def downgrade() -> None:
    op.execute("ALTER TYPE legislatorposition RENAME TO legislatorposition_old")
    op.execute("CREATE TYPE legislatorposition AS ENUM ('SENATOR', 'REPRESENTATIVE')")
    op.execute("""
        ALTER TABLE legislators 
        ALTER COLUMN position TYPE legislatorposition 
        USING (CASE position::text
            WHEN 'SENATE' THEN 'SENATOR'::legislatorposition
            WHEN 'HOUSE' THEN 'REPRESENTATIVE'::legislatorposition
        END)
    """)
    op.execute("DROP TYPE legislatorposition_old")