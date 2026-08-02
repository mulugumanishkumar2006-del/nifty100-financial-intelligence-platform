"""
Create SQLite Database

NIFTY100 Financial Intelligence Platform
"""

import sqlite3
from pathlib import Path


# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

DATABASE = PROJECT_ROOT / "nifty100.db"
SCHEMA = PROJECT_ROOT / "schema.sql"


# ==========================================================
# Create Database
# ==========================================================

def create_database():

    print("=" * 60)
    print("Creating NIFTY100 SQLite Database")
    print("=" * 60)

    if not SCHEMA.exists():
        raise FileNotFoundError(f"Schema file not found:\n{SCHEMA}")

    connection = sqlite3.connect(DATABASE)

    # Enable Foreign Keys
    connection.execute("PRAGMA foreign_keys = ON;")

    with open(SCHEMA, "r", encoding="utf-8") as file:
        sql = file.read()

    connection.executescript(sql)

    connection.commit()
    connection.close()

    print("✅ Database Created Successfully")
    print(f"📂 Database : {DATABASE}")
    print(f"📄 Schema   : {SCHEMA}")


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":
    create_database()