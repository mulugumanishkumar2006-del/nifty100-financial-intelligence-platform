"""
Company Service

NIFTY100 Financial Intelligence Platform
"""

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from app.utils import dataframe_to_records

# ==========================================================
# Database Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE = PROJECT_ROOT / "database" / "nifty100.db"


# ==========================================================
# Database Connection Helper
# ==========================================================

def get_connection() -> sqlite3.Connection:
    """Returns a connection to the SQLite database."""
    return sqlite3.connect(DATABASE)


# ==========================================================
# Get All Companies
# ==========================================================

def get_all_companies() -> List[Dict[str, Any]]:
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
    with get_connection() as connection:
        dataframe = pd.read_sql_query(query, connection)

    return dataframe_to_records(dataframe)


# ==========================================================
# Get Single Company Complete Details
# ==========================================================

def get_company(company_id: str) -> Optional[Dict[str, Any]]:
    company_query = """
    SELECT
        c.id,
        c.company_name,
        c.ticker,
        c.market_cap,
        c.company_logo,
        c.website,
        c.about_company,
        c.face_value,
        c.book_value,
        c.roce_percentage,
        c.roe_percentage,

        s.broad_sector,
        s.sub_sector,
        s.market_cap_category,
        s.index_weight_pct

    FROM companies c
    LEFT JOIN sectors s ON c.id = s.company_id
    WHERE c.id = ?;
    """

    profit_loss_query = """
    SELECT *
    FROM profitandloss
    WHERE company_id = ?
    ORDER BY year;
    """

    balance_query = """
    SELECT *
    FROM balancesheet
    WHERE company_id = ?
    ORDER BY year;
    """

    cashflow_query = """
    SELECT *
    FROM cashflow
    WHERE company_id = ?
    ORDER BY year;
    """

    ratio_query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year;
    """

    with get_connection() as connection:
        company_df = pd.read_sql_query(company_query, connection, params=(company_id,))

        if company_df.empty:
            return None

        profit_loss_df = pd.read_sql_query(profit_loss_query, connection, params=(company_id,))
        balance_df = pd.read_sql_query(balance_query, connection, params=(company_id,))
        cashflow_df = pd.read_sql_query(cashflow_query, connection, params=(company_id,))
        ratio_df = pd.read_sql_query(ratio_query, connection, params=(company_id,))

    company_info = dataframe_to_records(company_df)[0]

    return {
        "company": company_info,
        "profit_loss": dataframe_to_records(profit_loss_df),
        "balance_sheet": dataframe_to_records(balance_df),
        "cash_flow": dataframe_to_records(cashflow_df),
        "financial_ratios": dataframe_to_records(ratio_df),
    }


# ==========================================================
# Search Company
# ==========================================================

def search_company(keyword: str) -> List[Dict[str, Any]]:
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
    with get_connection() as connection:
        dataframe = pd.read_sql_query(query, connection, params=(f"%{keyword}%",))

    return dataframe_to_records(dataframe)


# ==========================================================
# Company Count
# ==========================================================

def total_companies() -> int:
    query = "SELECT COUNT(*) AS total FROM companies;"
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()

    return int(result[0]) if result else 0


# ==========================================================
# Company Statistics
# ==========================================================

def company_statistics() -> Dict[str, Any]:
    query = """
    SELECT
        COUNT(*) AS total_companies,
        COUNT(DISTINCT website) AS companies_with_website
    FROM companies;
    """
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(query)
        row = cursor.fetchone()

    return dict(row) if row else {}


# ==========================================================
# Compare Companies
# ==========================================================

def compare_companies(company1: str, company2: str) -> List[Dict[str, Any]]:
    query = """
    SELECT
        c.id,
        c.company_name,
        c.ticker,
        c.market_cap,
        c.face_value,
        c.book_value,
        c.roce_percentage,
        c.roe_percentage,

        s.broad_sector,
        s.sub_sector

    FROM companies c
    LEFT JOIN sectors s ON c.id = s.company_id
    WHERE c.id IN (?, ?)
    ORDER BY c.company_name;
    """
    with get_connection() as connection:
        dataframe = pd.read_sql_query(query, connection, params=(company1, company2))

    return dataframe_to_records(dataframe)


# ==========================================================
# Get Company Sector
# ==========================================================

def get_company_sector(company_id: str) -> Optional[Dict[str, Any]]:
    query = """
    SELECT
        broad_sector,
        sub_sector
    FROM sectors
    WHERE company_id = ?;
    """
    with get_connection() as connection:
        dataframe = pd.read_sql_query(query, connection, params=(company_id,))

    if dataframe.empty:
        return None

    return dataframe_to_records(dataframe)[0]


# ==========================================================
# Companies in Same Sector
# ==========================================================

def get_peer_companies(company_id: str) -> List[Dict[str, Any]]:
    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector
    FROM companies c
    JOIN sectors s ON c.id = s.company_id
    WHERE s.broad_sector = (
        SELECT broad_sector
        FROM sectors
        WHERE company_id = ?
    )
    ORDER BY c.company_name;
    """
    with get_connection() as connection:
        dataframe = pd.read_sql_query(query, connection, params=(company_id,))

    return dataframe_to_records(dataframe)