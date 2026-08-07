"""
AI Chat Service

NIFTY100 Financial Intelligence Platform
Provides company-aware financial responses using the local SQLite database.
"""

import sqlite3
from pathlib import Path

import pandas as pd


# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATABASE = PROJECT_ROOT / "database" / "nifty100.db"


# ==========================================================
# Database Connection
# ==========================================================

def get_connection():
    """
    Create a connection to the NIFTY100 SQLite database.
    """

    if not DATABASE.exists():
        raise FileNotFoundError(
            f"NIFTY100 database not found: {DATABASE}"
        )

    return sqlite3.connect(DATABASE)


# ==========================================================
# Load Company Data
# ==========================================================

def load_companies():
    """
    Load verified company information from SQLite.

    Available columns in the companies table:
        id
        company_name
        company_logo
        chart_link
        about_company
        website
        nse_profile
        bse_profile
        face_value
        book_value
        roce_percentage
        roe_percentage
    """

    connection = get_connection()

    try:
        companies = pd.read_sql_query(
            """
            SELECT
                id,
                company_name,
                about_company,
                website,
                face_value,
                book_value,
                roe_percentage,
                roce_percentage
            FROM companies
            """,
            connection,
        )

        return companies

    finally:
        connection.close()


# ==========================================================
# Safe Value Formatting
# ==========================================================

def format_number(value, prefix=""):
    """
    Safely format numeric database values.
    """

    if pd.isna(value):
        return "N/A"

    try:
        number = float(value)

        if number.is_integer():
            formatted = f"{int(number):,}"
        else:
            formatted = f"{number:,.2f}"

        return f"{prefix}{formatted}"

    except (ValueError, TypeError):
        return str(value)


# ==========================================================
# AI Chat
# ==========================================================

def ask_ai(question: str):
    """
    Process a financial question using NIFTY100 company data.

    Current implementation:
        1. Validates the question.
        2. Loads company data from SQLite.
        3. Identifies a company from the question.
        4. Retrieves available financial metrics.
        5. Generates a company-aware response.

    This is the foundation for the future AI intelligence layer.
    """

    # ------------------------------------------------------
    # Validate question
    # ------------------------------------------------------

    if not question or not question.strip():
        return {
            "success": False,
            "company": None,
            "answer": "Please enter a financial question.",
        }

    original_question = question.strip()

    normalized_question = original_question.lower()

    # ------------------------------------------------------
    # Load companies
    # ------------------------------------------------------

    try:

        companies = load_companies()

    except Exception as exc:

        print(f"❌ Database Error: {exc}")

        return {
            "success": False,
            "company": None,
            "answer": "Unable to access NIFTY100 financial data.",
            "error": str(exc),
        }

    # ------------------------------------------------------
    # Find company
    # ------------------------------------------------------

    for _, row in companies.iterrows():

        company_name = str(
            row["company_name"]
        ).strip()

        company_normalized = company_name.lower()

        if company_normalized in normalized_question:

            # --------------------------------------------------
            # Safely retrieve values
            # --------------------------------------------------

            company_id = (
                str(row["id"])
                if pd.notna(row["id"])
                else None
            )

            book_value = format_number(
                row["book_value"],
                prefix="₹",
            )

            face_value = format_number(
                row["face_value"],
                prefix="₹",
            )

            roe = (
                "N/A"
                if pd.isna(row["roe_percentage"])
                else f"{float(row['roe_percentage']):.2f}%"
            )

            roce = (
                "N/A"
                if pd.isna(row["roce_percentage"])
                else f"{float(row['roce_percentage']):.2f}%"
            )

            # --------------------------------------------------
            # Optional company description
            # --------------------------------------------------

            about_company = row["about_company"]

            if pd.isna(about_company):
                about_company = None
            else:
                about_company = str(about_company).strip()

            # --------------------------------------------------
            # Build financial snapshot
            # --------------------------------------------------

            answer = (
                f"{company_name} financial snapshot:\n\n"
                f"• Book Value: {book_value}\n"
                f"• Face Value: {face_value}\n"
                f"• ROE: {roe}\n"
                f"• ROCE: {roce}\n\n"
                f"This information is based on the financial "
                f"data available in the NIFTY100 database."
            )

            # --------------------------------------------------
            # Add company description when available
            # --------------------------------------------------

            if about_company:

                # Keep the response concise
                description = about_company

                if len(description) > 500:
                    description = description[:500].rstrip() + "..."

                answer += (
                    f"\n\nAbout the company:\n"
                    f"{description}"
                )

            # --------------------------------------------------
            # Return response
            # --------------------------------------------------

            return {
                "success": True,
                "company": company_name,
                "company_id": company_id,
                "answer": answer,
            }

    # ======================================================
    # Company Not Identified
    # ======================================================

    return {
        "success": False,
        "company": None,
        "answer": (
            "I couldn't identify the company from your question.\n\n"
            "Please mention the complete NIFTY100 company name.\n\n"
            "Examples:\n"
            "• Tell me about Reliance\n"
            "• What is the ROE of Infosys?\n"
            "• Give me the financial details of TCS\n"
            "• Tell me about HDFC Bank"
        ),
    }