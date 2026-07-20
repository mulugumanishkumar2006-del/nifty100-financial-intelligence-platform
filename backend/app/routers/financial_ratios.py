"""
Financial Ratios Router

NIFTY100 Financial Intelligence Platform
"""

from fastapi import APIRouter
from fastapi import HTTPException

from app.services.ratio_service import (
    get_latest_ratios,
    get_company_ratios,
    latest_year,
    top_roe,
    top_asset_turnover
)

router = APIRouter()


# ==========================================================
# Get All Financial Ratios
# ==========================================================

@router.get(
    "/",
    summary="Get Financial Ratios"
)
def fetch_ratios():

    return get_latest_ratios()


# ==========================================================
# Get Company Financial Ratios
# ==========================================================

@router.get(
    "/company/{company_id}",
    summary="Get Company Financial Ratios"
)
def fetch_company_ratios(company_id: int):

    data = get_company_ratios(company_id)

    if len(data) == 0:

        raise HTTPException(

            status_code=404,

            detail="Financial ratios not found"

        )

    return data


# ==========================================================
# Latest Financial Year
# ==========================================================

@router.get(
    "/latest-year",
    summary="Latest Financial Year"
)
def fetch_latest_year():

    return {

        "latest_year": latest_year()

    }


# ==========================================================
# Top ROE Companies
# ==========================================================

@router.get(
    "/top-roe",
    summary="Top ROE Companies"
)
def fetch_top_roe(limit: int = 10):

    return top_roe(limit)


# ==========================================================
# Top Asset Turnover Companies
# ==========================================================

@router.get(
    "/top-asset-turnover",
    summary="Top Asset Turnover Companies"
)
def fetch_top_asset_turnover(limit: int = 10):

    return top_asset_turnover(limit)