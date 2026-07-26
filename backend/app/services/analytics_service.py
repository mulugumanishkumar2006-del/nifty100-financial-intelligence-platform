"""
Analytics Service

NIFTY100 Financial Intelligence Platform
"""

import sqlite3
from pathlib import Path

import pandas as pd
from app.utils import dataframe_to_records

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

    # ======================================================
    # Total Companies
    # ======================================================

    summary["companies"] = int(
        pd.read_sql_query(
            """
            SELECT COUNT(*) AS total
            FROM companies
            """,
            connection,
        ).iloc[0]["total"]
    )

    # ======================================================
    # Total Revenue
    # ======================================================

    revenue = pd.read_sql_query(
        """
        SELECT SUM(sales) AS total_revenue
        FROM profitandloss
        """,
        connection,
    )

    summary["total_revenue"] = float(
        revenue.iloc[0]["total_revenue"] or 0
    )

    # ======================================================
    # Total Net Profit
    # ======================================================

    profit = pd.read_sql_query(
        """
        SELECT SUM(net_profit) AS total_profit
        FROM profitandloss
        """,
        connection,
    )

    summary["total_profit"] = float(
        profit.iloc[0]["total_profit"] or 0
    )

    # ======================================================
    # Average ROE
    # ======================================================

    roe = pd.read_sql_query(
        """
        SELECT AVG(roe_percentage) AS average_roe
        FROM companies
        """,
        connection,
    )

    summary["average_roe"] = round(
        float(roe.iloc[0]["average_roe"] or 0),
        2,
    )

    # ======================================================
    # Average ROCE
    # ======================================================

    roce = pd.read_sql_query(
        """
        SELECT AVG(roce_percentage) AS average_roce
        FROM companies
        """,
        connection,
    )

    summary["average_roce"] = round(
        float(roce.iloc[0]["average_roce"] or 0),
        2,
    )

    # ======================================================
    # Latest Financial Year
    # ======================================================

    latest = pd.read_sql_query(
        """
        SELECT MAX(year) AS latest_year
        FROM financial_ratios
        """,
        connection,
    )

    summary["latest_year"] = latest.iloc[0]["latest_year"]

    # ======================================================
    # Total Sectors
    # ======================================================

    sectors = pd.read_sql_query(
        """
        SELECT COUNT(DISTINCT broad_sector) AS total
        FROM sectors
        """,
        connection,
    )

    summary["total_sectors"] = int(
        sectors.iloc[0]["total"]
    )

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
        ON p.company_id = c.id
    ORDER BY p.sales DESC
    LIMIT {limit}
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe_to_records(dataframe)


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
        ON p.company_id = c.id
    ORDER BY p.net_profit DESC
    LIMIT {limit}
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe_to_records(dataframe)


# ==========================================================
# Sector Distribution
# ==========================================================

def sector_distribution():

    connection = get_connection()

    query = """
    SELECT
        broad_sector,
        COUNT(*) AS companies
    FROM sectors
    GROUP BY broad_sector
    ORDER BY companies DESC
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe_to_records(dataframe)


# ==========================================================
# Latest Financial Year
# ==========================================================

def latest_financial_year():

    connection = get_connection()

    query = """
    SELECT MAX(year) AS latest_year
    FROM financial_ratios
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe.iloc[0]["latest_year"]

def revenue_ranking(limit=10):

    connection = get_connection()

    query = f"""
    SELECT
        c.company_name,
        p.sales
    FROM profitandloss p
    INNER JOIN companies c
        ON c.id = p.company_id
    WHERE p.sales IS NOT NULL
    ORDER BY p.sales DESC
    LIMIT {limit}
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe_to_records(dataframe)

def profit_ranking(limit=10):

    connection = get_connection()

    query = f"""
    SELECT
        c.company_name,
        p.net_profit
    FROM profitandloss p
    INNER JOIN companies c
        ON c.id = p.company_id
    WHERE p.net_profit IS NOT NULL
    ORDER BY p.net_profit DESC
    LIMIT {limit}
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe_to_records(dataframe)