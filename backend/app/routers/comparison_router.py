"""
Company Comparison Router
"""

from fastapi import APIRouter, HTTPException

from app.services.company_service import (
    compare_companies,
    get_peer_companies,
    get_peer_comparison,
)

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


# ==========================================================
# Get Peer Companies
# ==========================================================

@router.get("/peers/{company_id}")
def peer_companies(company_id: str):

    peers = get_peer_companies(company_id)

    if not peers:
        raise HTTPException(
            status_code=404,
            detail="No peer companies found."
        )

    return peers


# ==========================================================
# Peer Comparison
# ==========================================================

@router.get("/peer-comparison/{company_id}")
def peer_comparison(company_id: str):

    comparison = get_peer_comparison(company_id)

    if not comparison:
        raise HTTPException(
            status_code=404,
            detail="Peer comparison data not found."
        )

    return comparison