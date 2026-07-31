"""
AI Intelligence Router
"""

from fastapi import APIRouter, HTTPException

from app.services.intelligence_service import (
    calculate_health_score,
    investment_recommendation,
    ai_summary,
)

router = APIRouter(
    prefix="/intelligence",
    tags=["AI Intelligence"],
)


# ==========================================================
# Health Score
# ==========================================================

@router.get("/health-score/{company_id}")
def health_score(company_id: str):

    result = calculate_health_score(company_id)

    if result["health_score"] == 0:
        raise HTTPException(
            status_code=404,
            detail="Company not found.",
        )

    return result


# ==========================================================
# Recommendation
# ==========================================================

@router.get("/recommendation/{company_id}")
def recommendation(company_id: str):

    result = investment_recommendation(company_id)

    if result["health_score"] == 0:
        raise HTTPException(
            status_code=404,
            detail="Company not found.",
        )

    return result


# ==========================================================
# Summary
# ==========================================================

@router.get("/summary/{company_id}")
def summary(company_id: str):

    result = ai_summary(company_id)

    return result