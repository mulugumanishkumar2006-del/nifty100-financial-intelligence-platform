import sqlite3
from pathlib import Path

# ==========================================================
# Database Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "database" / "nifty100.db"

# ==========================================================
# Connect
# ==========================================================

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

# ==========================================================
# Tables
# ==========================================================

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
    "financial_ratios",
]

print("=" * 60)
print("DATABASE ROW COUNT VERIFICATION")
print("=" * 60)

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table:<20}: {count} rows")

connection.close()