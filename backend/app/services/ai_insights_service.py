"""
AI Insights Router

NIFTY100 Financial Intelligence Platform
"""

from fastapi import APIRouter, HTTPException

from app.services.ai_insights_service import (
    get_company_ai_insights,
    get_growth_analysis,
    get_risk_analysis,
    get_investment_recommendation,
)

router = APIRouter(
    prefix="/ai",
    tags=["AI Insights"],
)

# ==========================================================
# Complete AI Insights
# ==========================================================

@router.get("/company/{company_id}")
def company_ai(company_id: str):
    result = get_company_ai_insights(company_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found."
        )

    return result


# ==========================================================
# Growth Analysis
# ==========================================================

@router.get("/growth/{company_id}")
def growth_analysis(company_id: str):
    result = get_growth_analysis(company_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found."
        )

    return result


# ==========================================================
# Risk Analysis
# ==========================================================

@router.get("/risk/{company_id}")
def risk_analysis(company_id: str):
    result = get_risk_analysis(company_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found."
        )

    return result


# ==========================================================
# Investment Recommendation
# ==========================================================

@router.get("/recommendation/{company_id}")
def recommendation(company_id: str):
    result = get_investment_recommendation(company_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found."
        )

    return result