from .database import execute_query

# ==========================================================
# Dashboard KPIs
# ==========================================================

def get_total_companies():
    return execute_query("""
        SELECT COUNT(*) AS total
        FROM companies
    """)

def get_total_ratios():
    return execute_query("""
        SELECT COUNT(*) AS total
        FROM financial_ratios
    """)

def get_total_years():
    return execute_query("""
        SELECT COUNT(DISTINCT year) AS total
        FROM profitandloss
    """)

# ==========================================================
# Company List
# ==========================================================

def get_company_list():

    return execute_query("""

    SELECT
        id,
        company_name

    FROM companies

    ORDER BY company_name

    """)

# ==========================================================
# Sector Distribution
# ==========================================================

def get_sector_distribution():

    return execute_query("""

    SELECT

        broad_sector,

        COUNT(*) total_companies

    FROM sectors

    GROUP BY broad_sector

    ORDER BY total_companies DESC

    """)

# ==========================================================
# Companies Preview
# ==========================================================

def get_company_preview():

    return execute_query("""

    SELECT *

    FROM companies

    LIMIT 10

    """)

# ==========================================================
# Top Revenue Companies
# ==========================================================

def get_top_revenue():

    return execute_query("""

    SELECT

        c.company_name,

        MAX(p.sales) revenue

    FROM companies c

    JOIN profitandloss p

    ON c.id=p.company_id

    GROUP BY c.company_name

    ORDER BY revenue DESC

    LIMIT 10

    """)

# ==========================================================
# Revenue Trend
# ==========================================================

def get_revenue(company_id):

    return execute_query(f"""

    SELECT

        year,

        sales

    FROM profitandloss

    WHERE company_id='{company_id}'

    ORDER BY year

    """)

# ==========================================================
# Profit Trend
# ==========================================================

def get_profit(company_id):

    return execute_query(f"""

    SELECT

        year,

        net_profit

    FROM profitandloss

    WHERE company_id='{company_id}'

    ORDER BY year

    """)

# ==========================================================
# Financial Ratios
# ==========================================================

def get_ratios(company_id):

    return execute_query(f"""

    SELECT

        year,

        return_on_equity_pct,

        debt_to_equity,

        asset_turnover

    FROM financial_ratios

    WHERE company_id='{company_id}'

    ORDER BY year

    """)

# ==========================================================
# Latest Snapshot
# ==========================================================

def get_latest_snapshot(company_id):

    return execute_query(f"""
    SELECT
        p.sales,
        p.net_profit,
        r.return_on_equity_pct,
        r.debt_to_equity
    FROM profitandloss p
    JOIN financial_ratios r
    ON p.company_id=r.company_id
    AND p.year=r.year
    WHERE p.company_id='{company_id}'
    ORDER BY p.year DESC
    LIMIT 1;
    """)
from utils.database import execute_query


# ==========================================================
# Dashboard KPIs
# ==========================================================

def get_total_companies():
    return execute_query("""
        SELECT COUNT(*) AS total
        FROM companies
    """)


def get_total_ratios():
    return execute_query("""
        SELECT COUNT(*) AS total
        FROM financial_ratios
    """)


def get_total_years():
    return execute_query("""
        SELECT COUNT(DISTINCT year) AS total
        FROM profitandloss
    """)


# ==========================================================
# Company List
# ==========================================================

def get_company_list():

    return execute_query("""

    SELECT
        id,
        company_name

    FROM companies

    ORDER BY company_name

    """)


# ==========================================================
# Sector Distribution
# ==========================================================

def get_sector_distribution():

    return execute_query("""

    SELECT

        broad_sector,

        COUNT(*) total_companies

    FROM sectors

    GROUP BY broad_sector

    ORDER BY total_companies DESC

    """)


# ==========================================================
# Companies Preview
# ==========================================================

def get_company_preview():

    return execute_query("""

    SELECT *

    FROM companies

    LIMIT 10

    """)


# ==========================================================
# Top Revenue Companies
# ==========================================================

def get_top_revenue():

    return execute_query("""

    SELECT

        c.company_name,

        MAX(p.sales) revenue

    FROM companies c

    JOIN profitandloss p

    ON c.id=p.company_id

    GROUP BY c.company_name

    ORDER BY revenue DESC

    LIMIT 10

    """)


# ==========================================================
# Revenue Trend
# ==========================================================

def get_revenue(company_id):

    return execute_query(f"""

    SELECT

        year,

        sales

    FROM profitandloss

    WHERE company_id='{company_id}'

    ORDER BY year

    """)


# ==========================================================
# Profit Trend
# ==========================================================

def get_profit(company_id):

    return execute_query(f"""

    SELECT

        year,

        net_profit

    FROM profitandloss

    WHERE company_id='{company_id}'

    ORDER BY year

    """)


# ==========================================================
# Financial Ratios
# ==========================================================

def get_ratios(company_id):

    return execute_query(f"""

    SELECT

        year,

        return_on_equity_pct,

        debt_to_equity,

        asset_turnover

    FROM financial_ratios

    WHERE company_id='{company_id}'

    ORDER BY year

    """)