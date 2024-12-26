"""fix pyenums for real

Revision ID: de6b3731f8bb
Revises: e721611714e1
Create Date: 2024-12-26 17:10:57.842901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'de6b3731f8bb'
down_revision: Union[str, None] = 'e721611714e1'
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
        END)
    """)
    op.execute("DROP TYPE legislatorposition_old")