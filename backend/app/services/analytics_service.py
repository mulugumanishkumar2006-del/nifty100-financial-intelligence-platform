"""
Analytics Service

NIFTY100 Financial Intelligence Platform
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
# Dashboard Summary
# ==========================================================

def dashboard_summary():

    connection = get_connection()

    summary = {}

    summary["companies"] = pd.read_sql_query(
        "SELECT COUNT(*) total FROM companies",
        connection
    ).iloc[0]["total"]

    summary["financial_ratios"] = pd.read_sql_query(
        "SELECT COUNT(*) total FROM financial_ratios",
        connection
    ).iloc[0]["total"]

    summary["stock_prices"] = pd.read_sql_query(
        "SELECT COUNT(*) total FROM stock_prices",
        connection
    ).iloc[0]["total"]

    summary["sectors"] = pd.read_sql_query(
        "SELECT COUNT(DISTINCT broad_sector) total FROM sectors",
        connection
    ).iloc[0]["total"]

    connection.close()

    return summary


# ==========================================================
# Top Revenue Companies
# ==========================================================

def top_revenue(limit=10):

    connection = get_connection()

    query = f"""

    SELECT

        c.company_name,

        p.sales

    FROM profitandloss p

    JOIN companies c

    ON p.company_id=c.id

    ORDER BY sales DESC

    LIMIT {limit}

    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe.to_dict(orient="records")


# ==========================================================
# Top Net Profit Companies
# ==========================================================

def top_profit(limit=10):

    connection = get_connection()

    query = f"""

    SELECT

        c.company_name,

        p.net_profit

    FROM profitandloss p

    JOIN companies c

    ON p.company_id=c.id

    ORDER BY net_profit DESC

    LIMIT {limit}

    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe.to_dict(orient="records")


# ==========================================================
# Sector Distribution
# ==========================================================

def sector_distribution():

    connection = get_connection()

    query = """

    SELECT

        broad_sector,

        COUNT(*) companies

    FROM sectors

    GROUP BY broad_sector

    ORDER BY companies DESC

    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe.to_dict(orient="records")


# ==========================================================
# Latest Financial Year
# ==========================================================

def latest_financial_year():

    connection = get_connection()

    query = """

    SELECT MAX(year) latest_year

    FROM financial_ratios

    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe.iloc[0]["latest_year"]