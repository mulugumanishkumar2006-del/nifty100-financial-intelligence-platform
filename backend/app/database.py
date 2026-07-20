"""
Database Connection Module
NIFTY100 Financial Intelligence Platform
"""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


# ==========================================================
# Database Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = PROJECT_ROOT / "database" / "nifty100.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# ==========================================================
# SQLAlchemy Engine
# ==========================================================

engine = create_engine(

    DATABASE_URL,

    connect_args={
        "check_same_thread": False
    }

)


# ==========================================================
# Session
# ==========================================================

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)


# ==========================================================
# Base Class
# ==========================================================

Base = declarative_base()


# ==========================================================
# Dependency
# ==========================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()