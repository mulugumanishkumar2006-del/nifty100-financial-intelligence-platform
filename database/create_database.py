import sqlite3
from pathlib import Path


def create_database():
    # Project root
    project_root = Path(__file__).resolve().parent

    db_path = project_root / "nifty100.db"
    schema_path = project_root / "schema.sql"

    print("=" * 50)
    print("Creating SQLite Database...")
    print("=" * 50)

    conn = sqlite3.connect(db_path)

    # Enable Foreign Keys
    conn.execute("PRAGMA foreign_keys = ON;")

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = f.read()

    conn.executescript(schema)

    conn.commit()
    conn.close()

    print("✅ Database Created Successfully")
    print(f"📁 Location : {db_path}")


if __name__ == "__main__":
    create_database()