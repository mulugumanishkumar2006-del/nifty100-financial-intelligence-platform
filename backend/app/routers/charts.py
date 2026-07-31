"""
Charts Router

Provides APIs for Dashboard Charts
"""

from fastapi import APIRouter

from app.services.chart_service import (
    get_revenue_trend,
    get_roe_trend,
    get_market_cap,
    get_sector_distribution,
    get_stock_history,
)

router = APIRouter(
    prefix="/charts",
    tags=["Charts"],
)

# ==========================================================
# Revenue Trend
# ==========================================================

@router.get("/revenue/{company_id}")
def revenue(company_id: str):
    return get_revenue_trend(company_id)


# ==========================================================
# ROE Trend
# ==========================================================

@router.get("/roe/{company_id}")
def roe(company_id: str):
    return get_roe_trend(company_id)


# ==========================================================
# Market Cap
# ==========================================================

@router.get("/market-cap")
def market_cap():
    return get_market_cap()


# ==========================================================
# Sector Distribution
# ==========================================================

@router.get("/sector-distribution")
def sectors():
    return get_sector_distribution()


# ==========================================================
# Stock History
# ==========================================================

@router.get("/stock-history/{company_id}")
def stock_history(company_id: str):
    return get_stock_history(company_id)