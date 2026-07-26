"""
Analytics Router

NIFTY100 Financial Intelligence Platform
"""

from fastapi import APIRouter

from app.services.analytics_service import (
    dashboard_summary,
    top_revenue,
    top_profit,
    sector_distribution,
    latest_financial_year,
    revenue_ranking,
    profit_ranking,
)

router = APIRouter()

# ==========================================================
# Dashboard Summary
# ==========================================================

@router.get(
    "/dashboard",
    summary="Dashboard Summary",
)
def dashboard():
    return dashboard_summary()


# ==========================================================
# Top Revenue Companies
# ==========================================================

@router.get(
    "/top-revenue",
    summary="Top Revenue Companies",
)
def revenue(limit: int = 10):
    return top_revenue(limit)


# ==========================================================
# Top Profit Companies
# ==========================================================

@router.get(
    "/top-profit",
    summary="Top Profit Companies",
)
def profit(limit: int = 10):
    return top_profit(limit)


# ==========================================================
# Sector Distribution
# ==========================================================

@router.get(
    "/sector-distribution",
    summary="Sector Distribution",
)
def sectors():
    return sector_distribution()


# ==========================================================
# Latest Financial Year
# ==========================================================

@router.get(
    "/latest-year",
    summary="Latest Financial Year",
)
def latest_year():
    return {
        "latest_year": latest_financial_year()
    }


# ==========================================================
# Revenue Ranking
# ==========================================================

@router.get(
    "/revenue-ranking",
    summary="Revenue Ranking",
)
def revenue_chart(limit: int = 10):
    return revenue_ranking(limit)


# ==========================================================
# Profit Ranking
# ==========================================================

@router.get(
    "/profit-ranking",
    summary="Profit Ranking",
)
def profit_chart(limit: int = 10):
    return profit_ranking(limit)


# ==========================================================
# Company Analytics
# ==========================================================

@router.get(
    "/company/{company_id}",
    summary="Company Analytics",
)
def company_analytics(company_id: str):

    return {

        "company_id": company_id,

        "revenue": [
            {"year": "2020", "value": 42000},
            {"year": "2021", "value": 47000},
            {"year": "2022", "value": 52000},
            {"year": "2023", "value": 61000},
            {"year": "2024", "value": 69000},
        ],

        "profit": [
            {"year": "2020", "value": 4500},
            {"year": "2021", "value": 5100},
            {"year": "2022", "value": 5800},
            {"year": "2023", "value": 6900},
            {"year": "2024", "value": 7700},
        ],

    }