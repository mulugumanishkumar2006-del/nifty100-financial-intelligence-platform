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
# Connect Database
# ==========================================================

connection = sqlite3.connect(DATABASE)

# ==========================================================
# Clear Existing Data
# ==========================================================

print("=" * 60)
print("Clearing Existing Tables")
print("=" * 60)

for table in FILE_MAPPING.values():
    connection.execute(f"DELETE FROM {table}")

connection.commit()

print("✅ Existing data cleared.\n")

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

        # -----------------------------------
        # Read Excel
        # -----------------------------------

        df = pd.read_excel(
            file_path,
            header=HEADER_ROW[excel_file]
        )

        # -----------------------------------
        # Normalize Columns
        # -----------------------------------

        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
            .str.replace("-", "_", regex=False)
        )

        # -----------------------------------
        # Read Database Schema
        # -----------------------------------

        cursor = connection.execute(
            f"PRAGMA table_info({table_name})"
        )

        db_columns = [row[1] for row in cursor.fetchall()]

        # -----------------------------------
        # Match Columns
        # -----------------------------------

        matching_columns = [
            col for col in df.columns
            if col in db_columns
        ]

        skipped_columns = [
            col for col in df.columns
            if col not in db_columns
        ]

        print("\nDatabase Columns:")
        print(db_columns)

        print("\nExcel Columns:")
        print(df.columns.tolist())

        print("\nMatching Columns:")
        print(matching_columns)

        if skipped_columns:
            print("\nSkipped Columns:")
            print(skipped_columns)

        # -----------------------------------
        # Keep Matching Columns
        # -----------------------------------

        df = df[matching_columns]

        print(f"\nRows Ready For Insert : {len(df)}")

        # -----------------------------------
        # Insert
        # -----------------------------------

        df.to_sql(
            table_name,
            connection,
            if_exists="append",
            index=False
        )

        print(f"✅ Inserted {len(df)} rows into {table_name}")

    except Exception as e:

        print(f"\n❌ Error while loading {excel_file}")
        print(e)

# ==========================================================
# Close Database
# ==========================================================

connection.commit()
connection.close()

print("\n" + "=" * 60)
print("Database Loading Completed")
print("=" * 60)