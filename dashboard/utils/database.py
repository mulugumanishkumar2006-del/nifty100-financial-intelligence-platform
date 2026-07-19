"""
==========================================================
Database Utility
==========================================================
Handles SQLite database connection and query execution
==========================================================
"""

import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st


# --------------------------------------------------------
# Project Paths
# --------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE = PROJECT_ROOT / "database" / "nifty100.db"


# --------------------------------------------------------
# Database Connection
# --------------------------------------------------------

@st.cache_resource
def get_connection():
    """
    Returns SQLite connection
    """

    connection = sqlite3.connect(
        DATABASE,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


# --------------------------------------------------------
# Execute Query
# --------------------------------------------------------

@st.cache_data(show_spinner=False)
def run_query(query: str):

    connection = get_connection()

    dataframe = pd.read_sql_query(query, connection)

    return dataframe


# --------------------------------------------------------
# Execute Query (compatibility wrapper)
# --------------------------------------------------------

def execute_query(query: str, params: tuple | None = None):
    """Execute a SQL query and return a DataFrame."""

    if params is None:
        return run_query(query)

    return run_query_params(query, params)


# --------------------------------------------------------
# Execute Parameterized Query
# --------------------------------------------------------

@st.cache_data(show_spinner=False)
def run_query_params(query: str, params: tuple):

    connection = get_connection()

    dataframe = pd.read_sql_query(
        query,
        connection,
        params=params
    )

    return dataframe


# --------------------------------------------------------
# List Tables
# --------------------------------------------------------

def get_tables():

    query = """

    SELECT
        name

    FROM sqlite_master

    WHERE type='table'

    ORDER BY name;

    """

    return run_query(query)


# --------------------------------------------------------
# Company List
# --------------------------------------------------------

def get_company_names():

    query = """

    SELECT
        company_name

    FROM companies

    ORDER BY company_name;

    """

    df = run_query(query)

    return df["company_name"].tolist()


# --------------------------------------------------------
# Sector List
# --------------------------------------------------------

def get_sector_names():

    query = """

    SELECT DISTINCT

        broad_sector

    FROM sectors

    ORDER BY broad_sector;

    """

    df = run_query(query)

    return df["broad_sector"].dropna().tolist()


# --------------------------------------------------------
# Database Statistics
# --------------------------------------------------------

def database_statistics():

    connection = get_connection()

    cursor = connection.cursor()

    tables = [

        "companies",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "analysis",
        "documents",
        "prosandcons",
        "stock_prices",
        "sectors"

    ]

    statistics = {}

    for table in tables:

        try:

            cursor.execute(
                f"SELECT COUNT(*) FROM {table}"
            )

            statistics[table] = cursor.fetchone()[0]

        except Exception:

            statistics[table] = 0

    return statistics


# --------------------------------------------------------
# Latest Financial Year
# --------------------------------------------------------

def latest_year():

    query = """

    SELECT

        MAX(year) AS latest_year

    FROM profitandloss;

    """

    df = run_query(query)

    return df.iloc[0]["latest_year"]


# --------------------------------------------------------
# Database Health Check
# --------------------------------------------------------

def health_check():

    try:

        connection = get_connection()

        connection.execute("SELECT 1")

        return True

    except Exception:

        return False


# --------------------------------------------------------
# Close Connection
# --------------------------------------------------------

def close_connection():

    try:

        get_connection().close()

    except Exception:

        pass