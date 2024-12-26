"""Change party enum

Revision ID: f9c85bcac0ed
Revises: fe2c5cdb4085
Create Date: 2024-12-26 16:30:32.344948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f9c85bcac0ed'
down_revision: Union[str, None] = 'fe2c5cdb4085'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.execute("ALTER TYPE legislatorparty RENAME TO legislatorparty_old")
   op.execute("CREATE TYPE legislatorparty AS ENUM ('Democrat', 'Republican', 'Independent')")
   op.execute((
       "ALTER TABLE legislators ALTER COLUMN party TYPE legislatorparty USING "
       "CASE "
       "WHEN party::text = 'Democratic' THEN 'Democrat'::legislatorparty "
       "ELSE party::text::legislatorparty "
       "END"
   ))
   op.execute("DROP TYPE legislatorparty_old")

def downgrade() -> None:
   op.execute("ALTER TYPE legislatorparty RENAME TO legislatorparty_old")
   op.execute("CREATE TYPE legislatorparty AS ENUM ('Democratic', 'Republican', 'Independent')")
   op.execute((
       "ALTER TABLE legislators ALTER COLUMN party TYPE legislatorparty USING "
       "CASE "
       "WHEN party::text = 'Democrat' THEN 'Democratic'::legislatorparty "
       "ELSE party::text::legislatorparty "
       "END"
   ))
   op.execute("DROP TYPE legislatorparty_old")