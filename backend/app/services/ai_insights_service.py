"""
AI Insights Service

NIFTY100 Financial Intelligence Platform
"""

import sqlite3
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE = PROJECT_ROOT / "database" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DATABASE)


# ==========================================================
# Fetch Company Data
# ==========================================================

def get_company_data(company_id: str):
    conn = get_connection()

    company = pd.read_sql_query(
        """
        SELECT *
        FROM companies
        WHERE id=?
        """,
        conn,
        params=(company_id,),
    )

    ratios = pd.read_sql_query(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year DESC
        LIMIT 1
        """,
        conn,
        params=(company_id,),
    )

    pnl = pd.read_sql_query(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id=?
        ORDER BY year DESC
        LIMIT 1
        """,
        conn,
        params=(company_id,),
    )

    balance = pd.read_sql_query(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id=?
        ORDER BY year DESC
        LIMIT 1
        """,
        conn,
        params=(company_id,),
    )

    conn.close()

    if company.empty:
        return None

    return {
        "company": company.iloc[0].to_dict(),
        "ratios": ratios.iloc[0].to_dict() if not ratios.empty else {},
        "profit": pnl.iloc[0].to_dict() if not pnl.empty else {},
        "balance": balance.iloc[0].to_dict() if not balance.empty else {},
    }


# ==========================================================
# Growth Analysis
# ==========================================================

def get_growth_analysis(company_id: str):

    data = get_company_data(company_id)

    if data is None:
        return None

    ratios = data["ratios"]

    roe = ratios.get("return_on_equity_pct", 0)

    if roe >= 20:
        growth = "Excellent Growth"
    elif roe >= 15:
        growth = "Strong Growth"
    elif roe >= 10:
        growth = "Stable Growth"
    else:
        growth = "Weak Growth"

    return {
        "growth_score": roe,
        "growth_analysis": growth,
    }


# ==========================================================
# Risk Analysis
# ==========================================================

def get_risk_analysis(company_id: str):

    data = get_company_data(company_id)

    if data is None:
        return None

    ratios = data["ratios"]

    debt = ratios.get("debt_to_equity", 0)

    if debt < 0.5:
        risk = "Low Risk"
    elif debt < 1:
        risk = "Moderate Risk"
    else:
        risk = "High Risk"

    return {
        "debt_to_equity": debt,
        "risk_level": risk,
    }


# ==========================================================
# Investment Recommendation
# ==========================================================

def get_investment_recommendation(company_id: str):

    growth = get_growth_analysis(company_id)

    risk = get_risk_analysis(company_id)

    if growth is None or risk is None:
        return None

    if (
        growth["growth_score"] >= 15
        and risk["risk_level"] == "Low Risk"
    ):
        recommendation = "Strong Buy"

    elif growth["growth_score"] >= 10:
        recommendation = "Buy"

    elif growth["growth_score"] >= 5:
        recommendation = "Hold"

    else:
        recommendation = "Sell"

    return {
        "recommendation": recommendation,
    }


# ==========================================================
# Complete AI Insights
# ==========================================================

def get_company_ai_insights(company_id: str):

    data = get_company_data(company_id)

    if data is None:
        return None

    growth = get_growth_analysis(company_id)

    risk = get_risk_analysis(company_id)

    recommendation = get_investment_recommendation(company_id)

    return {
        "company": data["company"],
        "growth": growth,
        "risk": risk,
        "recommendation": recommendation,
    }