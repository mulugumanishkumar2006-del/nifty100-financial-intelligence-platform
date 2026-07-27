"""
Company Intelligence Router

NIFTY100 Financial Intelligence Platform
"""


from fastapi import APIRouter, HTTPException

from app.services.health_service import (
    calculate_health_score
)


router = APIRouter()



# ==========================================================
# Health Score API
# ==========================================================


@router.get(
    "/company/{company_id}/health-score",
    summary="Company Health Score"
)
def health_score(company_id: str):


    result = calculate_health_score(
        company_id
    )


    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )


    return result