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

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE = PROJECT_ROOT / "database" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DATABASE)


# ==========================================================
# Revenue Trend
# ==========================================================

def get_revenue_trend(company_id):
    conn = get_connection()

    query = """
    SELECT year, sales
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
    SELECT year, roe
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
    conn = get_connection()

    query = """
    SELECT
        company_name,
        market_cap
    FROM market_cap
    ORDER BY market_cap DESC
    LIMIT 10
    """

    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        return []

    return df.to_dict(orient="records")


# ==========================================================
# Sector Distribution
# ==========================================================

def get_sector_distribution():
    conn = get_connection()

    query = """
    SELECT
        sector,
        COUNT(*) AS companies
    FROM sectors
    GROUP BY sector
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
        close
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