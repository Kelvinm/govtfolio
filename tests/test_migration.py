from sqlalchemy import text
from src.database import engine

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """))
    print("Created tables:", [row[0] for row in result])