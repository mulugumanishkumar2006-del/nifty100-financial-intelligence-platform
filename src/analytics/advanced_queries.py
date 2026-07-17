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

query = """
WITH revenue_data AS (
    SELECT
        company_id,
        year,
        sales,

        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year ASC
        ) AS first_year,

        ROW_NUMBER() OVER (
            PARTITION BY company_id
            ORDER BY year DESC
        ) AS last_year

    FROM profitandloss

    WHERE sales IS NOT NULL
),

first_sales AS (
    SELECT
        company_id,
        year AS start_year,
        sales AS start_sales
    FROM revenue_data
    WHERE first_year = 1
),

last_sales AS (
    SELECT
        company_id,
        year AS end_year,
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
                (CAST(ls.end_year AS INTEGER) -
                 CAST(fs.start_year AS INTEGER))
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
    AND CAST(ls.end_year AS INTEGER) >
        CAST(fs.start_year AS INTEGER)

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

query = """
WITH latest_ratios AS (
    SELECT
        company_id,
        year,
        return_on_equity_pct,
        return_on_capital_employed_pct,
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

    ROUND(lr.return_on_capital_employed_pct, 2) AS roce,

    ROUND(
        lr.return_on_equity_pct -
        lr.return_on_capital_employed_pct,
        2
    ) AS roe_roce_difference

FROM latest_ratios lr

JOIN companies c
ON lr.company_id = c.id

WHERE
    lr.rn = 1
    AND lr.return_on_equity_pct IS NOT NULL
    AND lr.return_on_capital_employed_pct IS NOT NULL

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
# Close Connection
# ==========================================================

connection.close()

print("\nAnalytics Completed Successfully")