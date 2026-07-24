"""
Company Service

NIFTY100 Financial Intelligence Platform
"""

import sqlite3
from pathlib import Path

import pandas as pd
from app.utils import dataframe_to_records

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
        website,
        about_company,
        face_value,
        book_value,
        roce_percentage,
        roe_percentage
    FROM companies
    ORDER BY company_name;
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe_to_records(dataframe)


# ==========================================================
# Get Company
# ==========================================================

def get_company(company_id: str):

    connection = get_connection()

    query = """
    SELECT
        id,
        company_name,
        website,
        about_company,
        face_value,
        book_value,
        roce_percentage,
        roe_percentage
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

    return dataframe_to_records(dataframe)[0]


# ==========================================================
# Search Company
# ==========================================================

def search_company(keyword: str):

    connection = get_connection()

    query = """
    SELECT
        id,
        company_name,
        website,
        about_company,
        face_value,
        book_value,
        roce_percentage,
        roe_percentage
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

    return dataframe_to_records(dataframe)


# ==========================================================
# Company Count
# ==========================================================

def total_companies():

    connection = get_connection()

    dataframe = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM companies;",
        connection
    )

    connection.close()

    return int(dataframe.iloc[0]["total"])


# ==========================================================
# Company Statistics
# ==========================================================

def company_statistics():

    connection = get_connection()

    dataframe = pd.read_sql_query(
        """
        SELECT
            COUNT(*) AS total_companies,
            COUNT(DISTINCT website) AS companies_with_website
        FROM companies;
        """,
        connection
    )

    connection.close()

    records = dataframe_to_records(dataframe)

    return records[0]