import sqlite3
from pathlib import Path

DATABASE = Path("database") / "nifty100.db"

print("Database:", DATABASE.resolve())

conn = sqlite3.connect(DATABASE)

tables = [
    "profitandloss",
    "financial_ratios",
    "stock_prices",
    "market_cap",
    "companies",
    "sectors"
]

for table in tables:
    print(f"\n========== {table} ==========")

    try:
        rows = conn.execute(f"PRAGMA table_info({table})").fetchall()

        if not rows:
            print("Table not found or empty.")
            continue

        for row in rows:
            print(row)

    except Exception as e:
        print(e)

conn.close()