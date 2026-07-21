"""
Sector Router
"""

from fastapi import APIRouter
from app.services.sector_service import (
    get_all_sectors,
    companies_in_sector,
    sector_summary,
    total_sectors
)

router = APIRouter(
    prefix="/sectors",
    tags=["Sectors"]
)


# ==========================================================
# Get All Sectors
# ==========================================================

@router.get("/")
def sectors():

    return get_all_sectors()


# ==========================================================
# Sector Summary
# ==========================================================

@router.get("/summary")
def summary():

    return sector_summary()


# ==========================================================
# Companies by Sector
# ==========================================================

@router.get("/{sector_name}")
def companies(sector_name: str):

    return companies_in_sector(sector_name)


# ==========================================================
# Total Sectors
# ==========================================================

@router.get("/stats/count")
def count():

    return {

        "total_sectors": total_sectors()

    }