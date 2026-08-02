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
# Latest Financial Ratio
# ==========================================================

def get_company_financial_data(company_id: str):

    connection = get_connection()

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id=?
    ORDER BY year DESC
    LIMIT 1
    """

    dataframe = pd.read_sql_query(
        query,
        connection,
        params=(company_id,)
    )

    connection.close()

    if dataframe.empty:
        return None

    return dataframe.iloc[0].to_dict()


# ==========================================================
# Health Score
# ==========================================================

def calculate_health_score(company_id: str):

    data = get_company_financial_data(company_id)

    if data is None:
        return {
            "company_id": company_id,
            "health_score": 0,
            "grade": "Unknown"
        }

    score = 0

    roe = float(data.get("return_on_equity_pct") or 0)
    debt = float(data.get("debt_to_equity") or 0)
    interest = float(data.get("interest_coverage") or 0)
    margin = float(data.get("net_profit_margin_pct") or 0)
    asset = float(data.get("asset_turnover") or 0)

    # ROE
    if roe >= 20:
        score += 20
    elif roe >= 15:
        score += 15
    elif roe >= 10:
        score += 10

    # Debt
    if debt <= 0.5:
        score += 20
    elif debt <= 1:
        score += 15
    elif debt <= 2:
        score += 10

    # Interest Coverage
    if interest >= 10:
        score += 20
    elif interest >= 5:
        score += 15
    elif interest >= 2:
        score += 10

    # Net Profit Margin
    if margin >= 20:
        score += 20
    elif margin >= 10:
        score += 15
    elif margin >= 5:
        score += 10

    # Asset Turnover
    if asset >= 2:
        score += 20
    elif asset >= 1:
        score += 15
    elif asset >= 0.5:
        score += 10

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
# Recommendation
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
            "The company has excellent financial strength with healthy profitability, "
            "strong returns and manageable debt."
        )
    elif score >= 60:
        summary = (
            "The company shows good financial performance with stable fundamentals."
        )
    elif score >= 40:
        summary = (
            "The company has average financial health. Investors should perform additional analysis."
        )
    else:
        summary = (
            "The company has weak financial indicators and higher investment risk."
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