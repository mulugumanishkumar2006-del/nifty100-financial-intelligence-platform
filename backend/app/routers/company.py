from fastapi import APIRouter
from app.services.company_service import (
    get_all_companies,
    get_company
)

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


@router.get("/")
def fetch_all_companies():
    return get_all_companies()


@router.get("/{company_id}")
def fetch_company(company_id: int):
    return get_company(company_id)