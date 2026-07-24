from fastapi import APIRouter, HTTPException

from app.schemas import CompanyResponse

from app.services.company_service import (
    get_all_companies,
    get_company,
)

router = APIRouter()


# ==========================================================
# Get All Companies
# ==========================================================

@router.get(
    "/companies/",
    response_model=list[CompanyResponse],
    summary="Fetch All Companies"
)
def fetch_all_companies():
    return get_all_companies()


# ==========================================================
# Get Company By ID
# ==========================================================

@router.get(
    "/companies/{company_id}",
    response_model=CompanyResponse,
    summary="Fetch Company By ID"
)
def fetch_company(company_id: str):

    company = get_company(company_id)

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return company