"""
Pydantic Schemas

NIFTY100 Financial Intelligence Platform
"""

from pydantic import BaseModel
from typing import Optional


# ==========================================================
# Company
# ==========================================================

class CompanySchema(BaseModel):

    id: int
    company_name: str
    ticker: Optional[str] = None
    isin: Optional[str] = None
    market_cap: Optional[float] = None

    class Config:
        from_attributes = True


# ==========================================================
# Sector
# ==========================================================

class SectorSchema(BaseModel):

    company_id: int
    broad_sector: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None

    class Config:
        from_attributes = True


# ==========================================================
# Financial Ratios
# ==========================================================

class FinancialRatioSchema(BaseModel):

    company_id: int
    year: int

    return_on_equity_pct: Optional[float] = None
    debt_to_equity: Optional[float] = None
    interest_coverage: Optional[float] = None
    asset_turnover: Optional[float] = None
    revenue_cagr_5yr: Optional[float] = None
    pat_cagr_5yr: Optional[float] = None
    composite_quality_score: Optional[float] = None

    class Config:
        from_attributes = True


# ==========================================================
# Profit & Loss
# ==========================================================

class ProfitLossSchema(BaseModel):

    company_id: int
    year: int

    sales: Optional[float] = None
    operating_profit: Optional[float] = None
    net_profit: Optional[float] = None
    eps: Optional[float] = None

    class Config:
        from_attributes = True


# ==========================================================
# Balance Sheet
# ==========================================================

class BalanceSheetSchema(BaseModel):

    company_id: int
    year: int

    equity_capital: Optional[float] = None
    reserves: Optional[float] = None
    borrowings: Optional[float] = None
    total_assets: Optional[float] = None

    class Config:
        from_attributes = True


# ==========================================================
# Cash Flow
# ==========================================================

class CashFlowSchema(BaseModel):

    company_id: int
    year: int

    operating_activity: Optional[float] = None
    investing_activity: Optional[float] = None
    financing_activity: Optional[float] = None

    class Config:
        from_attributes = True


# ==========================================================
# Stock Prices
# ==========================================================

class StockPriceSchema(BaseModel):

    company_id: int

    date: str

    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[float] = None

    class Config:
        from_attributes = True


# ==========================================================
# Analytics Response
# ==========================================================

class AnalyticsSchema(BaseModel):

    company_name: str

    revenue: Optional[float] = None
    net_profit: Optional[float] = None
    roe: Optional[float] = None

    class Config:
        from_attributes = True