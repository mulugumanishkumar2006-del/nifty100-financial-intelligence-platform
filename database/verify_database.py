import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "nifty100.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "sectors",
    "stock_prices",
    "financial_ratios"
]

print("=" * 60)
print("DATABASE ROW COUNT VERIFICATION")
print("=" * 60)

for table in tables:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<20} : {count} rows")
    except Exception as e:
        print(f"{table:<20} : ERROR -> {e}")

connection.close()