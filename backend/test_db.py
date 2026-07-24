from pathlib import Path
import sqlite3

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE = PROJECT_ROOT / "database" / "nifty100.db"

print("Database path:", DATABASE)
print("Exists:", DATABASE.exists())

conn = sqlite3.connect(DATABASE)

cursor = conn.execute("PRAGMA table_info(companies);")

print("\nCompanies Table:\n")

for row in cursor:
    print(row)

conn.close()