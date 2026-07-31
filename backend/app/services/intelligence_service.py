"""
AI Intelligence Service

NIFTY100 Financial Intelligence Platform
"""

import sqlite3
from pathlib import Path
import pandas as pd

# ==========================================================
# Database
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATABASE = PROJECT_ROOT / "database" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DATABASE)


# ==========================================================
# Fetch Company Financial Data
# ==========================================================

def get_company_financial_data(company_id: str):
    """
    Fetch latest financial ratios for a company.
    """

    connection = get_connection()

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year DESC
    LIMIT 1
    """

    dataframe = pd.read_sql_query(
        query,
        connection,
        params=(company_id,),
    )

    connection.close()

    if dataframe.empty:
        return None

    return dataframe.iloc[0].to_dict()


# ==========================================================
# Calculate Health Score
# ==========================================================

def calculate_health_score(company_id: str):

    data = get_company_financial_data(company_id)

    if data is None:
        return {
            "company_id": company_id,
            "health_score": 0,
            "grade": "Unknown",
        }

    score = 0

    roe = float(data.get("roe", 0) or 0)
    roce = float(data.get("roce", 0) or 0)
    current_ratio = float(data.get("current_ratio", 0) or 0)
    debt_equity = float(data.get("debt_to_equity", 0) or 0)
    pe_ratio = float(data.get("pe_ratio", 0) or 0)

    # ROE
    if roe >= 20:
        score += 20
    elif roe >= 15:
        score += 15
    elif roe >= 10:
        score += 10

    # ROCE
    if roce >= 20:
        score += 20
    elif roce >= 15:
        score += 15
    elif roce >= 10:
        score += 10

    # Current Ratio
    if current_ratio >= 2:
        score += 20
    elif current_ratio >= 1:
        score += 15

    # Debt to Equity
    if debt_equity <= 0.5:
        score += 20
    elif debt_equity <= 1:
        score += 15
    elif debt_equity <= 2:
        score += 10

    # PE Ratio
    if pe_ratio <= 25:
        score += 20
    elif pe_ratio <= 40:
        score += 15

    # Grade
    if score >= 80:
        grade = "Excellent"
    elif score >= 60:
        grade = "Good"
    elif score >= 40:
        grade = "Average"
    else:
        grade = "Poor"

    return {
        "company_id": company_id,
        "health_score": score,
        "grade": grade,
    }


# ==========================================================
# Investment Recommendation
# ==========================================================

def investment_recommendation(company_id: str):

    result = calculate_health_score(company_id)

    score = result["health_score"]

    if score >= 80:
        recommendation = "BUY"
    elif score >= 60:
        recommendation = "HOLD"
    else:
        recommendation = "SELL"

    return {
        "company_id": company_id,
        "health_score": score,
        "recommendation": recommendation,
    }


# ==========================================================
# AI Summary
# ==========================================================

def ai_summary(company_id: str):

    result = calculate_health_score(company_id)

    score = result["health_score"]

    if score >= 80:
        summary = (
            "This company demonstrates excellent financial health with strong profitability, "
            "healthy return ratios, manageable debt levels and appears suitable for long-term investment."
        )

    elif score >= 60:
        summary = (
            "This company has stable financial performance with moderate growth potential. "
            "Investors may consider holding while monitoring future results."
        )

    elif score >= 40:
        summary = (
            "The company has average financial strength. Additional analysis is recommended "
            "before making an investment decision."
        )

    else:
        summary = (
            "The company shows weak financial indicators and higher investment risk. "
            "Careful evaluation is recommended."
        )

    risk = (
        "Low"
        if score >= 80
        else "Medium"
        if score >= 60
        else "High"
    )

    return {
        "company_id": company_id,
        "health_score": score,
        "risk": risk,
        "summary": summary,
    }