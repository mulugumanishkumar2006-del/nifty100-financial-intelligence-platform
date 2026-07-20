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
    latest_financial_year
)

router = APIRouter()


# ==========================================================
# Dashboard Summary
# ==========================================================

@router.get(
    "/dashboard",
    summary="Dashboard Summary"
)
def dashboard():

    return dashboard_summary()


# ==========================================================
# Top Revenue Companies
# ==========================================================

@router.get(
    "/top-revenue",
    summary="Top Revenue Companies"
)
def revenue(limit: int = 10):

    return top_revenue(limit)


# ==========================================================
# Top Profit Companies
# ==========================================================

@router.get(
    "/top-profit",
    summary="Top Profit Companies"
)
def profit(limit: int = 10):

    return top_profit(limit)


# ==========================================================
# Sector Distribution
# ==========================================================

@router.get(
    "/sector-distribution",
    summary="Sector Distribution"
)
def sectors():

    return sector_distribution()


# ==========================================================
# Latest Financial Year
# ==========================================================

@router.get(
    "/latest-year",
    summary="Latest Financial Year"
)
def latest_year():

    return {

        "latest_year": latest_financial_year()

    }