"""
Chart Service

NIFTY100 Financial Intelligence Platform
Provides chart-ready financial data from SQLite.
"""

import sqlite3
from pathlib import Path


# ==========================================================
# Database Configuration
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATABASE = PROJECT_ROOT / "database" / "nifty100.db"


# ==========================================================
# Database Connection
# ==========================================================

def get_connection():
    """
    Create a connection to the NIFTY100 SQLite database.
    """

    if not DATABASE.exists():
        raise FileNotFoundError(
            f"NIFTY100 database not found: {DATABASE}"
        )

    return sqlite3.connect(DATABASE)


# ==========================================================
# Revenue / Sales Trend
# ==========================================================

def get_revenue_trend(company_id: str):
    """
    Return yearly sales/revenue trend for a company.

    Source:
        profitandloss.sales
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                year,
                sales
            FROM profitandloss
            WHERE company_id = ?
            ORDER BY year
            """,
            (company_id,),
        )

        rows = cursor.fetchall()

        return [
            {
                "year": row[0],
                "revenue": row[1],
            }
            for row in rows
        ]

    finally:
        connection.close()


# ==========================================================
# ROE Trend
# ==========================================================

def get_roe_trend(company_id: str):
    """
    Return yearly ROE trend for a company.

    Source:
        financial_ratios.return_on_equity_pct
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                year,
                return_on_equity_pct
            FROM financial_ratios
            WHERE company_id = ?
            ORDER BY year
            """,
            (company_id,),
        )

        rows = cursor.fetchall()

        return [
            {
                "year": row[0],
                "roe": row[1],
            }
            for row in rows
        ]

    finally:
        connection.close()


# ==========================================================
# Market Cap / Company Weight
# ==========================================================

def get_market_cap():
    """
    Return company market-cap category and index weight.

    Note:
        The companies table does NOT contain a market_cap column.

    Therefore this endpoint uses:
        sectors.market_cap_category
        sectors.index_weight_pct
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                c.id,
                c.company_name,
                s.market_cap_category,
                s.index_weight_pct
            FROM companies c
            LEFT JOIN sectors s
                ON c.id = s.company_id
            ORDER BY s.index_weight_pct DESC
            """
        )

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "company_name": row[1],
                "market_cap_category": row[2],
                "index_weight_pct": row[3],
            }
            for row in rows
        ]

    finally:
        connection.close()


# ==========================================================
# Sector Distribution
# ==========================================================

def get_sector_distribution():
    """
    Return number of companies in each broad sector.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                broad_sector,
                COUNT(*) AS company_count
            FROM sectors
            WHERE broad_sector IS NOT NULL
            GROUP BY broad_sector
            ORDER BY company_count DESC
            """
        )

        rows = cursor.fetchall()

        return [
            {
                "sector": row[0],
                "company_count": row[1],
            }
            for row in rows
        ]

    finally:
        connection.close()


# ==========================================================
# Stock Price History
# ==========================================================

def get_stock_history(company_id: str):
    """
    Return historical stock prices for a company.

    Source:
        stock_prices.close_price
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                date,
                open_price,
                high_price,
                low_price,
                close_price,
                volume,
                adjusted_close
            FROM stock_prices
            WHERE company_id = ?
            ORDER BY date
            """,
            (company_id,),
        )

        rows = cursor.fetchall()

        return [
            {
                "date": row[0],
                "open": row[1],
                "high": row[2],
                "low": row[3],
                "close": row[4],
                "volume": row[5],
                "adjusted_close": row[6],
            }
            for row in rows
        ]

    finally:
        connection.close()