import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "database" / "nifty100.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Get companies table structure
cursor.execute("PRAGMA table_info(companies)")
columns = cursor.fetchall()
print("Companies table columns:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

# Get a sample row
cursor.execute("SELECT * FROM companies LIMIT 1")
print("\nSample data:")
print(cursor.description)

conn.close()
