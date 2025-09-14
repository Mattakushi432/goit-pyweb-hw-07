from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os
# Prefer DATABASE_URL env var; default to a local SQLite database to avoid requiring a running Postgres instance
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# For SQLite, check_same_thread should be False when used with SQLAlchemy in some contexts; pass only for sqlite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
