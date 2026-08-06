"""
AI Chat Service

NIFTY100 Financial Intelligence Platform
"""

import sqlite3
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE = PROJECT_ROOT / "database" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def ask_ai(question: str):

    connection = get_connection()

    companies = pd.read_sql_query(
        """
        SELECT
            id,
            company_name,
            market_cap,
            book_value,
            face_value,
            roe_percentage,
            roce_percentage
        FROM companies
        """,
        connection,
    )

    connection.close()

    question = question.lower()

    for _, row in companies.iterrows():

        company = str(row["company_name"]).lower()

        if company in question:

            return {
                "success": True,
                "company": row["company_name"],
                "answer": (
                    f"{row['company_name']} has a Market Cap of {row['market_cap']}, "
                    f"Book Value {row['book_value']}, "
                    f"Face Value {row['face_value']}, "
                    f"ROE {row['roe_percentage']}%, "
                    f"ROCE {row['roce_percentage']}%."
                ),
            }

    return {
        "success": False,
        "answer": (
            "I couldn't identify the company. "
            "Please ask using the complete company name."
        ),
    }