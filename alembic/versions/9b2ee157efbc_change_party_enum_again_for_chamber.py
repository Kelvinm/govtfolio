"""Change party enum again for chamber

Revision ID: 9b2ee157efbc
Revises: f9c85bcac0ed
Create Date: 2024-12-26 16:37:06.561014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9b2ee157efbc'
down_revision: Union[str, None] = 'f9c85bcac0ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
   op.execute("ALTER TYPE legislatorposition RENAME TO legislatorposition_old")
   op.execute("CREATE TYPE legislatorposition AS ENUM ('Senate', 'House')")
   op.execute("ALTER TABLE legislators ALTER COLUMN position TYPE legislatorposition USING position::text::legislatorposition")
   op.execute("DROP TYPE legislatorposition_old")

def downgrade() -> None:
   op.execute("ALTER TYPE legislatorposition RENAME TO legislatorposition_old")
   op.execute("CREATE TYPE legislatorposition AS ENUM ('Senator', 'Representative')")
   op.execute("""
       ALTER TABLE legislators ALTER COLUMN position TYPE legislatorposition USING 
       CASE position::text
           WHEN 'Senate' THEN 'Senator'::legislatorposition
           WHEN 'House' THEN 'Representative'::legislatorposition
       END
   """)
   op.execute("DROP TYPE legislatorposition_old")