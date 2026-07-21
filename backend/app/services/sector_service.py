"""
Sector Service

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
# Get All Sectors
# ==========================================================

def get_all_sectors():

    connection = get_connection()

    query = """

    SELECT DISTINCT

        broad_sector

    FROM sectors

    ORDER BY broad_sector

    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe_to_records(dataframe)


# ==========================================================
# Companies in Sector
# ==========================================================

def companies_in_sector(sector_name):

    connection = get_connection()

    query = """

    SELECT

        c.id,

        c.company_name,

        s.broad_sector

    FROM companies c

    JOIN sectors s

    ON c.id=s.company_id

    WHERE s.broad_sector=?

    ORDER BY c.company_name

    """

    dataframe = pd.read_sql_query(

        query,

        connection,

        params=(sector_name,)

    )

    connection.close()

    return dataframe_to_records(dataframe)


# ==========================================================
# Sector Summary
# ==========================================================

def sector_summary():

    connection = get_connection()

    query = """

    SELECT

        broad_sector,

        COUNT(*) AS companies

    FROM sectors

    GROUP BY broad_sector

    ORDER BY companies DESC

    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe_to_records(dataframe)


# ==========================================================
# Total Sectors
# ==========================================================

def total_sectors():

    connection = get_connection()

    query = """

    SELECT

        COUNT(DISTINCT broad_sector)

        AS total

    FROM sectors

    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return int(dataframe.iloc[0]["total"])