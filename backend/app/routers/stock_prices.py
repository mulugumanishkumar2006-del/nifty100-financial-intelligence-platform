"""
Stock Prices Router
"""

from fastapi import APIRouter, HTTPException

from app.services.stock_price_service import (
    latest_prices,
    company_price_history,
    latest_price,
    total_stock_records,
)

router = APIRouter(
    prefix="/stock-prices",
    tags=["Stock Prices"],
)


# ==========================================================
# Get Latest Stock Prices
# Endpoint:
# GET /api/stock-prices
# ==========================================================

@router.get("/")
def get_latest_stock_prices(limit: int = 100):
    """
    Returns latest stock prices for all companies.
    """
    return latest_prices(limit)


# ==========================================================
# Company Price History
# Endpoint:
# GET /api/stock-prices/company/{company_id}
# ==========================================================

@router.get("/company/{company_id}")
def get_company_history(company_id: int):
    """
    Returns historical stock prices of one company.
    """

    data = company_price_history(company_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="No stock price history found.",
        )

    return data


# ==========================================================
# Latest Price of One Company
# Endpoint:
# GET /api/stock-prices/latest/{company_id}
# ==========================================================

@router.get("/latest/{company_id}")
def get_latest_company_price(company_id: int):
    """
    Returns latest stock price of a company.
    """
    return latest_price(company_id)


# ==========================================================
# Total Stock Records
# Endpoint:
# GET /api/stock-prices/stats/count
# ==========================================================

@router.get("/stats/count")
def get_total_stock_records():
    """
    Returns total stock records in database.
    """
    return {
        "total_stock_records": total_stock_records()
    }