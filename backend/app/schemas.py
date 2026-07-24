from pydantic import BaseModel


# ==========================================================
# Company
# ==========================================================

class CompanyResponse(BaseModel):
    id: str
    company_name: str

    website: str | None = None
    about_company: str | None = None

    face_value: float | None = None
    book_value: float | None = None

    roce_percentage: float | None = None
    roe_percentage: float | None = None

    class Config:
        from_attributes = True


# ==========================================================
# Dashboard
# ==========================================================

class DashboardResponse(BaseModel):
    total_companies: int
    total_sectors: int
    latest_financial_year: str


# ==========================================================
# Revenue
# ==========================================================

class RevenueResponse(BaseModel):
    company_name: str
    sales: float


# ==========================================================
# Profit
# ==========================================================

class ProfitResponse(BaseModel):
    company_name: str
    net_profit: float