import sqlite3
from pathlib import Path
import pandas as pd

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE = PROJECT_ROOT / "database" / "nifty100.db"

# ==========================================================
# Connect Database
# ==========================================================

connection = sqlite3.connect(DATABASE)

# ==========================================================
# Dynamic column resolution for balancesheet table
# ==========================================================
# Different exports of this dataset name the current-assets /
# current-liabilities columns differently (e.g. with a "_cr" suffix,
# like other tables in this DB). Instead of hardcoding a name that may
# not exist and crashing every liquidity-related query, we detect the
# real column names once here and reuse them everywhere below.

def resolve_column(table_name, candidates):
    cols = [row[1] for row in connection.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()]
    for name in candidates:
        if name in cols:
            return name
    return None

BALANCESHEET_COLS = [row[1] for row in connection.execute(
    "PRAGMA table_info(balancesheet)"
).fetchall()]
print("balancesheet columns found in DB:", BALANCESHEET_COLS)

CURRENT_ASSETS_COL = resolve_column("balancesheet", [
    "current_assets",
    "total_current_assets",
    "current_assets_cr",
    "total_current_assets_cr",
    "curr_assets",
])

CURRENT_LIABILITIES_COL = resolve_column("balancesheet", [
    "current_liabilities",
    "total_current_liabilities",
    "current_liabilities_cr",
    "total_current_liabilities_cr",
    "curr_liabilities",
])

HAS_LIQUIDITY_COLS = CURRENT_ASSETS_COL is not None and CURRENT_LIABILITIES_COL is not None

if not HAS_LIQUIDITY_COLS:
    print(
        "WARNING: Could not auto-detect current-assets / current-liabilities "
        "columns in 'balancesheet' from the candidate list above. "
        "Queries 84, 85, 87, 96, 98, and 100 (liquidity-ratio sections) "
        "will be skipped. Add the real column name (see the printed list "
        "above) to the candidates list in resolve_column() calls."
    )
else:
    print(f"Using '{CURRENT_ASSETS_COL}' as current assets column.")
    print(f"Using '{CURRENT_LIABILITIES_COL}' as current liabilities column.")

# ==========================================================
# Dynamic table/column resolution for market cap data
# ==========================================================
# The dataset doesn't have a table literally named `market_cap` in
# every export. We detect the real table name (and its value column)
# once here and reuse them in every market-cap-dependent query below.

ALL_TABLES = [row[0] for row in connection.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()]
print("Tables found in DB:", ALL_TABLES)

def resolve_table(candidates):
    for name in candidates:
        if name in ALL_TABLES:
            return name
    return None

MARKET_CAP_TABLE = resolve_table([
    "market_cap",
    "marketcap",
    "market_capitalization",
    "mcap",
])

MARKET_CAP_COL = None
if MARKET_CAP_TABLE:
    MARKET_CAP_COL = resolve_column(MARKET_CAP_TABLE, [
        "market_cap",
        "market_cap_cr",
        "marketcap",
        "mcap",
        "market_capitalization",
    ])

HAS_MARKET_CAP = MARKET_CAP_TABLE is not None and MARKET_CAP_COL is not None

if not HAS_MARKET_CAP:
    print(
        "WARNING: Could not auto-detect a market cap table/column from the "
        "candidate lists above. Queries 89, 90, 97, 99, and 100 "
        "(market-cap-dependent sections) will be skipped. Add the real "
        "table/column name (see the printed lists above) to the "
        "candidates lists in resolve_table()/resolve_column() calls."
    )
else:
    print(f"Using table '{MARKET_CAP_TABLE}', column '{MARKET_CAP_COL}' for market cap data.")

print("====================================================")
print("Query 51 - Company Revenue Ranking")
print("====================================================")

# ==========================================================
# Query 51 - Rank Companies by Latest Revenue
# ==========================================================

query = """
WITH latest_sales AS (
    SELECT
        company_id,
        year,
        sales,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
)

SELECT
    RANK() OVER (
        ORDER BY ls.sales DESC
    ) AS revenue_rank,
    c.company_name,
    ls.year,
    ls.sales

FROM latest_sales ls

JOIN companies c
ON ls.company_id = c.id

WHERE ls.rn = 1
AND ls.sales IS NOT NULL

ORDER BY revenue_rank;
"""

df = pd.read_sql_query(query, connection)

print(df)
# ==========================================================
# Query 53 - Top Company in Each Sector by Latest Revenue
# ==========================================================

query = """
WITH latest_sales AS (
    SELECT
        p.company_id,
        p.sales,
        p.year,
        ROW_NUMBER() OVER (
            PARTITION BY p.company_id
            ORDER BY p.year DESC
        ) AS rn
    FROM profitandloss p
),

sector_ranking AS (
    SELECT
        s.broad_sector,
        c.company_name,
        ls.year,
        ls.sales,
        RANK() OVER (
            PARTITION BY s.broad_sector
            ORDER BY ls.sales DESC
        ) AS sector_rank
    FROM latest_sales ls
    JOIN companies c
        ON ls.company_id = c.id
    JOIN sectors s
        ON ls.company_id = s.company_id
    WHERE ls.rn = 1
      AND ls.sales IS NOT NULL
)

SELECT
    broad_sector,
    company_name,
    year,
    sales
FROM sector_ranking
WHERE sector_rank = 1
ORDER BY broad_sector;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 53 - Top Company in Each Sector")
print("====================================================")
print(df)
# ==========================================================
# Query 54 - Running Total of Sales
# ==========================================================

query = """
SELECT
    c.company_name,
    p.year,
    p.sales,

    SUM(p.sales) OVER (
        PARTITION BY p.company_id
        ORDER BY p.year
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_sales

FROM profitandloss p

JOIN companies c
ON p.company_id = c.id

WHERE p.sales IS NOT NULL

ORDER BY
    c.company_name,
    p.year;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 54 - Running Total of Sales")
print("====================================================")
print(df)
# ==========================================================
# Query 55 - 3-Year Moving Average of Net Profit
# ==========================================================

query = """
SELECT
    c.company_name,
    p.year,
    p.net_profit,

    ROUND(
        AVG(p.net_profit) OVER (
            PARTITION BY p.company_id
            ORDER BY p.year
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS moving_average_net_profit

FROM profitandloss p

JOIN companies c
ON p.company_id = c.id

WHERE p.net_profit IS NOT NULL

ORDER BY
    c.company_name,
    p.year;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 55 - 3-Year Moving Average of Net Profit")
print("====================================================")
print(df)
# ==========================================================
# Query 56 - Revenue Forecast using LEAD()
# ==========================================================

query = """
SELECT
    c.company_name,
    p.year,
    p.sales AS current_year_sales,

    LEAD(p.sales) OVER (
        PARTITION BY p.company_id
        ORDER BY p.year
    ) AS next_year_sales,

    ROUND(
        (
            LEAD(p.sales) OVER (
                PARTITION BY p.company_id
                ORDER BY p.year
            ) - p.sales
        ) * 100.0 / p.sales,
        2
    ) AS expected_growth_percentage

FROM profitandloss p

JOIN companies c
ON p.company_id = c.id

WHERE p.sales IS NOT NULL

ORDER BY
    c.company_name,
    p.year;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 56 - Revenue Forecast using LEAD()")
print("====================================================")
print(df)
# ==========================================================
# Query 57 - Highest Revenue using FIRST_VALUE()
# ==========================================================

query = """
SELECT
    c.company_name,
    p.year,
    p.sales,

    FIRST_VALUE(p.sales) OVER (
        PARTITION BY p.company_id
        ORDER BY p.sales DESC
    ) AS highest_sales,

    ROUND(
        (
            p.sales * 100.0
        ) /
        FIRST_VALUE(p.sales) OVER (
            PARTITION BY p.company_id
            ORDER BY p.sales DESC
        ),
        2
    ) AS percentage_of_highest_sales

FROM profitandloss p

JOIN companies c
ON p.company_id = c.id

WHERE p.sales IS NOT NULL

ORDER BY
    c.company_name,
    p.year;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 57 - Highest Revenue using FIRST_VALUE()")
print("====================================================")
print(df)
# ==========================================================
# Query 58 - Latest Revenue using LAST_VALUE()
# ==========================================================

query = """
SELECT
    c.company_name,
    p.year,
    p.sales,

    LAST_VALUE(p.sales) OVER (
        PARTITION BY p.company_id
        ORDER BY p.year
        ROWS BETWEEN UNBOUNDED PRECEDING
        AND UNBOUNDED FOLLOWING
    ) AS latest_sales

FROM profitandloss p

JOIN companies c
ON p.company_id = c.id

WHERE p.sales IS NOT NULL

ORDER BY
    c.company_name,
    p.year;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 58 - Latest Revenue using LAST_VALUE()")
print("====================================================")
print(df)
# ==========================================================
# Query 59 - Revenue Quartiles using NTILE()
# ==========================================================

query = """
WITH latest_sales AS (
    SELECT
        company_id,
        year,
        sales,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
)

SELECT
    c.company_name,
    ls.year,
    ls.sales,

    NTILE(4) OVER (
        ORDER BY ls.sales DESC
    ) AS revenue_quartile

FROM latest_sales ls

JOIN companies c
ON ls.company_id = c.id

WHERE ls.rn = 1
AND ls.sales IS NOT NULL

ORDER BY
    revenue_quartile,
    ls.sales DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 59 - Revenue Quartiles using NTILE()")
print("====================================================")
print(df)
# ==========================================================
# Query 60 - Revenue Percentile Analysis
# ==========================================================

query = """
WITH latest_sales AS (
    SELECT
        company_id,
        year,
        sales,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
)

SELECT
    c.company_name,
    ls.year,
    ls.sales,

    ROUND(
        PERCENT_RANK() OVER (
            ORDER BY ls.sales
        ),
        4
    ) AS revenue_percentile

FROM latest_sales ls

JOIN companies c
ON ls.company_id = c.id

WHERE ls.rn = 1
AND ls.sales IS NOT NULL

ORDER BY
    revenue_percentile DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 60 - Revenue Percentile Analysis")
print("====================================================")
print(df)
# ==========================================================
# Query 61 - Sector-wise Revenue Analysis
# ==========================================================

query = """
WITH latest_sales AS (
    SELECT
        company_id,
        sales,
        year,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
)

SELECT
    s.broad_sector,
    COUNT(DISTINCT c.id) AS total_companies,

    ROUND(SUM(ls.sales), 2) AS total_sector_revenue,

    ROUND(AVG(ls.sales), 2) AS average_company_revenue,

    ROUND(MAX(ls.sales), 2) AS highest_company_revenue,

    ROUND(MIN(ls.sales), 2) AS lowest_company_revenue

FROM latest_sales ls

JOIN companies c
ON ls.company_id = c.id

JOIN sectors s
ON c.id = s.company_id

WHERE
    ls.rn = 1
    AND ls.sales IS NOT NULL

GROUP BY
    s.broad_sector

ORDER BY
    total_sector_revenue DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 61 - Sector-wise Revenue Analysis")
print("====================================================")
print(df)
# ==========================================================
# Query 62 - Revenue CAGR Analysis
# ==========================================================
# FIX: `year` is stored as text like "Mar 2024", "Dec 2012", or "TTM".
# CAST(year AS INTEGER) on a non-numeric-leading string returns 0 in
# SQLite, which silently broke the start_year/end_year filter and made
# this query return an empty DataFrame. We now:
#   1) exclude 'TTM' rows (not a fixed calendar year)
#   2) extract the last 4 characters (the actual year digits) instead
#      of casting the whole string

query = """
WITH revenue_data AS (
    SELECT
        company_id,
        year,
        sales,
        CAST(SUBSTR(year, -4) AS INTEGER) AS year_num,

        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY CAST(SUBSTR(year, -4) AS INTEGER) ASC
        ) AS first_year,

        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY CAST(SUBSTR(year, -4) AS INTEGER) DESC
        ) AS last_year

    FROM profitandloss

    WHERE sales IS NOT NULL
      AND year <> 'TTM'
),

first_sales AS (
    SELECT
        company_id,
        year_num AS start_year,
        sales AS start_sales
    FROM revenue_data
    WHERE first_year = 1
),

last_sales AS (
    SELECT
        company_id,
        year_num AS end_year,
        sales AS end_sales
    FROM revenue_data
    WHERE last_year = 1
)

SELECT
    c.company_name,

    fs.start_year,
    ls.end_year,

    fs.start_sales,
    ls.end_sales,

    ROUND(
        (
            POWER(
                (ls.end_sales * 1.0 / fs.start_sales),
                1.0 /
                (ls.end_year - fs.start_year)
            ) - 1
        ) * 100,
        2
    ) AS revenue_cagr_percentage

FROM companies c

JOIN first_sales fs
ON c.id = fs.company_id

JOIN last_sales ls
ON c.id = ls.company_id

WHERE
    fs.start_sales > 0
    AND ls.end_sales > 0
    AND ls.end_year > fs.start_year

ORDER BY
    revenue_cagr_percentage DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 62 - Revenue CAGR Analysis")
print("====================================================")
print(df)
# ==========================================================
# Query 63 - Financial Health Score
# ==========================================================

query = """
WITH latest_profit AS (
    SELECT
        company_id,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        debt_to_equity,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
),

latest_cashflow AS (
    SELECT
        company_id,
        net_cash_flow,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM cashflow
)

SELECT
    c.company_name,

    lp.net_profit,

    lr.return_on_equity_pct,

    lr.debt_to_equity,

    lc.net_cash_flow,

    (
        CASE WHEN lp.net_profit > 0 THEN 1 ELSE 0 END +
        CASE WHEN lr.return_on_equity_pct > 15 THEN 1 ELSE 0 END +
        CASE WHEN lr.debt_to_equity < 1 THEN 1 ELSE 0 END +
        CASE WHEN lc.net_cash_flow > 0 THEN 1 ELSE 0 END
    ) AS financial_health_score

FROM companies c

LEFT JOIN latest_profit lp
ON c.id = lp.company_id
AND lp.rn = 1

LEFT JOIN latest_ratios lr
ON c.id = lr.company_id
AND lr.rn = 1

LEFT JOIN latest_cashflow lc
ON c.id = lc.company_id
AND lc.rn = 1

ORDER BY
    financial_health_score DESC,
    lp.net_profit DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 63 - Financial Health Score")
print("====================================================")
print(df)
# ==========================================================
# Query 64 - Revenue Consistency Index
# ==========================================================

query = """
SELECT
    c.company_name,

    COUNT(*) AS years_available,

    ROUND(AVG(p.sales), 2) AS average_sales,

    ROUND(
        SQRT(
            AVG(p.sales * p.sales) -
            AVG(p.sales) * AVG(p.sales)
        ),
        2
    ) AS sales_standard_deviation,

    ROUND(
        (
            SQRT(
                AVG(p.sales * p.sales) -
                AVG(p.sales) * AVG(p.sales)
            ) * 100.0
        ) / AVG(p.sales),
        2
    ) AS coefficient_of_variation

FROM profitandloss p

JOIN companies c
ON p.company_id = c.id

WHERE
    p.sales IS NOT NULL

GROUP BY
    c.company_name

HAVING
    COUNT(*) >= 3

ORDER BY
    coefficient_of_variation ASC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 64 - Revenue Consistency Index")
print("====================================================")
print(df)
# ==========================================================
# Query 65 - Profit Growth Ranking
# ==========================================================

query = """
WITH profit_growth AS (
    SELECT
        company_id,
        year,
        net_profit,

        LAG(net_profit) OVER (
            PARTITION BY company_id
            ORDER BY year
        ) AS previous_year_profit

    FROM profitandloss

    WHERE net_profit IS NOT NULL
)

SELECT
    c.company_name,

    pg.year,

    pg.previous_year_profit,

    pg.net_profit,

    ROUND(
        (
            (pg.net_profit - pg.previous_year_profit)
            * 100.0
        ) / pg.previous_year_profit,
        2
    ) AS profit_growth_percentage,

    RANK() OVER (
        ORDER BY
        (
            (pg.net_profit - pg.previous_year_profit)
            * 100.0
        ) / pg.previous_year_profit DESC
    ) AS growth_rank

FROM profit_growth pg

JOIN companies c
ON pg.company_id = c.id

WHERE
    pg.previous_year_profit IS NOT NULL
    AND pg.previous_year_profit <> 0

ORDER BY
    growth_rank;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 65 - Profit Growth Ranking")
print("====================================================")
print(df)
# ==========================================================
# Query 66 - Cash Flow Stability Analysis
# ==========================================================

query = """
SELECT
    c.company_name,

    COUNT(*) AS years_available,

    ROUND(AVG(cf.net_cash_flow), 2) AS average_cash_flow,

    ROUND(
        MIN(cf.net_cash_flow),
        2
    ) AS minimum_cash_flow,

    ROUND(
        MAX(cf.net_cash_flow),
        2
    ) AS maximum_cash_flow,

    ROUND(
        SQRT(
            AVG(cf.net_cash_flow * cf.net_cash_flow) -
            AVG(cf.net_cash_flow) * AVG(cf.net_cash_flow)
        ),
        2
    ) AS cash_flow_std_dev

FROM cashflow cf

JOIN companies c
ON cf.company_id = c.id

WHERE
    cf.net_cash_flow IS NOT NULL

GROUP BY
    c.company_name

HAVING
    COUNT(*) >= 3

ORDER BY
    cash_flow_std_dev ASC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 66 - Cash Flow Stability Analysis")
print("====================================================")
print(df)
# ==========================================================
# Query 67 - ROE vs ROCE Comparison
# ==========================================================
# FIX: your financial_ratios table does not have a column literally
# named `return_on_capital_employed_pct` (that caused the crash).
# We first inspect the real schema, then run the query using whichever
# ROCE-like column actually exists. If none is found, we skip cleanly
# instead of crashing the whole script.

roce_column = None
candidate_names = [
    "return_on_capital_employed_pct",
    "roce_pct",
    "roce",
    "return_on_capital_employed",
]

schema_cols = [row[1] for row in connection.execute(
    "PRAGMA table_info(financial_ratios)"
).fetchall()]

print("\nfinancial_ratios columns found in DB:", schema_cols)

for name in candidate_names:
    if name in schema_cols:
        roce_column = name
        break

if roce_column is None:
    print("\n====================================================")
    print("Query 67 - ROE vs ROCE Comparison")
    print("====================================================")
    print(
        "SKIPPED: No ROCE-like column found in 'financial_ratios'. "
        "Checked for: " + ", ".join(candidate_names) + ". "
        "Update `candidate_names` above with the real column name "
        "from the list printed above and re-run."
    )
else:
    query = f"""
    WITH latest_ratios AS (
        SELECT
            company_id,
            year,
            return_on_equity_pct,
            {roce_column} AS roce_raw,
            ROW_NUMBER() OVER (
                PARTITION BY company_id
                ORDER BY year DESC
            ) AS rn
        FROM financial_ratios
    )

    SELECT
        c.company_name,

        lr.year,

        ROUND(lr.return_on_equity_pct, 2) AS roe,

        ROUND(lr.roce_raw, 2) AS roce,

        ROUND(
            lr.return_on_equity_pct -
            lr.roce_raw,
            2
        ) AS roe_roce_difference

    FROM latest_ratios lr

    JOIN companies c
    ON lr.company_id = c.id

    WHERE
        lr.rn = 1
        AND lr.return_on_equity_pct IS NOT NULL
        AND lr.roce_raw IS NOT NULL

    ORDER BY
        roe DESC;
    """

    df = pd.read_sql_query(query, connection)

    print("\n====================================================")
    print("Query 67 - ROE vs ROCE Comparison")
    print("====================================================")
    print(df)
# ==========================================================
# Query 68 - Debt Risk Classification
# ==========================================================

query = """
WITH latest_ratios AS (
    SELECT
        company_id,
        year,
        debt_to_equity,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
)

SELECT
    c.company_name,

    lr.year,

    ROUND(lr.debt_to_equity, 2) AS debt_to_equity,

    CASE
        WHEN lr.debt_to_equity < 0.50 THEN 'Low Risk'
        WHEN lr.debt_to_equity BETWEEN 0.50 AND 1.50 THEN 'Moderate Risk'
        WHEN lr.debt_to_equity > 1.50 THEN 'High Risk'
        ELSE 'Not Available'
    END AS debt_risk

FROM latest_ratios lr

JOIN companies c
ON lr.company_id = c.id

WHERE
    lr.rn = 1

ORDER BY
    lr.debt_to_equity ASC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 68 - Debt Risk Classification")
print("====================================================")
print(df)
# ==========================================================
# Query 69 - Sector Benchmark Report
# ==========================================================

query = """
WITH latest_profit AS (
    SELECT
        company_id,
        sales,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
)

SELECT
    s.broad_sector,

    COUNT(DISTINCT c.id) AS total_companies,

    ROUND(AVG(lp.sales), 2) AS average_revenue,

    ROUND(AVG(lp.net_profit), 2) AS average_net_profit,

    ROUND(AVG(lr.return_on_equity_pct), 2) AS average_roe

FROM companies c

JOIN sectors s
ON c.id = s.company_id

LEFT JOIN latest_profit lp
ON c.id = lp.company_id
AND lp.rn = 1

LEFT JOIN latest_ratios lr
ON c.id = lr.company_id
AND lr.rn = 1

GROUP BY
    s.broad_sector

ORDER BY
    average_revenue DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 69 - Sector Benchmark Report")
print("====================================================")
print(df)
# ==========================================================
# Query 70 - Executive Financial KPI Dashboard
# ==========================================================

query = """
WITH latest_profit AS (
    SELECT
        company_id,
        year,
        sales,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        debt_to_equity,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
),

latest_cashflow AS (
    SELECT
        company_id,
        net_cash_flow,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM cashflow
)

SELECT
    c.company_name,

    lp.year,

    ROUND(lp.sales,2) AS revenue,

    ROUND(lp.net_profit,2) AS net_profit,

    ROUND(lr.return_on_equity_pct,2) AS roe,

    ROUND(lr.debt_to_equity,2) AS debt_to_equity,

    ROUND(lc.net_cash_flow,2) AS net_cash_flow,

    (
        CASE WHEN lp.net_profit > 0 THEN 1 ELSE 0 END +
        CASE WHEN lr.return_on_equity_pct > 15 THEN 1 ELSE 0 END +
        CASE WHEN lr.debt_to_equity < 1 THEN 1 ELSE 0 END +
        CASE WHEN lc.net_cash_flow > 0 THEN 1 ELSE 0 END
    ) AS financial_score,

    CASE
        WHEN (
            CASE WHEN lp.net_profit > 0 THEN 1 ELSE 0 END +
            CASE WHEN lr.return_on_equity_pct > 15 THEN 1 ELSE 0 END +
            CASE WHEN lr.debt_to_equity < 1 THEN 1 ELSE 0 END +
            CASE WHEN lc.net_cash_flow > 0 THEN 1 ELSE 0 END
        ) = 4 THEN 'Excellent'

        WHEN (
            CASE WHEN lp.net_profit > 0 THEN 1 ELSE 0 END +
            CASE WHEN lr.return_on_equity_pct > 15 THEN 1 ELSE 0 END +
            CASE WHEN lr.debt_to_equity < 1 THEN 1 ELSE 0 END +
            CASE WHEN lc.net_cash_flow > 0 THEN 1 ELSE 0 END
        ) = 3 THEN 'Good'

        WHEN (
            CASE WHEN lp.net_profit > 0 THEN 1 ELSE 0 END +
            CASE WHEN lr.return_on_equity_pct > 15 THEN 1 ELSE 0 END +
            CASE WHEN lr.debt_to_equity < 1 THEN 1 ELSE 0 END +
            CASE WHEN lc.net_cash_flow > 0 THEN 1 ELSE 0 END
        ) = 2 THEN 'Average'

        ELSE 'Needs Attention'
    END AS financial_rating

FROM companies c

LEFT JOIN latest_profit lp
ON c.id = lp.company_id
AND lp.rn = 1

LEFT JOIN latest_ratios lr
ON c.id = lr.company_id
AND lr.rn = 1

LEFT JOIN latest_cashflow lc
ON c.id = lc.company_id
AND lc.rn = 1

ORDER BY
    financial_score DESC,
    revenue DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n======================================================")
print("Executive Financial KPI Dashboard")
print("======================================================")
print(df)
# ==========================================================
# Query 71 - Investment Opportunity Scorecard
# ==========================================================

query = """
WITH latest_profit AS (
    SELECT
        company_id,
        sales,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        debt_to_equity,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
),

latest_cashflow AS (
    SELECT
        company_id,
        net_cash_flow,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM cashflow
)

SELECT
    c.company_name,

    ROUND(lp.sales,2) AS revenue,

    ROUND(lp.net_profit,2) AS net_profit,

    ROUND(lr.return_on_equity_pct,2) AS roe,

    ROUND(lr.debt_to_equity,2) AS debt_to_equity,

    ROUND(lc.net_cash_flow,2) AS net_cash_flow,

    (
        CASE WHEN lp.net_profit > 0 THEN 1 ELSE 0 END +
        CASE WHEN lr.return_on_equity_pct > 15 THEN 1 ELSE 0 END +
        CASE WHEN lr.debt_to_equity < 1 THEN 1 ELSE 0 END +
        CASE WHEN lc.net_cash_flow > 0 THEN 1 ELSE 0 END
    ) AS investment_score

FROM companies c

LEFT JOIN latest_profit lp
ON c.id = lp.company_id
AND lp.rn = 1

LEFT JOIN latest_ratios lr
ON c.id = lr.company_id
AND lr.rn = 1

LEFT JOIN latest_cashflow lc
ON c.id = lc.company_id
AND lc.rn = 1

ORDER BY
    investment_score DESC,
    roe DESC,
    revenue DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 71 - Investment Opportunity Scorecard")
print("====================================================")
print(df)
# ==========================================================
# Query 72 - Multi-Factor Company Ranking
# ==========================================================

query = """
WITH latest_profit AS (
    SELECT
        company_id,
        sales,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        debt_to_equity,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
),

latest_cashflow AS (
    SELECT
        company_id,
        net_cash_flow,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM cashflow
),

company_scores AS (
    SELECT
        c.company_name,

        lp.sales,

        lp.net_profit,

        lr.return_on_equity_pct,

        lr.debt_to_equity,

        lc.net_cash_flow,

        (
            CASE WHEN lp.net_profit > 0 THEN 1 ELSE 0 END +
            CASE WHEN lr.return_on_equity_pct > 15 THEN 1 ELSE 0 END +
            CASE WHEN lr.debt_to_equity < 1 THEN 1 ELSE 0 END +
            CASE WHEN lc.net_cash_flow > 0 THEN 1 ELSE 0 END
        ) AS investment_score

    FROM companies c

    LEFT JOIN latest_profit lp
    ON c.id = lp.company_id
    AND lp.rn = 1

    LEFT JOIN latest_ratios lr
    ON c.id = lr.company_id
    AND lr.rn = 1

    LEFT JOIN latest_cashflow lc
    ON c.id = lc.company_id
    AND lc.rn = 1
)

SELECT

    RANK() OVER(
        ORDER BY
            investment_score DESC,
            return_on_equity_pct DESC,
            net_profit DESC,
            debt_to_equity ASC
    ) AS company_rank,

    company_name,

    ROUND(sales,2) AS revenue,

    ROUND(net_profit,2) AS net_profit,

    ROUND(return_on_equity_pct,2) AS roe,

    ROUND(debt_to_equity,2) AS debt_to_equity,

    investment_score

FROM company_scores

ORDER BY company_rank;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 72 - Multi-Factor Company Ranking")
print("====================================================")
print(df)
# ==========================================================
# Query 73 - Sector Leadership Analysis
# ==========================================================

query = """
WITH latest_profit AS (
    SELECT
        company_id,
        sales,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        debt_to_equity,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
),

latest_cashflow AS (
    SELECT
        company_id,
        net_cash_flow,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM cashflow
),

company_scores AS (
    SELECT
        s.broad_sector,
        c.company_name,
        lp.sales,
        lp.net_profit,
        lr.return_on_equity_pct,
        lr.debt_to_equity,
        lc.net_cash_flow,

        (
            CASE WHEN lp.net_profit > 0 THEN 1 ELSE 0 END +
            CASE WHEN lr.return_on_equity_pct > 15 THEN 1 ELSE 0 END +
            CASE WHEN lr.debt_to_equity < 1 THEN 1 ELSE 0 END +
            CASE WHEN lc.net_cash_flow > 0 THEN 1 ELSE 0 END
        ) AS investment_score

    FROM companies c

    JOIN sectors s
    ON c.id = s.company_id

    LEFT JOIN latest_profit lp
    ON c.id = lp.company_id
    AND lp.rn = 1

    LEFT JOIN latest_ratios lr
    ON c.id = lr.company_id
    AND lr.rn = 1

    LEFT JOIN latest_cashflow lc
    ON c.id = lc.company_id
    AND lc.rn = 1
)

SELECT
    broad_sector,
    company_name,

    ROUND(sales,2) AS revenue,

    ROUND(net_profit,2) AS net_profit,

    ROUND(return_on_equity_pct,2) AS roe,

    ROUND(debt_to_equity,2) AS debt_to_equity,

    investment_score

FROM (
    SELECT
        *,

        ROW_NUMBER() OVER (
            PARTITION BY broad_sector
            ORDER BY
                investment_score DESC,
                return_on_equity_pct DESC,
                sales DESC
        ) AS sector_rank

    FROM company_scores
)

WHERE sector_rank = 1

ORDER BY broad_sector;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 73 - Sector Leadership Analysis")
print("====================================================")
print(df)
# ==========================================================
# Query 74 - High Growth, Low Risk Companies
# ==========================================================

query = """
WITH latest_profit AS (
    SELECT
        company_id,
        sales,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        debt_to_equity,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
),

latest_cashflow AS (
    SELECT
        company_id,
        net_cash_flow,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM cashflow
)

SELECT
    c.company_name,

    ROUND(lp.sales, 2) AS revenue,

    ROUND(lp.net_profit, 2) AS net_profit,

    ROUND(lr.return_on_equity_pct, 2) AS roe,

    ROUND(lr.debt_to_equity, 2) AS debt_to_equity,

    ROUND(lc.net_cash_flow, 2) AS net_cash_flow

FROM companies c

LEFT JOIN latest_profit lp
ON c.id = lp.company_id
AND lp.rn = 1

LEFT JOIN latest_ratios lr
ON c.id = lr.company_id
AND lr.rn = 1

LEFT JOIN latest_cashflow lc
ON c.id = lc.company_id
AND lc.rn = 1

WHERE
    lp.net_profit > 0
    AND lr.return_on_equity_pct > 15
    AND lr.debt_to_equity < 1
    AND lc.net_cash_flow > 0

ORDER BY
    lr.return_on_equity_pct DESC,
    lp.net_profit DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 74 - High Growth, Low Risk Companies")
print("====================================================")
print(df)
# ==========================================================
# Query 75 - Top Value Companies
# ==========================================================

query = """
WITH latest_ratios AS (
    SELECT
        company_id,
        year,
        return_on_equity_pct,
        earnings_per_share,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
)

SELECT
    c.company_name,

    lr.year,

    ROUND(lr.return_on_equity_pct, 2) AS roe,

    ROUND(lr.earnings_per_share, 2) AS eps,

    RANK() OVER (
        ORDER BY
            lr.return_on_equity_pct DESC,
            lr.earnings_per_share DESC
    ) AS value_rank

FROM latest_ratios lr

JOIN companies c
ON c.id = lr.company_id

WHERE
    lr.rn = 1
    AND lr.return_on_equity_pct IS NOT NULL
    AND lr.earnings_per_share IS NOT NULL

ORDER BY
    value_rank;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 75 - Top Value Companies")
print("====================================================")
print(df)
# ==========================================================
# Query 76 - Portfolio Performance Analysis
# ==========================================================

query = """
WITH latest_profit AS (
    SELECT
        company_id,
        year,
        sales,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
),

latest_cashflow AS (
    SELECT
        company_id,
        net_cash_flow,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM cashflow
)

SELECT
    c.company_name,

    lp.year,

    ROUND(lp.sales, 2) AS revenue,

    ROUND(lp.net_profit, 2) AS net_profit,

    ROUND(lr.return_on_equity_pct, 2) AS roe,

    ROUND(lc.net_cash_flow, 2) AS net_cash_flow,

    (
        CASE WHEN lp.sales > 10000 THEN 1 ELSE 0 END +
        CASE WHEN lp.net_profit > 1000 THEN 1 ELSE 0 END +
        CASE WHEN lr.return_on_equity_pct > 15 THEN 1 ELSE 0 END +
        CASE WHEN lc.net_cash_flow > 0 THEN 1 ELSE 0 END
    ) AS portfolio_score

FROM companies c

LEFT JOIN latest_profit lp
ON c.id = lp.company_id
AND lp.rn = 1

LEFT JOIN latest_ratios lr
ON c.id = lr.company_id
AND lr.rn = 1

LEFT JOIN latest_cashflow lc
ON c.id = lc.company_id
AND lc.rn = 1

ORDER BY
    portfolio_score DESC,
    revenue DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 76 - Portfolio Performance Analysis")
print("====================================================")
print(df)
# ==========================================================
# Query 77 - Portfolio Diversification Analysis
# ==========================================================

query = """
WITH latest_profit AS (
    SELECT
        company_id,
        sales,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
)

SELECT

    s.broad_sector,

    COUNT(DISTINCT c.id) AS total_companies,

    ROUND(SUM(lp.sales),2) AS total_revenue,

    ROUND(SUM(lp.net_profit),2) AS total_net_profit,

    ROUND(AVG(lr.return_on_equity_pct),2) AS average_roe,

    ROUND(
        100.0 * SUM(lp.sales) /
        SUM(SUM(lp.sales)) OVER (),
        2
    ) AS portfolio_revenue_percent

FROM companies c

JOIN sectors s
ON c.id = s.company_id

LEFT JOIN latest_profit lp
ON c.id = lp.company_id
AND lp.rn = 1

LEFT JOIN latest_ratios lr
ON c.id = lr.company_id
AND lr.rn = 1

GROUP BY
    s.broad_sector

ORDER BY
    total_revenue DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 77 - Portfolio Diversification Analysis")
print("====================================================")
print(df)
# ==========================================================
# Query 78 - Risk vs Return Matrix
# ==========================================================

query = """
WITH latest_ratios AS (
    SELECT
        company_id,
        year,
        return_on_equity_pct,
        debt_to_equity,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
)

SELECT

    c.company_name,

    lr.year,

    ROUND(lr.return_on_equity_pct,2) AS roe,

    ROUND(lr.debt_to_equity,2) AS debt_to_equity,

    CASE

        WHEN lr.return_on_equity_pct >= 15
             AND lr.debt_to_equity < 1
        THEN 'High Return - Low Risk'

        WHEN lr.return_on_equity_pct >= 15
             AND lr.debt_to_equity >= 1
        THEN 'High Return - High Risk'

        WHEN lr.return_on_equity_pct < 15
             AND lr.debt_to_equity < 1
        THEN 'Low Return - Low Risk'

        ELSE 'Low Return - High Risk'

    END AS investment_category

FROM latest_ratios lr

JOIN companies c
ON lr.company_id = c.id

WHERE
    lr.rn = 1
    AND lr.return_on_equity_pct IS NOT NULL
    AND lr.debt_to_equity IS NOT NULL

ORDER BY
    investment_category,
    roe DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 78 - Risk vs Return Matrix")
print("====================================================")
print(df)
# ==========================================================
# Query 79 - Sector Allocation Dashboard
# ==========================================================

query = """
WITH latest_profit AS (
    SELECT
        company_id,
        sales,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

sector_summary AS (
    SELECT
        s.broad_sector,

        COUNT(DISTINCT c.id) AS total_companies,

        SUM(lp.sales) AS total_revenue,

        AVG(lp.sales) AS average_revenue

    FROM companies c

    JOIN sectors s
        ON c.id = s.company_id

    LEFT JOIN latest_profit lp
        ON c.id = lp.company_id
       AND lp.rn = 1

    GROUP BY s.broad_sector
)

SELECT

    broad_sector,

    total_companies,

    ROUND(total_revenue,2) AS total_revenue,

    ROUND(average_revenue,2) AS average_revenue,

    ROUND(
        total_revenue * 100.0 /
        SUM(total_revenue) OVER (),
        2
    ) AS revenue_percentage,

    RANK() OVER (
        ORDER BY total_revenue DESC
    ) AS revenue_rank

FROM sector_summary

ORDER BY revenue_rank;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 79 - Sector Allocation Dashboard")
print("====================================================")
print(df)
# ==========================================================
# Query 80 - Portfolio Health Index
# ==========================================================

query = """
WITH latest_profit AS (
    SELECT
        company_id,
        year,
        sales,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        debt_to_equity,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
),

latest_cashflow AS (
    SELECT
        company_id,
        net_cash_flow,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM cashflow
),

portfolio_health AS (
    SELECT
        c.company_name,
        lp.year,
        lp.sales,
        lp.net_profit,
        lr.return_on_equity_pct,
        lr.debt_to_equity,
        lc.net_cash_flow,

        (
            CASE WHEN lp.sales > 10000 THEN 1 ELSE 0 END +
            CASE WHEN lp.net_profit > 0 THEN 1 ELSE 0 END +
            CASE WHEN lr.return_on_equity_pct >= 15 THEN 1 ELSE 0 END +
            CASE WHEN lr.debt_to_equity < 1 THEN 1 ELSE 0 END +
            CASE WHEN lc.net_cash_flow > 0 THEN 1 ELSE 0 END
        ) AS health_score

    FROM companies c

    LEFT JOIN latest_profit lp
        ON c.id = lp.company_id
       AND lp.rn = 1

    LEFT JOIN latest_ratios lr
        ON c.id = lr.company_id
       AND lr.rn = 1

    LEFT JOIN latest_cashflow lc
        ON c.id = lc.company_id
       AND lc.rn = 1
)

SELECT

    company_name,

    year,

    ROUND(sales,2) AS revenue,

    ROUND(net_profit,2) AS net_profit,

    ROUND(return_on_equity_pct,2) AS roe,

    ROUND(debt_to_equity,2) AS debt_to_equity,

    ROUND(net_cash_flow,2) AS net_cash_flow,

    health_score,

    CASE
        WHEN health_score = 5 THEN 'Excellent'
        WHEN health_score = 4 THEN 'Good'
        WHEN health_score = 3 THEN 'Average'
        WHEN health_score = 2 THEN 'Weak'
        ELSE 'Critical'
    END AS portfolio_health

FROM portfolio_health

ORDER BY
    health_score DESC,
    revenue DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 80 - Portfolio Health Index")
print("====================================================")
print(df)
# ==========================================================
# Query 81 - Earnings Volatility Analysis
# ==========================================================

query = """
WITH profit_statistics AS (
    SELECT
        company_id,

        AVG(net_profit) AS avg_profit,

        MAX(net_profit) AS max_profit,

        MIN(net_profit) AS min_profit,

        MAX(net_profit) - MIN(net_profit) AS profit_range

    FROM profitandloss

    WHERE net_profit IS NOT NULL

    GROUP BY company_id
)

SELECT

    c.company_name,

    ROUND(ps.avg_profit,2) AS average_profit,

    ROUND(ps.max_profit,2) AS highest_profit,

    ROUND(ps.min_profit,2) AS lowest_profit,

    ROUND(ps.profit_range,2) AS profit_range,

    CASE

        WHEN ps.profit_range < 1000
        THEN 'Low Volatility'

        WHEN ps.profit_range BETWEEN 1000 AND 10000
        THEN 'Moderate Volatility'

        ELSE 'High Volatility'

    END AS earnings_risk

FROM profit_statistics ps

JOIN companies c
ON ps.company_id = c.id

ORDER BY
    ps.profit_range DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 81 - Earnings Volatility Analysis")
print("====================================================")
print(df)
# ==========================================================
# Query 82 - Revenue Stability Analysis
# ==========================================================

query = """
WITH revenue_statistics AS (

    SELECT
        company_id,

        AVG(sales) AS average_revenue,

        MAX(sales) AS highest_revenue,

        MIN(sales) AS lowest_revenue,

        MAX(sales) - MIN(sales) AS revenue_range

    FROM profitandloss

    WHERE sales IS NOT NULL

    GROUP BY company_id

)

SELECT

    c.company_name,

    ROUND(rs.average_revenue,2) AS average_revenue,

    ROUND(rs.highest_revenue,2) AS highest_revenue,

    ROUND(rs.lowest_revenue,2) AS lowest_revenue,

    ROUND(rs.revenue_range,2) AS revenue_range,

    CASE

        WHEN rs.revenue_range < 5000
            THEN 'Very Stable'

        WHEN rs.revenue_range BETWEEN 5000 AND 50000
            THEN 'Moderately Stable'

        ELSE 'Highly Variable'

    END AS revenue_stability

FROM revenue_statistics rs

JOIN companies c
ON rs.company_id = c.id

ORDER BY
    rs.revenue_range DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 82 - Revenue Stability Analysis")
print("====================================================")
print(df)
# ==========================================================
# Query 83 - Cash Flow Risk Detection
# ==========================================================

query = """
WITH cashflow_statistics AS (

    SELECT
        company_id,

        AVG(net_cash_flow) AS average_cash_flow,

        MAX(net_cash_flow) AS highest_cash_flow,

        MIN(net_cash_flow) AS lowest_cash_flow,

        MAX(net_cash_flow) - MIN(net_cash_flow) AS cash_flow_range

    FROM cashflow

    WHERE net_cash_flow IS NOT NULL

    GROUP BY company_id

)

SELECT

    c.company_name,

    ROUND(cs.average_cash_flow,2) AS average_cash_flow,

    ROUND(cs.highest_cash_flow,2) AS highest_cash_flow,

    ROUND(cs.lowest_cash_flow,2) AS lowest_cash_flow,

    ROUND(cs.cash_flow_range,2) AS cash_flow_range,

    CASE

        WHEN cs.average_cash_flow > 0
             AND cs.cash_flow_range < 5000
        THEN 'Low Risk'

        WHEN cs.average_cash_flow > 0
             AND cs.cash_flow_range >= 5000
        THEN 'Moderate Risk'

        ELSE 'High Risk'

    END AS cash_flow_risk

FROM cashflow_statistics cs

JOIN companies c
ON cs.company_id = c.id

ORDER BY
    cs.cash_flow_range DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 83 - Cash Flow Risk Detection")
print("====================================================")
print(df)
# ==========================================================
# Query 84 - Liquidity Risk Dashboard
# ==========================================================

print("\n====================================================")
print("Query 84 - Liquidity Risk Dashboard")
print("====================================================")

if not HAS_LIQUIDITY_COLS:
    print("SKIPPED: current assets/liabilities columns not found in 'balancesheet'.")
else:
    query = f"""
    WITH latest_balance AS (

        SELECT
            company_id,
            year,
            {CURRENT_ASSETS_COL} AS current_assets,
            {CURRENT_LIABILITIES_COL} AS current_liabilities,

            ROW_NUMBER() OVER (
                PARTITION BY company_id
                ORDER BY year DESC
            ) AS rn

        FROM balancesheet
    )

    SELECT

        c.company_name,

        lb.year,

        ROUND(lb.current_assets,2) AS current_assets,

        ROUND(lb.current_liabilities,2) AS current_liabilities,

        ROUND(
            lb.current_assets /
            NULLIF(lb.current_liabilities,0),
            2
        ) AS current_ratio,

        ROUND(
            lb.current_assets -
            lb.current_liabilities,
            2
        ) AS working_capital,

        CASE

            WHEN (lb.current_assets / NULLIF(lb.current_liabilities,0)) >= 2
                THEN 'Excellent'

            WHEN (lb.current_assets / NULLIF(lb.current_liabilities,0)) >= 1
                THEN 'Healthy'

            WHEN (lb.current_assets / NULLIF(lb.current_liabilities,0)) >= 0.5
                THEN 'Warning'

            ELSE 'Critical'

        END AS liquidity_status

    FROM latest_balance lb

    JOIN companies c
    ON lb.company_id = c.id

    WHERE lb.rn = 1

    ORDER BY
        current_ratio DESC;
    """

    df = pd.read_sql_query(query, connection)
    print(df)
# ==========================================================
# Query 85 - Enterprise Risk Score
# ==========================================================

print("\n====================================================")
print("Query 85 - Enterprise Risk Score")
print("====================================================")

if not HAS_LIQUIDITY_COLS:
    print("SKIPPED: current assets/liabilities columns not found in 'balancesheet'.")
else:
    query = f"""
WITH latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        debt_to_equity,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
),

latest_cashflow AS (
    SELECT
        company_id,
        net_cash_flow,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM cashflow
),

latest_balance AS (
    SELECT
        company_id,
        {CURRENT_ASSETS_COL} AS current_assets,
        {CURRENT_LIABILITIES_COL} AS current_liabilities,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM balancesheet
)

SELECT

    c.company_name,

    ROUND(lr.return_on_equity_pct,2) AS roe,

    ROUND(lr.debt_to_equity,2) AS debt_to_equity,

    ROUND(lc.net_cash_flow,2) AS net_cash_flow,

    ROUND(
        lb.current_assets /
        NULLIF(lb.current_liabilities,0),
        2
    ) AS current_ratio,

    (
        CASE WHEN lr.return_on_equity_pct < 15 THEN 1 ELSE 0 END +
        CASE WHEN lr.debt_to_equity >= 1 THEN 1 ELSE 0 END +
        CASE WHEN lc.net_cash_flow <= 0 THEN 1 ELSE 0 END +
        CASE
            WHEN (lb.current_assets / NULLIF(lb.current_liabilities,0)) < 1
            THEN 1
            ELSE 0
        END
    ) AS risk_score,

    CASE

        WHEN (
            CASE WHEN lr.return_on_equity_pct < 15 THEN 1 ELSE 0 END +
            CASE WHEN lr.debt_to_equity >= 1 THEN 1 ELSE 0 END +
            CASE WHEN lc.net_cash_flow <= 0 THEN 1 ELSE 0 END +
            CASE
                WHEN (lb.current_assets / NULLIF(lb.current_liabilities,0)) < 1
                THEN 1
                ELSE 0
            END
        ) = 0 THEN 'Low Risk'

        WHEN (
            CASE WHEN lr.return_on_equity_pct < 15 THEN 1 ELSE 0 END +
            CASE WHEN lr.debt_to_equity >= 1 THEN 1 ELSE 0 END +
            CASE WHEN lc.net_cash_flow <= 0 THEN 1 ELSE 0 END +
            CASE
                WHEN (lb.current_assets / NULLIF(lb.current_liabilities,0)) < 1
                THEN 1
                ELSE 0
            END
        ) = 1 THEN 'Moderate Risk'

        WHEN (
            CASE WHEN lr.return_on_equity_pct < 15 THEN 1 ELSE 0 END +
            CASE WHEN lr.debt_to_equity >= 1 THEN 1 ELSE 0 END +
            CASE WHEN lc.net_cash_flow <= 0 THEN 1 ELSE 0 END +
            CASE
                WHEN (lb.current_assets / NULLIF(lb.current_liabilities,0)) < 1
                THEN 1
                ELSE 0
            END
        ) = 2 THEN 'High Risk'

        ELSE 'Critical Risk'

    END AS risk_category

FROM companies c

LEFT JOIN latest_ratios lr
ON c.id = lr.company_id
AND lr.rn = 1

LEFT JOIN latest_cashflow lc
ON c.id = lc.company_id
AND lc.rn = 1

LEFT JOIN latest_balance lb
ON c.id = lb.company_id
AND lb.rn = 1

ORDER BY
    risk_score DESC,
    debt_to_equity DESC;
"""

    df = pd.read_sql_query(query, connection)
    print(df)
# ==========================================================
# Query 86 - CEO Executive Dashboard
# ==========================================================

query = """
WITH latest_profit AS (
    SELECT
        company_id,
        year,
        sales,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        debt_to_equity,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
),

latest_cashflow AS (
    SELECT
        company_id,
        net_cash_flow,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM cashflow
)

SELECT

    c.company_name,

    s.broad_sector,

    lp.year,

    ROUND(lp.sales,2) AS revenue,

    ROUND(lp.net_profit,2) AS net_profit,

    ROUND(lr.return_on_equity_pct,2) AS roe,

    ROUND(lc.net_cash_flow,2) AS net_cash_flow,

    CASE
        WHEN lr.debt_to_equity < 1
             AND lc.net_cash_flow > 0
        THEN 'Low Risk'

        WHEN lr.debt_to_equity < 2
        THEN 'Moderate Risk'

        ELSE 'High Risk'
    END AS risk_category,

    CASE

        WHEN lr.return_on_equity_pct >= 20
             AND lp.net_profit > 0
             AND lc.net_cash_flow > 0
        THEN 'Excellent'

        WHEN lr.return_on_equity_pct >= 15
             AND lp.net_profit > 0
        THEN 'Good'

        WHEN lr.return_on_equity_pct >= 10
        THEN 'Average'

        ELSE 'Needs Attention'

    END AS ceo_rating

FROM companies c

JOIN sectors s
ON c.id = s.company_id

LEFT JOIN latest_profit lp
ON c.id = lp.company_id
AND lp.rn = 1

LEFT JOIN latest_ratios lr
ON c.id = lr.company_id
AND lr.rn = 1

LEFT JOIN latest_cashflow lc
ON c.id = lc.company_id
AND lc.rn = 1

ORDER BY
    revenue DESC,
    roe DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 86 - CEO Executive Dashboard")
print("====================================================")
print(df)
# ==========================================================
# Query 87 - CFO Executive Dashboard
# ==========================================================

print("\n====================================================")
print("Query 87 - CFO Executive Dashboard")
print("====================================================")

if not HAS_LIQUIDITY_COLS:
    print("SKIPPED: current assets/liabilities columns not found in 'balancesheet'.")
else:
    query = f"""
WITH latest_profit AS (
    SELECT
        company_id,
        year,
        sales,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        debt_to_equity,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
),

latest_balance AS (
    SELECT
        company_id,
        {CURRENT_ASSETS_COL} AS current_assets,
        {CURRENT_LIABILITIES_COL} AS current_liabilities,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM balancesheet
),

latest_cashflow AS (
    SELECT
        company_id,
        net_cash_flow,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM cashflow
)

SELECT

    c.company_name,

    lp.year,

    ROUND(lp.sales,2) AS revenue,

    ROUND(lp.net_profit,2) AS net_profit,

    ROUND(
        (lp.net_profit * 100.0) /
        NULLIF(lp.sales,0),
        2
    ) AS profit_margin,

    ROUND(
        lb.current_assets /
        NULLIF(lb.current_liabilities,0),
        2
    ) AS current_ratio,

    ROUND(lr.debt_to_equity,2) AS debt_to_equity,

    ROUND(lc.net_cash_flow,2) AS net_cash_flow,

    CASE

        WHEN
            (lp.net_profit * 100.0 / NULLIF(lp.sales,0)) >= 15
            AND (lb.current_assets / NULLIF(lb.current_liabilities,0)) >= 1.5
            AND lr.debt_to_equity < 1
        THEN 'Excellent'

        WHEN
            (lp.net_profit * 100.0 / NULLIF(lp.sales,0)) >= 10
            AND (lb.current_assets / NULLIF(lb.current_liabilities,0)) >= 1
        THEN 'Healthy'

        WHEN
            (lp.net_profit * 100.0 / NULLIF(lp.sales,0)) >= 5
        THEN 'Watchlist'

        ELSE 'Critical'

    END AS cfo_financial_status

FROM companies c

LEFT JOIN latest_profit lp
ON c.id = lp.company_id
AND lp.rn = 1

LEFT JOIN latest_ratios lr
ON c.id = lr.company_id
AND lr.rn = 1

LEFT JOIN latest_balance lb
ON c.id = lb.company_id
AND lb.rn = 1

LEFT JOIN latest_cashflow lc
ON c.id = lc.company_id
AND lc.rn = 1

ORDER BY
    profit_margin DESC,
    current_ratio DESC;
"""

    df = pd.read_sql_query(query, connection)
    print(df)
# ==========================================================
# Query 88 - Sector KPI Dashboard
# ==========================================================

query = """
WITH latest_profit AS (
    SELECT
        company_id,
        sales,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        debt_to_equity,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
),

latest_cashflow AS (
    SELECT
        company_id,
        net_cash_flow,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM cashflow
)

SELECT

    s.broad_sector,

    COUNT(DISTINCT c.id) AS total_companies,

    ROUND(SUM(lp.sales),2) AS total_revenue,

    ROUND(SUM(lp.net_profit),2) AS total_net_profit,

    ROUND(AVG(lr.return_on_equity_pct),2) AS average_roe,

    ROUND(AVG(lr.debt_to_equity),2) AS average_debt_to_equity,

    ROUND(AVG(lc.net_cash_flow),2) AS average_net_cash_flow,

    CASE

        WHEN AVG(lr.return_on_equity_pct) >= 20
             AND AVG(lr.debt_to_equity) < 1
             AND AVG(lc.net_cash_flow) > 0
        THEN 'Excellent'

        WHEN AVG(lr.return_on_equity_pct) >= 15
             AND AVG(lr.debt_to_equity) < 1.5
        THEN 'Good'

        WHEN AVG(lr.return_on_equity_pct) >= 10
        THEN 'Average'

        ELSE 'Needs Improvement'

    END AS sector_rating

FROM companies c

JOIN sectors s
ON c.id = s.company_id

LEFT JOIN latest_profit lp
ON c.id = lp.company_id
AND lp.rn = 1

LEFT JOIN latest_ratios lr
ON c.id = lr.company_id
AND lr.rn = 1

LEFT JOIN latest_cashflow lc
ON c.id = lc.company_id
AND lc.rn = 1

GROUP BY
    s.broad_sector

ORDER BY
    total_revenue DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 88 - Sector KPI Dashboard")
print("====================================================")
print(df)
# ==========================================================
# Query 89 - Market Intelligence Dashboard
# ==========================================================

print("\n====================================================")
print("Query 89 - Market Intelligence Dashboard")
print("====================================================")

if not HAS_MARKET_CAP:
    print("SKIPPED: market cap table/column not found in DB.")
else:
    query = f"""
WITH latest_profit AS (
    SELECT
        company_id,
        sales,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
),

latest_market_cap AS (
    SELECT
        company_id,
        {MARKET_CAP_COL} AS market_cap,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM {MARKET_CAP_TABLE}
)

SELECT

    c.company_name,

    s.broad_sector,

    ROUND(mc.market_cap,2) AS market_cap,

    ROUND(lp.sales,2) AS revenue,

    ROUND(lp.net_profit,2) AS net_profit,

    ROUND(lr.return_on_equity_pct,2) AS roe,

    CASE

        WHEN mc.market_cap >= 100000
             AND lr.return_on_equity_pct >= 20
        THEN 'Market Leader'

        WHEN mc.market_cap >= 50000
             AND lr.return_on_equity_pct >= 15
        THEN 'Strong Performer'

        WHEN mc.market_cap >= 10000
        THEN 'Emerging Leader'

        ELSE 'Developing Company'

    END AS market_position

FROM companies c

JOIN sectors s
ON c.id = s.company_id

LEFT JOIN latest_market_cap mc
ON c.id = mc.company_id
AND mc.rn = 1

LEFT JOIN latest_profit lp
ON c.id = lp.company_id
AND lp.rn = 1

LEFT JOIN latest_ratios lr
ON c.id = lr.company_id
AND lr.rn = 1

ORDER BY
    market_cap DESC,
    roe DESC;
"""

    df = pd.read_sql_query(query, connection)
    print(df)
# ==========================================================
# Query 90 - Executive Summary Dashboard
# ==========================================================

print("\n====================================================")
print("Query 90 - Executive Summary Dashboard")
print("====================================================")

if not HAS_MARKET_CAP:
    print("SKIPPED: market cap table/column not found in DB.")
else:
    query = f"""
WITH latest_profit AS (
    SELECT
        company_id,
        year,
        sales,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        debt_to_equity,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
),

latest_cashflow AS (
    SELECT
        company_id,
        net_cash_flow,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM cashflow
),

latest_marketcap AS (
    SELECT
        company_id,
        {MARKET_CAP_COL} AS market_cap,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM {MARKET_CAP_TABLE}
)

SELECT

    c.company_name,

    s.broad_sector,

    lp.year,

    ROUND(mc.market_cap,2) AS market_cap,

    ROUND(lp.sales,2) AS revenue,

    ROUND(lp.net_profit,2) AS net_profit,

    ROUND(lr.return_on_equity_pct,2) AS roe,

    ROUND(lr.debt_to_equity,2) AS debt_to_equity,

    ROUND(lc.net_cash_flow,2) AS net_cash_flow,

    CASE

        WHEN lr.return_on_equity_pct >= 20
             AND lp.net_profit > 0
             AND lc.net_cash_flow > 0
             AND lr.debt_to_equity < 1
        THEN 'Excellent'

        WHEN lr.return_on_equity_pct >= 15
             AND lp.net_profit > 0
        THEN 'Good'

        WHEN lr.return_on_equity_pct >= 10
        THEN 'Average'

        ELSE 'Needs Attention'

    END AS business_status

FROM companies c

JOIN sectors s
ON c.id = s.company_id

LEFT JOIN latest_profit lp
ON c.id = lp.company_id
AND lp.rn = 1

LEFT JOIN latest_ratios lr
ON c.id = lr.company_id
AND lr.rn = 1

LEFT JOIN latest_cashflow lc
ON c.id = lc.company_id
AND lc.rn = 1

LEFT JOIN latest_marketcap mc
ON c.id = mc.company_id
AND mc.rn = 1

ORDER BY
    market_cap DESC,
    revenue DESC;
"""

    df = pd.read_sql_query(query, connection)
    print(df)
# ==========================================================
# Query 91 - Revenue Trend Analysis
# ==========================================================

query = """
WITH revenue_trend AS (

    SELECT

        company_id,

        year,

        sales,

        LAG(sales) OVER (
            PARTITION BY company_id
            ORDER BY year
        ) AS previous_revenue

    FROM profitandloss

    WHERE sales IS NOT NULL

)

SELECT

    c.company_name,

    rt.year,

    ROUND(rt.sales,2) AS current_revenue,

    ROUND(rt.previous_revenue,2) AS previous_revenue,

    ROUND(
        (
            (rt.sales - rt.previous_revenue) * 100.0
        ) / NULLIF(rt.previous_revenue,0),
        2
    ) AS revenue_growth_pct,

    CASE

        WHEN rt.previous_revenue IS NULL
        THEN 'No Previous Data'

        WHEN (
            (rt.sales - rt.previous_revenue) * 100.0
        ) / NULLIF(rt.previous_revenue,0) > 10
        THEN 'High Growth'

        WHEN (
            (rt.sales - rt.previous_revenue) * 100.0
        ) / NULLIF(rt.previous_revenue,0) >= 0
        THEN 'Stable Growth'

        ELSE 'Declining'

    END AS revenue_trend

FROM revenue_trend rt

JOIN companies c
ON rt.company_id = c.id

ORDER BY
    c.company_name,
    rt.year;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 91 - Revenue Trend Analysis")
print("====================================================")
print(df)
# ==========================================================
# Query 92 - Net Profit Trend Analysis
# ==========================================================

query = """
WITH profit_trend AS (

    SELECT

        company_id,

        year,

        net_profit,

        LAG(net_profit) OVER (
            PARTITION BY company_id
            ORDER BY year
        ) AS previous_profit

    FROM profitandloss

    WHERE net_profit IS NOT NULL

)

SELECT

    c.company_name,

    pt.year,

    ROUND(pt.net_profit,2) AS current_profit,

    ROUND(pt.previous_profit,2) AS previous_profit,

    ROUND(
        (
            (pt.net_profit - pt.previous_profit) * 100.0
        ) / NULLIF(pt.previous_profit,0),
        2
    ) AS profit_growth_pct,

    CASE

        WHEN pt.previous_profit IS NULL
            THEN 'No Previous Data'

        WHEN (
            (pt.net_profit - pt.previous_profit) * 100.0
        ) / NULLIF(pt.previous_profit,0) > 15
            THEN 'Strong Growth'

        WHEN (
            (pt.net_profit - pt.previous_profit) * 100.0
        ) / NULLIF(pt.previous_profit,0) >= 0
            THEN 'Stable Growth'

        ELSE 'Profit Decline'

    END AS profit_trend

FROM profit_trend pt

JOIN companies c
ON pt.company_id = c.id

ORDER BY
    c.company_name,
    pt.year;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 92 - Net Profit Trend Analysis")
print("====================================================")
print(df)
# ==========================================================
# Query 93 - ROE Trend Analysis
# ==========================================================

query = """
WITH roe_trend AS (

    SELECT

        company_id,

        year,

        return_on_equity_pct,

        LAG(return_on_equity_pct) OVER (
            PARTITION BY company_id
            ORDER BY year
        ) AS previous_roe

    FROM financial_ratios

    WHERE return_on_equity_pct IS NOT NULL

)

SELECT

    c.company_name,

    rt.year,

    ROUND(rt.return_on_equity_pct,2) AS current_roe,

    ROUND(rt.previous_roe,2) AS previous_roe,

    ROUND(
        rt.return_on_equity_pct - rt.previous_roe,
        2
    ) AS roe_change,

    CASE

        WHEN rt.previous_roe IS NULL
        THEN 'No Previous Data'

        WHEN (rt.return_on_equity_pct - rt.previous_roe) > 2
        THEN 'Improving'

        WHEN (rt.return_on_equity_pct - rt.previous_roe) >= -2
        THEN 'Stable'

        ELSE 'Declining'

    END AS roe_trend

FROM roe_trend rt

JOIN companies c
ON rt.company_id = c.id

ORDER BY
    c.company_name,
    rt.year;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 93 - ROE Trend Analysis")
print("====================================================")
print(df)
# ==========================================================
# Query 94 - Cash Flow Trend Analysis
# ==========================================================

query = """
WITH cashflow_trend AS (

    SELECT

        company_id,

        year,

        net_cash_flow,

        LAG(net_cash_flow) OVER (
            PARTITION BY company_id
            ORDER BY year
        ) AS previous_cash_flow

    FROM cashflow

    WHERE net_cash_flow IS NOT NULL

)

SELECT

    c.company_name,

    ct.year,

    ROUND(ct.net_cash_flow,2) AS current_cash_flow,

    ROUND(ct.previous_cash_flow,2) AS previous_cash_flow,

    ROUND(
        ct.net_cash_flow - ct.previous_cash_flow,
        2
    ) AS cash_flow_change,

    CASE

        WHEN ct.previous_cash_flow IS NULL
        THEN 'No Previous Data'

        WHEN (ct.net_cash_flow - ct.previous_cash_flow) > 1000
        THEN 'Improving'

        WHEN (ct.net_cash_flow - ct.previous_cash_flow) >= -1000
        THEN 'Stable'

        ELSE 'Declining'

    END AS cash_flow_trend

FROM cashflow_trend ct

JOIN companies c
ON ct.company_id = c.id

ORDER BY
    c.company_name,
    ct.year;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 94 - Cash Flow Trend Analysis")
print("====================================================")
print(df)
# ==========================================================
# Query 95 - Business Growth Trend Dashboard
# ==========================================================

query = """
WITH financial_trends AS (

    SELECT

        p.company_id,

        p.year,

        p.sales,

        p.net_profit,

        r.return_on_equity_pct,

        LAG(p.sales) OVER (
            PARTITION BY p.company_id
            ORDER BY p.year
        ) AS previous_sales,

        LAG(p.net_profit) OVER (
            PARTITION BY p.company_id
            ORDER BY p.year
        ) AS previous_profit

    FROM profitandloss p

    JOIN financial_ratios r
    ON p.company_id = r.company_id
    AND p.year = r.year

)

SELECT

    c.company_name,

    ft.year,

    ROUND(ft.sales,2) AS revenue,

    ROUND(ft.net_profit,2) AS net_profit,

    ROUND(ft.return_on_equity_pct,2) AS roe,

    ROUND(
        ((ft.sales - ft.previous_sales) * 100.0) /
        NULLIF(ft.previous_sales,0),
        2
    ) AS revenue_growth_pct,

    ROUND(
        ((ft.net_profit - ft.previous_profit) * 100.0) /
        NULLIF(ft.previous_profit,0),
        2
    ) AS profit_growth_pct,

    CASE

        WHEN
            ((ft.sales - ft.previous_sales) * 100.0 /
            NULLIF(ft.previous_sales,0)) >= 10

            AND

            ((ft.net_profit - ft.previous_profit) * 100.0 /
            NULLIF(ft.previous_profit,0)) >= 10

            AND ft.return_on_equity_pct >= 20

        THEN 'High Growth'

        WHEN
            ((ft.sales - ft.previous_sales) * 100.0 /
            NULLIF(ft.previous_sales,0)) >= 0

            AND

            ((ft.net_profit - ft.previous_profit) * 100.0 /
            NULLIF(ft.previous_profit,0)) >= 0

        THEN 'Stable Growth'

        ELSE 'Declining'

    END AS overall_growth_status

FROM financial_trends ft

JOIN companies c
ON ft.company_id = c.id

ORDER BY

    overall_growth_status DESC,

    revenue_growth_pct DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n====================================================")
print("Query 95 - Business Growth Trend Dashboard")
print("====================================================")
print(df)
# ==========================================================
# Query 96 - Enterprise Financial Scorecard
# ==========================================================

print("\n====================================================")
print("Query 96 - Enterprise Financial Scorecard")
print("====================================================")

if not HAS_LIQUIDITY_COLS:
    print("SKIPPED: current assets/liabilities columns not found in 'balancesheet'.")
else:
    query = f"""
WITH latest_profit AS (
    SELECT
        company_id,
        sales,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        debt_to_equity,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
),

latest_balance AS (
    SELECT
        company_id,
        {CURRENT_ASSETS_COL} AS current_assets,
        {CURRENT_LIABILITIES_COL} AS current_liabilities,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM balancesheet
),

latest_cashflow AS (
    SELECT
        company_id,
        net_cash_flow,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM cashflow
)

SELECT

    c.company_name,

    s.broad_sector,

    ROUND(lp.sales,2) AS revenue,

    ROUND(lp.net_profit,2) AS net_profit,

    ROUND(lr.return_on_equity_pct,2) AS roe,

    ROUND(lr.debt_to_equity,2) AS debt_to_equity,

    ROUND(
        lb.current_assets /
        NULLIF(lb.current_liabilities,0),
        2
    ) AS current_ratio,

    ROUND(lc.net_cash_flow,2) AS net_cash_flow,

    CASE

        WHEN lr.return_on_equity_pct >= 20
             AND (lb.current_assets / NULLIF(lb.current_liabilities,0)) >= 1.5
             AND lr.debt_to_equity < 1
             AND lc.net_cash_flow > 0
        THEN 'Excellent'

        WHEN lr.return_on_equity_pct >= 15
             AND (lb.current_assets / NULLIF(lb.current_liabilities,0)) >= 1
        THEN 'Strong'

        WHEN lr.return_on_equity_pct >= 10
        THEN 'Moderate'

        ELSE 'Weak'

    END AS enterprise_rating

FROM companies c

JOIN sectors s
ON c.id = s.company_id

LEFT JOIN latest_profit lp
ON c.id = lp.company_id
AND lp.rn = 1

LEFT JOIN latest_ratios lr
ON c.id = lr.company_id
AND lr.rn = 1

LEFT JOIN latest_balance lb
ON c.id = lb.company_id
AND lb.rn = 1

LEFT JOIN latest_cashflow lc
ON c.id = lc.company_id
AND lc.rn = 1

ORDER BY
    roe DESC,
    revenue DESC;
"""

    df = pd.read_sql_query(query, connection)
    print(df)
# ==========================================================
# Query 97 - Investment Opportunity Dashboard
# ==========================================================

print("\n====================================================")
print("Query 97 - Investment Opportunity Dashboard")
print("====================================================")

if not HAS_MARKET_CAP:
    print("SKIPPED: market cap table/column not found in DB.")
else:
    query = f"""
WITH latest_profit AS (
    SELECT
        company_id,
        sales,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        debt_to_equity,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
),

latest_cashflow AS (
    SELECT
        company_id,
        net_cash_flow,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM cashflow
),

latest_marketcap AS (
    SELECT
        company_id,
        {MARKET_CAP_COL} AS market_cap,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM {MARKET_CAP_TABLE}
)

SELECT

    c.company_name,

    s.broad_sector,

    ROUND(mc.market_cap,2) AS market_cap,

    ROUND(lp.sales,2) AS revenue,

    ROUND(lp.net_profit,2) AS net_profit,

    ROUND(lr.return_on_equity_pct,2) AS roe,

    ROUND(lr.debt_to_equity,2) AS debt_to_equity,

    ROUND(lc.net_cash_flow,2) AS net_cash_flow,

    CASE

        WHEN lr.return_on_equity_pct >= 20
             AND lr.debt_to_equity < 1
             AND lc.net_cash_flow > 0
        THEN 'Strong Buy'

        WHEN lr.return_on_equity_pct >= 15
             AND lr.debt_to_equity < 1.5
        THEN 'Buy'

        WHEN lr.return_on_equity_pct >= 10
        THEN 'Hold'

        ELSE 'Avoid'

    END AS investment_rating

FROM companies c

JOIN sectors s
ON c.id = s.company_id

LEFT JOIN latest_marketcap mc
ON c.id = mc.company_id
AND mc.rn = 1

LEFT JOIN latest_profit lp
ON c.id = lp.company_id
AND lp.rn = 1

LEFT JOIN latest_ratios lr
ON c.id = lr.company_id
AND lr.rn = 1

LEFT JOIN latest_cashflow lc
ON c.id = lc.company_id
AND lc.rn = 1

ORDER BY

    investment_rating,

    roe DESC,

    market_cap DESC;
"""

    df = pd.read_sql_query(query, connection)
    print(df)
# ==========================================================
# Query 98 - Company Performance Index
# ==========================================================

print("\n====================================================")
print("Query 98 - Company Performance Index")
print("====================================================")

if not HAS_LIQUIDITY_COLS:
    print("SKIPPED: current assets/liabilities columns not found in 'balancesheet'.")
else:
    query = f"""
WITH latest_profit AS (
    SELECT
        company_id,
        sales,
        net_profit,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM profitandloss
),

latest_ratios AS (
    SELECT
        company_id,
        return_on_equity_pct,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM financial_ratios
),

latest_balance AS (
    SELECT
        company_id,
        {CURRENT_ASSETS_COL} AS current_assets,
        {CURRENT_LIABILITIES_COL} AS current_liabilities,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM balancesheet
),

latest_cashflow AS (
    SELECT
        company_id,
        net_cash_flow,
        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS rn
    FROM cashflow
)

SELECT

    c.company_name,

    s.broad_sector,

    ROUND(lp.sales,2) AS revenue,

    ROUND(lp.net_profit,2) AS net_profit,

    ROUND(lr.return_on_equity_pct,2) AS roe,

    ROUND(lc.net_cash_flow,2) AS net_cash_flow,

    ROUND(

        (
            lr.return_on_equity_pct * 0.40

            +

            ((lp.net_profit * 100.0 /
            NULLIF(lp.sales,0)) * 0.30)

            +

            ((lb.current_assets /
            NULLIF(lb.current_liabilities,0)) * 0.20)

            +

            (
                CASE
                    WHEN lc.net_cash_flow > 0
                    THEN 10
                    ELSE 0
                END
            ) * 0.10

        ),

        2

    ) AS performance_score,

    CASE

        WHEN (

            lr.return_on_equity_pct * 0.40

            +

            ((lp.net_profit * 100.0 /
            NULLIF(lp.sales,0)) * 0.30)

            +

            ((lb.current_assets /
            NULLIF(lb.current_liabilities,0)) * 0.20)

            +

            (
                CASE
                    WHEN lc.net_cash_flow > 0
                    THEN 10
                    ELSE 0
                END
            ) * 0.10

        ) >= 25

        THEN 'A+'

        WHEN (

            lr.return_on_equity_pct * 0.40

            +

            ((lp.net_profit * 100.0 /
            NULLIF(lp.sales,0)) * 0.30)

            +

            ((lb.current_assets /
            NULLIF(lb.current_liabilities,0)) * 0.20)

            +

            (
                CASE
                    WHEN lc.net_cash_flow > 0
                    THEN 10
                    ELSE 0
                END
            ) * 0.10

        ) >= 20

        THEN 'A'

        WHEN (

            lr.return_on_equity_pct * 0.40

            +

            ((lp.net_profit * 100.0 /
            NULLIF(lp.sales,0)) * 0.30)

            +

            ((lb.current_assets /
            NULLIF(lb.current_liabilities,0)) * 0.20)

            +

            (
                CASE
                    WHEN lc.net_cash_flow > 0
                    THEN 10
                    ELSE 0
                END
            ) * 0.10

        ) >= 15

        THEN 'B'

        WHEN (

            lr.return_on_equity_pct * 0.40

            +

            ((lp.net_profit * 100.0 /
            NULLIF(lp.sales,0)) * 0.30)

            +

            ((lb.current_assets /
            NULLIF(lb.current_liabilities,0)) * 0.20)

            +

            (
                CASE
                    WHEN lc.net_cash_flow > 0
                    THEN 10
                    ELSE 0
                END
            ) * 0.10

        ) >= 10

        THEN 'C'

        ELSE 'D'

    END AS performance_grade

FROM companies c

JOIN sectors s
ON c.id = s.company_id

LEFT JOIN latest_profit lp
ON c.id = lp.company_id
AND lp.rn = 1

LEFT JOIN latest_ratios lr
ON c.id = lr.company_id
AND lr.rn = 1

LEFT JOIN latest_balance lb
ON c.id = lb.company_id
AND lb.rn = 1

LEFT JOIN latest_cashflow lc
ON c.id = lc.company_id
AND lc.rn = 1

ORDER BY
    performance_score DESC;
"""

    df = pd.read_sql_query(query, connection)
    print(df)
# ==========================================================
# Query 99 - Market Leaders Dashboard
# ==========================================================

print("\n====================================================")
print("Query 99 - Market Leaders Dashboard")
print("====================================================")

query = """
WITH latest_profit AS (

    SELECT
        company_id,
        sales,
        net_profit,
        ROW_NUMBER() OVER(
            PARTITION BY company_id
            ORDER BY year DESC
        ) rn
    FROM profitandloss
),

latest_ratios AS (

    SELECT
        company_id,
        return_on_equity_pct,
        debt_to_equity,
        ROW_NUMBER() OVER(
            PARTITION BY company_id
            ORDER BY year DESC
        ) rn
    FROM financial_ratios
)

SELECT

RANK() OVER(
ORDER BY
lp.sales DESC,
lp.net_profit DESC,
lr.return_on_equity_pct DESC
) AS company_rank,

c.company_name,

s.broad_sector,

ROUND(lp.sales,2) revenue,

ROUND(lp.net_profit,2) net_profit,

ROUND(lr.return_on_equity_pct,2) roe,

ROUND(lr.debt_to_equity,2) debt_to_equity,

CASE

WHEN lp.sales>=100000
AND lr.return_on_equity_pct>=20
THEN 'Elite Leader'

WHEN lp.sales>=50000
THEN 'Market Leader'

WHEN lp.sales>=10000
THEN 'Emerging Leader'

ELSE 'Growth Company'

END AS leader_category

FROM companies c

JOIN sectors s
ON c.id=s.company_id

LEFT JOIN latest_profit lp
ON c.id=lp.company_id
AND lp.rn=1

LEFT JOIN latest_ratios lr
ON c.id=lr.company_id
AND lr.rn=1

ORDER BY company_rank;
"""

df = pd.read_sql_query(query, connection)

print(df)
# ==========================================================
# Query 100 - Executive Analytics Dashboard
# ==========================================================

print("\n====================================================")
print("Query 100 - Executive Analytics Dashboard")
print("====================================================")

query = """

WITH latest_profit AS (

SELECT
company_id,
sales,
net_profit,
ROW_NUMBER() OVER(
PARTITION BY company_id
ORDER BY year DESC
) rn

FROM profitandloss

),

latest_ratios AS (

SELECT
company_id,
return_on_equity_pct,
net_profit_margin_pct,
operating_profit_margin_pct,
debt_to_equity,
free_cash_flow_cr,

ROW_NUMBER() OVER(
PARTITION BY company_id
ORDER BY year DESC
) rn

FROM financial_ratios

),

latest_balance AS (

SELECT

company_id,

total_assets,

total_liabilities,

ROW_NUMBER() OVER(
PARTITION BY company_id
ORDER BY year DESC
) rn

FROM balancesheet

),

latest_cashflow AS (

SELECT

company_id,

net_cash_flow,

ROW_NUMBER() OVER(
PARTITION BY company_id
ORDER BY year DESC
) rn

FROM cashflow

)

SELECT

c.company_name,

s.broad_sector,

ROUND(lp.sales,2) revenue,

ROUND(lp.net_profit,2) net_profit,

ROUND(lb.total_assets,2) total_assets,

ROUND(lb.total_liabilities,2) total_liabilities,

ROUND(lr.return_on_equity_pct,2) roe,

ROUND(lr.net_profit_margin_pct,2) profit_margin,

ROUND(lr.operating_profit_margin_pct,2) operating_margin,

ROUND(lr.debt_to_equity,2) debt_to_equity,

ROUND(lc.net_cash_flow,2) net_cash_flow,

ROUND(

(
lr.return_on_equity_pct*0.40
+
lr.net_profit_margin_pct*0.30
+
lr.operating_profit_margin_pct*0.20
+
CASE
WHEN lc.net_cash_flow>0
THEN 10
ELSE 0
END

),2

) performance_score,

CASE

WHEN lr.return_on_equity_pct>=20
AND lr.debt_to_equity<1
THEN 'Excellent'

WHEN lr.return_on_equity_pct>=15
THEN 'Strong'

WHEN lr.return_on_equity_pct>=10
THEN 'Moderate'

ELSE 'Weak'

END executive_status

FROM companies c

JOIN sectors s
ON c.id=s.company_id

LEFT JOIN latest_profit lp
ON c.id=lp.company_id
AND lp.rn=1

LEFT JOIN latest_ratios lr
ON c.id=lr.company_id
AND lr.rn=1

LEFT JOIN latest_balance lb
ON c.id=lb.company_id
AND lb.rn=1

LEFT JOIN latest_cashflow lc
ON c.id=lc.company_id
AND lc.rn=1

ORDER BY performance_score DESC;

"""

df = pd.read_sql_query(query, connection)

print(df)
# ==========================================================
# Close Connection
# ==========================================================

connection.close()

print("\nAnalytics Completed Successfully")