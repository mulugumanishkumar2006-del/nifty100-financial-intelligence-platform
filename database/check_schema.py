import sqlite3
from pathlib import Path

# Update the path if your database is elsewhere
DATABASE = Path(__file__).parent / "nifty100.db"

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

# Get all tables
cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name;
""")

tables = cursor.fetchall()

print("=" * 60)
print("DATABASE TABLES")
print("=" * 60)

for table in tables:
    table_name = table[0]
    print(f"\n📁 {table_name}")

    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    for column in columns:
        print(f"   • {column[1]} ({column[2]})")

connection.close()