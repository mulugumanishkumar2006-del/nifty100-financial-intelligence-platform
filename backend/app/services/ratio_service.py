"""
Financial Ratio Service

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
# Latest Financial Ratios
# ==========================================================

def get_latest_ratios():

    connection = get_connection()

    query = """
    SELECT *

    FROM financial_ratios

    ORDER BY year DESC;
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe_to_records(dataframe)


# ==========================================================
# Company Ratios
# ==========================================================

def get_company_ratios(company_id: int):

    connection = get_connection()

    query = """
    SELECT *

    FROM financial_ratios

    WHERE company_id=?

    ORDER BY year DESC;
    """

    dataframe = pd.read_sql_query(

        query,

        connection,

        params=(company_id,)

    )

    connection.close()

    return dataframe_to_records(dataframe)


# ==========================================================
# Latest Year
# ==========================================================

def latest_year():

    connection = get_connection()

    query = """

    SELECT MAX(year) AS latest_year

    FROM financial_ratios

    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe.iloc[0]["latest_year"]


# ==========================================================
# Top ROE Companies
# ==========================================================

def top_roe(limit: int = 10):

    connection = get_connection()

    query = f"""

    SELECT

        c.company_name,

        f.return_on_equity_pct

    FROM financial_ratios f

    JOIN companies c

    ON c.id=f.company_id

    ORDER BY return_on_equity_pct DESC

    LIMIT {limit}

    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe_to_records(dataframe)


# ==========================================================
# Top Asset Turnover
# ==========================================================

def top_asset_turnover(limit: int = 10):

    connection = get_connection()

    query = f"""

    SELECT

        c.company_name,

        f.asset_turnover

    FROM financial_ratios f

    JOIN companies c

    ON c.id=f.company_id

    ORDER BY asset_turnover DESC

    LIMIT {limit}

    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe_to_records(dataframe)