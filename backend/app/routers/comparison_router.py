"""
Company Comparison Router
"""

from fastapi import APIRouter, HTTPException

from app.services.company_service import compare_companies

router = APIRouter(
    prefix="/comparison",
    tags=["Company Comparison"],
)


# ==========================================================
# Compare Two Companies
# ==========================================================

@router.get("/")
def compare(company1: str, company2: str):

    companies = compare_companies(company1, company2)

    if len(companies) < 2:
        raise HTTPException(
            status_code=404,
            detail="One or both companies not found."
        )

    return companies