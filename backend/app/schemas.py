"""
Pydantic Schemas

NIFTY100 Financial Intelligence Platform
"""

from typing import Optional
from pydantic import BaseModel


# ==========================================================
# Company
# ==========================================================

class CompanyResponse(BaseModel):
    id: str
    company_name: str

    website: Optional[str] = None
    about_company: Optional[str] = None

    face_value: Optional[float] = None
    book_value: Optional[float] = None

    roce_percentage: Optional[float] = None
    roe_percentage: Optional[float] = None

    class Config:
        from_attributes = True


# ==========================================================
# Dashboard
# ==========================================================

class DashboardResponse(BaseModel):
    companies: int
    total_revenue: float
    total_profit: float
    average_roe: float
    average_roce: float
    latest_year: str
    total_sectors: int


# ==========================================================
# Revenue Ranking
# ==========================================================

class RevenueResponse(BaseModel):
    company_name: str
    sales: float


# ==========================================================
# Profit Ranking
# ==========================================================

class ProfitResponse(BaseModel):
    company_name: str
    net_profit: float


# ==========================================================
# Sector
# ==========================================================

class SectorResponse(BaseModel):
    broad_sector: str
    companies: Optional[int] = None


# ==========================================================
# Stock Price
# ==========================================================

class StockPriceResponse(BaseModel):
    company_id: str
    company_name: str

    date: str

    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    close_price: Optional[float] = None

    volume: Optional[int] = None


# ==========================================================
# Financial Ratio
# ==========================================================

class FinancialRatioResponse(BaseModel):
    company_id: str
    year: str

    return_on_equity_pct: Optional[float] = None
    return_on_capital_employed_pct: Optional[float] = None

    current_ratio: Optional[float] = None
    debt_to_equity: Optional[float] = None

    asset_turnover: Optional[float] = None
    pe_ratio: Optional[float] = None


# ==========================================================
# Revenue Chart
# ==========================================================

class RevenueChartResponse(BaseModel):
    year: str
    sales: float


# ==========================================================
# ROE Chart
# ==========================================================

class ROEChartResponse(BaseModel):
    year: str
    roe: float


# ==========================================================
# Stock History
# ==========================================================

class StockHistoryResponse(BaseModel):
    date: str
    close: float


# ==========================================================
# AI Health Score
# ==========================================================

class HealthScoreResponse(BaseModel):
    company_id: str
    health_score: int
    grade: str


# ==========================================================
# AI Recommendation
# ==========================================================

class RecommendationResponse(BaseModel):
    company_id: str
    health_score: int
    recommendation: str


# ==========================================================
# AI Summary
# ==========================================================

class AISummaryResponse(BaseModel):
    company_id: str
    health_score: int
    risk: str
    summary: str