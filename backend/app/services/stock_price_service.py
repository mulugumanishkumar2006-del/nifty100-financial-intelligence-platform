"""
Stock Price Service

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
# Latest Stock Prices
# ==========================================================

def latest_prices(limit: int = 100):

    connection = get_connection()

    query = f"""

    SELECT

        c.company_name,

        sp.*

    FROM stock_prices sp

    JOIN companies c

    ON sp.company_id = c.id

    ORDER BY sp.date DESC

    LIMIT {limit}

    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe.to_dict(orient="records")


# ==========================================================
# Company Price History
# ==========================================================

def company_price_history(company_id: int):

    connection = get_connection()

    query = """

    SELECT *

    FROM stock_prices

    WHERE company_id = ?

    ORDER BY date DESC

    """

    dataframe = pd.read_sql_query(

        query,

        connection,

        params=(company_id,)

    )

    connection.close()

    return dataframe.to_dict(orient="records")


# ==========================================================
# Latest Price
# ==========================================================

def latest_price(company_id: int):

    connection = get_connection()

    query = """

    SELECT *

    FROM stock_prices

    WHERE company_id = ?

    ORDER BY date DESC

    LIMIT 1

    """

    dataframe = pd.read_sql_query(

        query,

        connection,

        params=(company_id,)

    )

    connection.close()

    if dataframe.empty:

        return {}

    return dataframe.to_dict(orient="records")[0]


# ==========================================================
# Total Records
# ==========================================================

def total_stock_records():

    connection = get_connection()

    query = """

    SELECT COUNT(*) total

    FROM stock_prices

    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return int(dataframe.iloc[0]["total"])