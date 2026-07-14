-- ==========================================================
-- Drop Existing Tables
-- ==========================================================

DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS profitandloss;
DROP TABLE IF EXISTS balancesheet;
DROP TABLE IF EXISTS cashflow;
DROP TABLE IF EXISTS analysis;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS prosandcons;
DROP TABLE IF EXISTS sectors;
DROP TABLE IF EXISTS stock_prices;
DROP TABLE IF EXISTS financial_ratios;

-- ==========================================================
-- Companies
-- ==========================================================

CREATE TABLE companies (
    id TEXT PRIMARY KEY,
    company_name TEXT NOT NULL,
    company_logo TEXT,
    chart_link TEXT,
    about_company TEXT,
    website TEXT,
    nse_profile TEXT,
    bse_profile TEXT,
    face_value REAL,
    book_value REAL,
    roce_percentage REAL,
    roe_percentage REAL
);

-- ==========================================================
-- Profit & Loss
-- ==========================================================

CREATE TABLE profitandloss (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    year TEXT NOT NULL,
    sales REAL,
    expenses REAL,
    operating_profit REAL,
    opm_percentage REAL,
    other_income REAL,
    interest REAL,
    depreciation REAL,
    profit_before_tax REAL,
    tax_percentage REAL,
    net_profit REAL,
    eps REAL,
    dividend_payout REAL,
    FOREIGN KEY(company_id) REFERENCES companies(id)
);

-- ==========================================================
-- Balance Sheet
-- ==========================================================

CREATE TABLE balancesheet (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    year TEXT NOT NULL,
    equity_capital REAL,
    reserves REAL,
    borrowings REAL,
    other_liabilities REAL,
    total_liabilities REAL,
    fixed_assets REAL,
    cwip REAL,
    investments REAL,
    other_asset REAL,
    total_assets REAL,
    FOREIGN KEY(company_id) REFERENCES companies(id)
);

-- ==========================================================
-- Cash Flow
-- ==========================================================

CREATE TABLE cashflow (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    year TEXT,
    operating_activity REAL,
    investing_activity REAL,
    financing_activity REAL,
    net_cash_flow REAL,
    FOREIGN KEY(company_id) REFERENCES companies(id)
);

-- ==========================================================
-- Analysis
-- ==========================================================

CREATE TABLE analysis (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    compounded_sales_growth TEXT,
    compounded_profit_growth TEXT,
    stock_price_cagr TEXT,
    roe TEXT,
    FOREIGN KEY(company_id) REFERENCES companies(id)
);

-- ==========================================================
-- Documents
-- ==========================================================

CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    year TEXT,
    annual_report TEXT,
    FOREIGN KEY(company_id) REFERENCES companies(id)
);

-- ==========================================================
-- Pros & Cons
-- ==========================================================

CREATE TABLE prosandcons (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    pros TEXT,
    cons TEXT,
    FOREIGN KEY(company_id) REFERENCES companies(id)
);

-- ==========================================================
-- Sectors
-- ==========================================================

CREATE TABLE sectors (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    broad_sector TEXT,
    sub_sector TEXT,
    index_weight_pct REAL,
    market_cap_category TEXT,
    FOREIGN KEY(company_id) REFERENCES companies(id)
);

-- ==========================================================
-- Stock Prices
-- ==========================================================

CREATE TABLE stock_prices (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    date TEXT,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume INTEGER,
    adjusted_close REAL,
    FOREIGN KEY(company_id) REFERENCES companies(id)
);

-- ==========================================================
-- Financial Ratios
-- ==========================================================

CREATE TABLE financial_ratios (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    year TEXT,
    net_profit_margin_pct REAL,
    operating_profit_margin_pct REAL,
    return_on_equity_pct REAL,
    debt_to_equity REAL,
    interest_coverage REAL,
    asset_turnover REAL,
    free_cash_flow_cr REAL,
    capex_cr REAL,
    earnings_per_share REAL,
    book_value_per_share REAL,
    dividend_payout_ratio_pct REAL,
    total_debt_cr REAL,
    cash_from_operations_cr REAL,
    FOREIGN KEY(company_id) REFERENCES companies(id)
);