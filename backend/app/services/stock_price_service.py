"""
Stock Price Service

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
# Latest Stock Prices
# ==========================================================

def latest_prices(limit: int = 100):

    connection = get_connection()

    query = """
    SELECT
        sp.id,
        sp.company_id,
        c.company_name,

        sp.date,

        sp.open_price,
        sp.high_price,
        sp.low_price,
        sp.close_price,

        sp.adjusted_close,
        sp.volume,

        sp.high_price AS high_52,
        sp.low_price AS low_52,

        sp.close_price AS current_price,
        sp.close_price AS price,

        0 AS change_percentage

    FROM stock_prices sp

    INNER JOIN companies c
        ON sp.company_id = c.id

    ORDER BY sp.date DESC

    LIMIT ?
    """

    dataframe = pd.read_sql_query(
        query,
        connection,
        params=(limit,),
    )

    connection.close()

    return dataframe_to_records(dataframe)


# ==========================================================
# Company Price History
# ==========================================================

def company_price_history(company_id: str):

    connection = get_connection()

    query = """
    SELECT

        date,
        open_price,
        high_price,
        low_price,
        close_price,
        adjusted_close,
        volume

    FROM stock_prices

    WHERE company_id = ?

    ORDER BY date DESC
    """

    dataframe = pd.read_sql_query(
        query,
        connection,
        params=(company_id,),
    )

    connection.close()

    return dataframe_to_records(dataframe)


# ==========================================================
# Latest Price
# ==========================================================

def latest_price(company_id: str):

    connection = get_connection()

    query = """
    SELECT

        date,
        open_price,
        high_price,
        low_price,
        close_price,
        adjusted_close,
        volume

    FROM stock_prices

    WHERE company_id = ?

    ORDER BY date DESC

    LIMIT 1
    """

    dataframe = pd.read_sql_query(
        query,
        connection,
        params=(company_id,),
    )

    connection.close()

    if dataframe.empty:
        return {}

    return dataframe_to_records(dataframe)[0]


# ==========================================================
# Total Stock Records
# ==========================================================

def total_stock_records():

    connection = get_connection()

    query = """
    SELECT COUNT(*) AS total
    FROM stock_prices
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return int(dataframe.iloc[0]["total"])