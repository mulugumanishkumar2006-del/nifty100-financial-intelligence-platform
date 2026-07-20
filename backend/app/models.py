"""
SQLAlchemy Models

NIFTY100 Financial Intelligence Platform
"""

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Text
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


# ==========================================================
# Companies
# ==========================================================

class Company(Base):

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)

    company_name = Column(String)

    ticker = Column(String)

    isin = Column(String)

    market_cap = Column(Float)


# ==========================================================
# Sectors
# ==========================================================

class Sector(Base):

    __tablename__ = "sectors"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer)

    broad_sector = Column(String)

    sector = Column(String)

    industry = Column(String)


# ==========================================================
# Profit & Loss
# ==========================================================

class ProfitLoss(Base):

    __tablename__ = "profitandloss"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer)

    year = Column(Integer)

    sales = Column(Float)

    operating_profit = Column(Float)

    net_profit = Column(Float)

    eps = Column(Float)


# ==========================================================
# Balance Sheet
# ==========================================================

class BalanceSheet(Base):

    __tablename__ = "balancesheet"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer)

    year = Column(Integer)

    equity_capital = Column(Float)

    reserves = Column(Float)

    borrowings = Column(Float)

    total_assets = Column(Float)


# ==========================================================
# Cash Flow
# ==========================================================

class CashFlow(Base):

    __tablename__ = "cashflow"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer)

    year = Column(Integer)

    operating_activity = Column(Float)

    investing_activity = Column(Float)

    financing_activity = Column(Float)


# ==========================================================
# Financial Ratios
# ==========================================================

class FinancialRatio(Base):

    __tablename__ = "financial_ratios"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer)

    year = Column(Integer)

    return_on_equity_pct = Column(Float)

    debt_to_equity = Column(Float)

    interest_coverage = Column(Float)

    asset_turnover = Column(Float)

    revenue_cagr_5yr = Column(Float)

    pat_cagr_5yr = Column(Float)

    composite_quality_score = Column(Float)


# ==========================================================
# Stock Prices
# ==========================================================

class StockPrice(Base):

    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer)

    date = Column(String)

    open = Column(Float)

    high = Column(Float)

    low = Column(Float)

    close = Column(Float)

    volume = Column(Float)


# ==========================================================
# Documents
# ==========================================================

class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer)

    document_type = Column(String)

    url = Column(Text)


# ==========================================================
# Pros & Cons
# ==========================================================

class ProsCons(Base):

    __tablename__ = "prosandcons"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer)

    pros = Column(Text)

    cons = Column(Text)


# ==========================================================
# Analysis
# ==========================================================

class Analysis(Base):

    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer)

    year = Column(Integer)

    analysis = Column(Text)