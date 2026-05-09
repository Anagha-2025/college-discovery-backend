import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Get the URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Fix the "postgres://" vs "postgresql://" issue for SQLAlchemy 1.4+
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Fallback to your local DB if the cloud URL isn't found
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:AB1234@localhost/colleges"

# 4. Create the engine
# 'pool_pre_ping' is highly recommended for cloud databases like Neon to prevent timeouts
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()