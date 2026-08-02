"""
Chart Service

Provides data for Dashboard Charts
"""

import sqlite3
from pathlib import Path
import pandas as pd

# ==========================================================
# Database
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE = PROJECT_ROOT / "database" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DATABASE)


# ==========================================================
# Revenue Trend
# ==========================================================

def get_revenue_trend(company_id):
    conn = get_connection()

    query = """
    SELECT
        year,
        sales
    FROM profitandloss
    WHERE company_id = ?
    ORDER BY year
    """

    df = pd.read_sql(query, conn, params=[company_id])
    conn.close()

    if df.empty:
        return []

    return df.to_dict(orient="records")


# ==========================================================
# ROE Trend
# ==========================================================

def get_roe_trend(company_id):
    conn = get_connection()

    query = """
    SELECT
        year,
        return_on_equity_pct AS roe
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year
    """

    df = pd.read_sql(query, conn, params=[company_id])
    conn.close()

    if df.empty:
        return []

    return df.to_dict(orient="records")


# ==========================================================
# Market Cap Comparison
# ==========================================================

def get_market_cap():
    """
    Your current database does not contain a market_cap table.
    Returning an empty list until it is added.
    """
    return []


# ==========================================================
# Sector Distribution
# ==========================================================

def get_sector_distribution():
    conn = get_connection()

    query = """
    SELECT
        broad_sector AS sector,
        COUNT(*) AS companies
    FROM sectors
    GROUP BY broad_sector
    ORDER BY companies DESC
    """

    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        return []

    return df.to_dict(orient="records")


# ==========================================================
# Stock Price History
# ==========================================================

def get_stock_history(company_id):
    conn = get_connection()

    query = """
    SELECT
        date,
        close_price AS close
    FROM stock_prices
    WHERE company_id = ?
    ORDER BY date
    LIMIT 365
    """

    df = pd.read_sql(query, conn, params=[company_id])
    conn.close()

    if df.empty:
        return []

    return df.to_dict(orient="records")