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
# Close Connection
# ==========================================================

connection.close()

print("\nAnalytics Completed Successfully")