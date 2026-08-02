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


@router.get("/")
def get_latest_stock_prices(limit: int = 100):
    return latest_prices(limit)


@router.get("/company/{company_id}")
def get_company_history(company_id: str):

    data = company_price_history(company_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="No stock price history found."
        )

    return data


@router.get("/latest/{company_id}")
def get_latest_company_price(company_id: str):

    data = latest_price(company_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Company not found."
        )

    return data


@router.get("/stats/count")
def get_total_stock_records():

    return {
        "total_stock_records": total_stock_records()
    }