from sqlalchemy import create_engine, text

# Create database URL
DATABASE_URL = "postgresql://postgres:postgres@db/postgres"

# Create engine
engine = create_engine(DATABASE_URL)

# Test connection
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print(result.fetchone())