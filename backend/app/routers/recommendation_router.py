"""
AI Stock Recommendation Router

NIFTY100 Financial Intelligence Platform
Day 23
"""

from fastapi import APIRouter, HTTPException

from app.services.recommendation_service import (
    generate_recommendation,
)


# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    prefix="/recommendations",
    tags=["AI Stock Recommendations"],
)


# ==========================================================
# Get Recommendation
# ==========================================================

@router.get("/{company_id}")
def get_recommendation(company_id: str):

    result = generate_recommendation(company_id)

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Company not found.",
        )

    return result