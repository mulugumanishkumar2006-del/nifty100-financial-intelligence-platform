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

@router.get("/dashboard")
def dashboard():
    return dashboard_summary()


# ==========================================================
# Revenue Ranking
# ==========================================================

@router.get("/revenue-ranking")
def revenue(limit: int = 10):
    return revenue_ranking(limit)


# ==========================================================
# Profit Ranking
# ==========================================================

@router.get("/profit-ranking")
def profit(limit: int = 10):
    return profit_ranking(limit)


# ==========================================================
# Top Revenue
# ==========================================================

@router.get("/top-revenue")
def top_rev(limit: int = 10):
    return top_revenue(limit)


# ==========================================================
# Top Profit
# ==========================================================

@router.get("/top-profit")
def top_prof(limit: int = 10):
    return top_profit(limit)


# ==========================================================
# Sector Distribution
# ==========================================================

@router.get("/sector-distribution")
def sectors():
    return sector_distribution()


# ==========================================================
# Latest Financial Year
# ==========================================================

@router.get("/latest-year")
def latest():
    return {
        "latest_year": latest_financial_year()
    }


# ==========================================================
# Company Analytics
# ==========================================================

@router.get("/company/{company_id}")
def company(company_id: str):

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