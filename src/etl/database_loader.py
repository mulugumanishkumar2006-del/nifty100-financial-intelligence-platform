import sqlite3
from pathlib import Path
import pandas as pd

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FOLDER = PROJECT_ROOT / "data" / "raw"
DATABASE = PROJECT_ROOT / "database" / "nifty100.db"

# ==========================================================
# Excel File Mapping
# ==========================================================

FILE_MAPPING = {
    "companies.xlsx": "companies",
    "profitandloss.xlsx": "profitandloss",
    "balancesheet.xlsx": "balancesheet",
    "cashflow.xlsx": "cashflow",
    "analysis.xlsx": "analysis",
    "documents.xlsx": "documents",
    "prosandcons.xlsx": "prosandcons",
    "financial_ratios.xlsx": "financial_ratios",
    "stock_prices.xlsx": "stock_prices",
    "sectors.xlsx": "sectors",
}

# ==========================================================
# Header Row Mapping
# ==========================================================

HEADER_ROW = {
    "companies.xlsx": 1,
    "profitandloss.xlsx": 1,
    "balancesheet.xlsx": 1,
    "cashflow.xlsx": 1,
    "analysis.xlsx": 1,
    "documents.xlsx": 1,
    "prosandcons.xlsx": 1,
    "financial_ratios.xlsx": 0,
    "stock_prices.xlsx": 0,
    "sectors.xlsx": 0,
}

# ==========================================================
# Column Mapping
# ==========================================================

COLUMN_MAPPING = {

    # Profit & Loss
    "dividend": "dividend_payout",

    # Cash Flow
    "operating_cash_flow": "operating_activity",
    "investing_cash_flow": "investing_activity",
    "financing_cash_flow": "financing_activity",

    # Financial Ratios
    "roe": "return_on_equity_pct",
    "net_profit_margin": "net_profit_margin_pct",
    "operating_profit_margin": "operating_profit_margin_pct",
    "dividend_payout_ratio": "dividend_payout_ratio_pct",
}

# ==========================================================
# Connect Database
# ==========================================================

connection = sqlite3.connect(DATABASE)

print("=" * 60)
print("Clearing Existing Tables")
print("=" * 60)

for table in FILE_MAPPING.values():
    connection.execute(f"DELETE FROM {table}")

connection.commit()

print("✅ Existing data cleared\n")

# ==========================================================
# Load Excel Files
# ==========================================================

for excel_file, table_name in FILE_MAPPING.items():

    print("=" * 60)
    print(f"Loading {excel_file}")

    file_path = DATA_FOLDER / excel_file

    if not file_path.exists():
        print("❌ File not found")
        continue

    try:

        df = pd.read_excel(
            file_path,
            header=HEADER_ROW[excel_file]
        )

        # --------------------------------------------------
        # Normalize Columns
        # --------------------------------------------------

        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
            .str.replace("-", "_", regex=False)
            .str.replace("%", "_pct", regex=False)
            .str.replace("/", "_", regex=False)
        )

        # --------------------------------------------------
        # Rename Columns
        # --------------------------------------------------

        df.rename(columns=COLUMN_MAPPING, inplace=True)

        # --------------------------------------------------
        # Database Columns
        # --------------------------------------------------

        cursor = connection.execute(
            f"PRAGMA table_info({table_name})"
        )

        db_columns = [row[1] for row in cursor.fetchall()]

        matching_columns = [
            c for c in df.columns
            if c in db_columns
        ]

        skipped_columns = [
            c for c in df.columns
            if c not in db_columns
        ]

        print("\nMatching Columns:")
        print(matching_columns)

        if skipped_columns:
            print("\nSkipped Columns:")
            print(skipped_columns)

        df = df[matching_columns]

        print(f"\nRows : {len(df)}")

        df.to_sql(
            table_name,
            connection,
            if_exists="append",
            index=False,
        )

        print(f"✅ Loaded {len(df)} rows into {table_name}")

    except Exception as e:

        print(f"\n❌ Error in {excel_file}")
        print(e)

connection.commit()
connection.close()

print("\n" + "=" * 60)
print("Database Loading Completed")
print("=" * 60)