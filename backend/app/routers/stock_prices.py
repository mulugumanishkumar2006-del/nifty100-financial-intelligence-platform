"""
Stock Prices Router
"""

from fastapi import APIRouter
from fastapi import HTTPException

from app.services.stock_price_service import (

    latest_prices,

    company_price_history,

    latest_price,

    total_stock_records

)

router = APIRouter()


# ==========================================================
# Latest Prices
# ==========================================================

@router.get("/")
def prices(limit: int = 100):

    return latest_prices(limit)


# ==========================================================
# Company History
# ==========================================================

@router.get("/company/{company_id}")
def history(company_id: int):

    data = company_price_history(company_id)

    if len(data) == 0:

        raise HTTPException(

            status_code=404,

            detail="No stock price history found"

        )

    return data


# ==========================================================
# Latest Price
# ==========================================================

@router.get("/latest/{company_id}")
def latest(company_id: int):

    return latest_price(company_id)


# ==========================================================
# Total Records
# ==========================================================

@router.get("/stats/count")
def total():

    return {

        "total_stock_records": total_stock_records()

    }