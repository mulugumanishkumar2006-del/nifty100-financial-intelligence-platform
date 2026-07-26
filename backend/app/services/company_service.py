"""
Company Service

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


    df = pd.read_sql_query(
        query,
        connection
    )


    connection.close()


    return dataframe_to_records(df)



# ==========================================================
# Get Company By ID
# ==========================================================

def get_company(company_id):

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

    WHERE id = ?

    """


    df = pd.read_sql_query(
        query,
        connection,
        params=(company_id,)
    )


    connection.close()


    if df.empty:
        return None


    return dataframe_to_records(df)[0]



# ==========================================================
# Search Company
# ==========================================================

def search_company(keyword):

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

    ORDER BY company_name

    """


    df = pd.read_sql_query(
        query,
        connection,
        params=(f"%{keyword}%",)
    )


    connection.close()


    return dataframe_to_records(df)



# ==========================================================
# Company Count
# ==========================================================

def total_companies():

    connection = get_connection()


    df = pd.read_sql_query(
        """
        SELECT COUNT(*) total
        FROM companies
        """,
        connection
    )


    connection.close()


    return int(df.iloc[0]["total"])


# ==========================================================
# Complete Company Details
# ==========================================================

def get_company_details(company_id: str):

    connection = get_connection()


    company = pd.read_sql_query(
        """
        SELECT *
        FROM companies
        WHERE id = ?
        """,
        connection,
        params=(company_id,)
    )


    if company.empty:
        connection.close()
        return None


    company_data = dataframe_to_records(company)[0]


    # ================================
    # Profit & Loss
    # ================================

    pnl = pd.read_sql_query(
        """
        SELECT
            sales,
            operating_profit,
            net_profit,
            eps,
            dividend
        FROM profitandloss
        WHERE company_id = ?
        ORDER BY year DESC
        LIMIT 1
        """,
        connection,
        params=(company_id,)
    )


    company_data["profit_loss"] = (
        dataframe_to_records(pnl)[0]
        if not pnl.empty
        else {}
    )



    # ================================
    # Balance Sheet
    # ================================

    balance = pd.read_sql_query(
        """
        SELECT
            total_assets,
            total_liabilities,
            equity_capital,
            reserves,
            borrowings
        FROM balancesheet
        WHERE company_id = ?
        ORDER BY year DESC
        LIMIT 1
        """,
        connection,
        params=(company_id,)
    )


    company_data["balance_sheet"] = (
        dataframe_to_records(balance)[0]
        if not balance.empty
        else {}
    )



    # ================================
    # Cash Flow
    # ================================

    cashflow = pd.read_sql_query(
        """
        SELECT
            operating_cash_flow,
            investing_cash_flow,
            financing_cash_flow,
            net_cash_flow,
            free_cash_flow
        FROM cashflow
        WHERE company_id = ?
        ORDER BY year DESC
        LIMIT 1
        """,
        connection,
        params=(company_id,)
    )


    company_data["cash_flow"] = (
        dataframe_to_records(cashflow)[0]
        if not cashflow.empty
        else {}
    )


    connection.close()


    return company_data
# ==========================================================
# Complete Company Financial Details
# ==========================================================

def get_company_financials(company_id: str):

    connection = get_connection()


    company = pd.read_sql_query(
        """
        SELECT *
        FROM companies
        WHERE id = ?
        """,
        connection,
        params=(company_id,)
    )


    if company.empty:

        connection.close()
        return None



    profit_loss = pd.read_sql_query(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id = ?
        """,
        connection,
        params=(company_id,)
    )


    balance_sheet = pd.read_sql_query(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id = ?
        """,
        connection,
        params=(company_id,)
    )


    cash_flow = pd.read_sql_query(
        """
        SELECT *
        FROM cashflow
        WHERE company_id = ?
        """,
        connection,
        params=(company_id,)
    )


    ratios = pd.read_sql_query(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        """,
        connection,
        params=(company_id,)
    )


    connection.close()


    return {

        "company": dataframe_to_records(company)[0],

        "profit_loss":
            dataframe_to_records(profit_loss),

        "balance_sheet":
            dataframe_to_records(balance_sheet),

        "cash_flow":
            dataframe_to_records(cash_flow),

        "financial_ratios":
            dataframe_to_records(ratios)

    }