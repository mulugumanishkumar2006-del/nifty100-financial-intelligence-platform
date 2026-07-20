"""
Company Service

NIFTY100 Financial Intelligence Platform
"""

import sqlite3
from pathlib import Path

import pandas as pd


# ==========================================================
# Database Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATABASE = PROJECT_ROOT / "database" / "nifty100.db"


# ==========================================================
# Database Connection
# ==========================================================

def get_connection():

    return sqlite3.connect(DATABASE)


# ==========================================================
# Get All Companies
# ==========================================================

def get_all_companies():

    connection = get_connection()

    query = """
    SELECT
        id,
        company_name,
        ticker
    FROM companies
    ORDER BY company_name;
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe.to_dict(orient="records")


# ==========================================================
# Get Company By ID
# ==========================================================

def get_company(company_id: int):

    connection = get_connection()

    query = """
    SELECT *
    FROM companies
    WHERE id = ?;
    """

    dataframe = pd.read_sql_query(

        query,

        connection,

        params=(company_id,)

    )

    connection.close()

    if dataframe.empty:

        return None

    return dataframe.to_dict(orient="records")[0]


# ==========================================================
# Search Company
# ==========================================================

def search_company(keyword: str):

    connection = get_connection()

    query = """
    SELECT
        id,
        company_name,
        ticker
    FROM companies
    WHERE company_name LIKE ?
    ORDER BY company_name;
    """

    dataframe = pd.read_sql_query(

        query,

        connection,

        params=(f"%{keyword}%",)

    )

    connection.close()

    return dataframe.to_dict(orient="records")


# ==========================================================
# Company Count
# ==========================================================

def total_companies():

    connection = get_connection()

    query = """
    SELECT COUNT(*) AS total
    FROM companies;
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return int(dataframe.iloc[0]["total"])


# ==========================================================
# Company Statistics
# ==========================================================

def company_statistics():

    connection = get_connection()

    query = """
    SELECT

        COUNT(*) AS total_companies,

        COUNT(DISTINCT ticker) AS total_tickers

    FROM companies;
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe.to_dict(orient="records")[0]