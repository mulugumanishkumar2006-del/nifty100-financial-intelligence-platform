"""
Company Insight Router
"""

from fastapi import APIRouter

from app.services.company_insight_service import (
    get_health_score,
    get_recommendation,
    get_ai_summary,
    get_company_insights,
)

router = APIRouter(
    prefix="/intelligence",
    tags=["AI Intelligence"],
)


@router.get("/health-score/{company_id}")
def health_score(company_id: str):
    return get_health_score(company_id)


@router.get("/recommendation/{company_id}")
def recommendation(company_id: str):
    return get_recommendation(company_id)


@router.get("/summary/{company_id}")
def summary(company_id: str):
    return get_ai_summary(company_id)


@router.get("/company/{company_id}")
def company_insights(company_id: str):
    return get_company_insights(company_id)