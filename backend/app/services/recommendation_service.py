"""
AI Stock Recommendation Service

NIFTY100 Financial Intelligence Platform
Day 23
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
# Utility
# ==========================================================

def safe_number(value, default=0.0):
    """
    Safely convert database values into numbers.
    """

    if value is None:
        return default

    try:
        if pd.isna(value):
            return default

        return float(value)

    except (TypeError, ValueError):
        return default


# ==========================================================
# Get Company Financial Data
# ==========================================================

def get_company_financial_data(company_id: str):

    connection = get_connection()

    try:

        company = pd.read_sql_query(
            """
            SELECT
                id,
                company_name,
                face_value,
                book_value,
                roe_percentage,
                roce_percentage
            FROM companies
            WHERE id = ?
            """,
            connection,
            params=(company_id,),
        )

        if company.empty:
            return None

        company_data = company.iloc[0].to_dict()

        # --------------------------------------------------
        # Profit & Loss
        # --------------------------------------------------

        profit_loss = pd.read_sql_query(
            """
            SELECT *
            FROM profitandloss
            WHERE company_id = ?
            ORDER BY year DESC
            """,
            connection,
            params=(company_id,),
        )

        # --------------------------------------------------
        # Balance Sheet
        # --------------------------------------------------

        balance_sheet = pd.read_sql_query(
            """
            SELECT *
            FROM balancesheet
            WHERE company_id = ?
            ORDER BY year DESC
            """,
            connection,
            params=(company_id,),
        )

        # --------------------------------------------------
        # Cash Flow
        # --------------------------------------------------

        cash_flow = pd.read_sql_query(
            """
            SELECT *
            FROM cashflow
            WHERE company_id = ?
            ORDER BY year DESC
            """,
            connection,
            params=(company_id,),
        )

        return {
            "company": company_data,
            "profit_loss": profit_loss,
            "balance_sheet": balance_sheet,
            "cash_flow": cash_flow,
        }

    finally:

        connection.close()


# ==========================================================
# Growth Score
# ==========================================================

def calculate_growth_score(profit_loss):

    if profit_loss.empty:
        return 0

    score = 0

    # Latest two years
    if len(profit_loss) >= 2:

        latest = profit_loss.iloc[0]
        previous = profit_loss.iloc[1]

        latest_sales = safe_number(
            latest.get("sales")
        )

        previous_sales = safe_number(
            previous.get("sales")
        )

        latest_profit = safe_number(
            latest.get("net_profit")
        )

        previous_profit = safe_number(
            previous.get("net_profit")
        )

        # Sales growth
        if previous_sales > 0:

            sales_growth = (
                (latest_sales - previous_sales)
                / previous_sales
            ) * 100

            if sales_growth >= 15:
                score += 2

            elif sales_growth >= 5:
                score += 1

        # Profit growth
        if previous_profit > 0:

            profit_growth = (
                (latest_profit - previous_profit)
                / previous_profit
            ) * 100

            if profit_growth >= 15:
                score += 2

            elif profit_growth >= 5:
                score += 1

    return min(score, 4)


# ==========================================================
# Profitability Score
# ==========================================================

def calculate_profitability_score(company):

    roe = safe_number(
        company.get("roe_percentage")
    )

    roce = safe_number(
        company.get("roce_percentage")
    )

    score = 0

    # ROE
    if roe >= 20:
        score += 2

    elif roe >= 12:
        score += 1

    # ROCE
    if roce >= 20:
        score += 2

    elif roce >= 12:
        score += 1

    return min(score, 4)


# ==========================================================
# Financial Health Score
# ==========================================================

def calculate_financial_health_score(balance_sheet):

    if balance_sheet.empty:
        return 0

    latest = balance_sheet.iloc[0]

    score = 0

    assets = safe_number(
        latest.get("total_assets")
    )

    liabilities = safe_number(
        latest.get("total_liabilities")
    )

    borrowings = safe_number(
        latest.get("borrowings")
    )

    # Asset / liability strength
    if assets > 0 and liabilities > 0:

        liability_ratio = liabilities / assets

        if liability_ratio < 0.40:
            score += 2

        elif liability_ratio < 0.60:
            score += 1

    # Borrowings
    if borrowings <= 0:
        score += 2

    return min(score, 4)


# ==========================================================
# Risk Score
# ==========================================================

def calculate_risk_score(balance_sheet):

    if balance_sheet.empty:
        return 2

    latest = balance_sheet.iloc[0]

    assets = safe_number(
        latest.get("total_assets")
    )

    liabilities = safe_number(
        latest.get("total_liabilities")
    )

    if assets <= 0:
        return 2

    liability_ratio = liabilities / assets

    if liability_ratio < 0.40:
        return 1

    if liability_ratio < 0.60:
        return 2

    return 3


# ==========================================================
# Recommendation
# ==========================================================

def generate_recommendation(company_id: str):

    data = get_company_financial_data(company_id)

    if data is None:
        return None

    company = data["company"]
    profit_loss = data["profit_loss"]
    balance_sheet = data["balance_sheet"]

    growth_score = calculate_growth_score(
        profit_loss
    )

    profitability_score = calculate_profitability_score(
        company
    )

    financial_health_score = calculate_financial_health_score(
        balance_sheet
    )

    risk_score = calculate_risk_score(
        balance_sheet
    )

    # --------------------------------------------------
    # Total Score
    # --------------------------------------------------

    total_score = (
        growth_score
        + profitability_score
        + financial_health_score
        - risk_score
    )

    total_score = max(
        0,
        min(total_score, 12)
    )

    # --------------------------------------------------
    # Recommendation
    # --------------------------------------------------

    if total_score >= 9:

        recommendation = "BUY"

    elif total_score >= 6:

        recommendation = "HOLD"

    else:

        recommendation = "AVOID"

    # --------------------------------------------------
    # Confidence
    # --------------------------------------------------

    confidence = round(
        (total_score / 12) * 100,
        2,
    )

    # --------------------------------------------------
    # Reasoning
    # --------------------------------------------------

    reasons = []

    roe = safe_number(
        company.get("roe_percentage")
    )

    roce = safe_number(
        company.get("roce_percentage")
    )

    if roe >= 20:
        reasons.append(
            "Strong return on equity"
        )

    elif roe >= 12:
        reasons.append(
            "Healthy return on equity"
        )

    if roce >= 20:
        reasons.append(
            "Strong return on capital employed"
        )

    elif roce >= 12:
        reasons.append(
            "Healthy return on capital employed"
        )

    if growth_score >= 3:
        reasons.append(
            "Positive business growth indicators"
        )

    if financial_health_score >= 3:
        reasons.append(
            "Healthy balance-sheet profile"
        )

    if risk_score <= 1:
        reasons.append(
            "Relatively low financial risk"
        )

    if not reasons:
        reasons.append(
            "Financial indicators require further analysis"
        )

    return {
        "company_id": company_id,
        "company_name": company.get("company_name"),
        "recommendation": recommendation,
        "confidence": confidence,
        "score": total_score,
        "max_score": 12,
        "growth_score": growth_score,
        "profitability_score": profitability_score,
        "financial_health_score": financial_health_score,
        "risk_score": risk_score,
        "reasons": reasons,
    }