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


    dataframe = pd.read_sql_query(
        query,
        connection
    )


    connection.close()


    return dataframe_to_records(dataframe)




# ==========================================================
# Get Single Company Complete Details
# ==========================================================

def get_company(company_id: str):


    connection = get_connection()


    # -----------------------------
    # Company Information
    # -----------------------------

    company_query = """

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



    company_df = pd.read_sql_query(

        company_query,

        connection,

        params=(company_id,)

    )



    if company_df.empty:

        connection.close()

        return None



    company = dataframe_to_records(
        company_df
    )[0]



    # -----------------------------
    # Profit Loss
    # -----------------------------


    profit_loss_query = """

    SELECT *

    FROM profitandloss

    WHERE company_id = ?

    ORDER BY year

    """



    profit_loss_df = pd.read_sql_query(

        profit_loss_query,

        connection,

        params=(company_id,)

    )



    # -----------------------------
    # Balance Sheet
    # -----------------------------


    balance_query = """

    SELECT *

    FROM balancesheet

    WHERE company_id = ?

    ORDER BY year

    """



    balance_df = pd.read_sql_query(

        balance_query,

        connection,

        params=(company_id,)

    )




    # -----------------------------
    # Cash Flow
    # -----------------------------


    cashflow_query = """

    SELECT *

    FROM cashflow

    WHERE company_id = ?

    ORDER BY year

    """



    cashflow_df = pd.read_sql_query(

        cashflow_query,

        connection,

        params=(company_id,)

    )





    # -----------------------------
    # Financial Ratios
    # -----------------------------


    ratio_query = """

    SELECT *

    FROM financial_ratios

    WHERE company_id = ?

    ORDER BY year

    """



    ratio_df = pd.read_sql_query(

        ratio_query,

        connection,

        params=(company_id,)

    )




    connection.close()



    return {


        "company": company,


        "profit_loss":
            dataframe_to_records(
                profit_loss_df
            ),


        "balance_sheet":
            dataframe_to_records(
                balance_df
            ),


        "cash_flow":
            dataframe_to_records(
                cashflow_df
            ),


        "financial_ratios":
            dataframe_to_records(
                ratio_df
            )

    }





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



    return dataframe_to_records(
        dataframe
    )





# ==========================================================
# Company Count
# ==========================================================

def total_companies():


    connection = get_connection()


    dataframe = pd.read_sql_query(

        """
        SELECT COUNT(*) AS total
        FROM companies;
        """,

        connection

    )


    connection.close()



    return int(
        dataframe.iloc[0]["total"]
    )






# ==========================================================
# Company Statistics
# ==========================================================

def company_statistics():


    connection = get_connection()


    dataframe = pd.read_sql_query(

        """

        SELECT

            COUNT(*) AS total_companies,

            COUNT(DISTINCT website)
            AS companies_with_website


        FROM companies;

        """,

        connection

    )


    connection.close()



    records = dataframe_to_records(
        dataframe
    )


    return records[0] if records else {}






# ==========================================================
# Compare Companies
# ==========================================================

def compare_companies(
        company1: str,
        company2: str
):


    connection = get_connection()



    query = """

    SELECT

        id,
        company_name,
        face_value,
        book_value,
        roce_percentage,
        roe_percentage


    FROM companies


    WHERE id IN (?,?)


    """



    dataframe = pd.read_sql_query(

        query,

        connection,

        params=(
            company1,
            company2
        )

    )



    connection.close()



    return dataframe_to_records(
        dataframe
    )