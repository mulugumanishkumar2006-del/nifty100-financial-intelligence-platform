import sqlite3
from pathlib import Path
import pandas as pd

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE = PROJECT_ROOT / "database" / "nifty100.db"


def run_query(connection, title, query):
    """Execute a SQL query, print the results, and return the DataFrame."""
    try:
        print("\n" + "=" * 60)
        print(title)
        print("=" * 60)
        df = pd.read_sql_query(query, connection)
        print(df)
        return df
    except Exception as e:
        print(f"❌ Error while executing query: {title}")
        print(e)
        return None


def main():
    if not DATABASE.exists():
        print("❌ Database not found!")
        print(DATABASE)
        return

    connection = sqlite3.connect(DATABASE)
    print("✅ Connected Successfully")

    # ======================================================
    # Query 1 - Total Companies
    # ======================================================
    run_query(
        connection,
        "Total Companies",
        """
        SELECT COUNT(*) AS total_companies
        FROM companies;
        """
    )

    # ======================================================
    # Query 2 - Total Profit & Loss Records
    # ======================================================
    run_query(
        connection,
        "Total Profit & Loss Records",
        """
        SELECT COUNT(*) AS total_profit_records
        FROM profitandloss;
        """
    )

    # ======================================================
    # Query 3 - Total Balance Sheet Records
    # ======================================================
    run_query(
        connection,
        "Total Balance Sheet Records",
        """
        SELECT COUNT(*) AS total_balance_records
        FROM balancesheet;
        """
    )

    # ======================================================
    # Query 4 - Total Cash Flow Records
    # ======================================================
    run_query(
        connection,
        "Total Cash Flow Records",
        """
        SELECT COUNT(*) AS total_cashflow_records
        FROM cashflow;
        """
    )

    # ======================================================
    # Query 5 - Top 10 Companies by ROE
    # ======================================================
    run_query(
        connection,
        "Top 10 Companies by ROE",
        """
        SELECT
            company_name,
            roe_percentage
        FROM companies
        WHERE roe_percentage IS NOT NULL
        ORDER BY roe_percentage DESC
        LIMIT 10;
        """
    )

    # ======================================================
    # Query 6 - Top 10 Companies by ROCE
    # ======================================================
    run_query(
        connection,
        "Top 10 Companies by ROCE",
        """
        SELECT
            company_name,
            roce_percentage
        FROM companies
        WHERE roce_percentage IS NOT NULL
        ORDER BY roce_percentage DESC
        LIMIT 10;
        """
    )

    # ======================================================
    # Query 7 - Top 10 Companies by Book Value
    # ======================================================
    run_query(
        connection,
        "Top 10 Companies by Book Value",
        """
        SELECT
            company_name,
            book_value
        FROM companies
        WHERE book_value IS NOT NULL
        ORDER BY book_value DESC
        LIMIT 10;
        """
    )

    # ======================================================
    # Query 8 - Top 10 Highest EPS
    # ======================================================
    run_query(
        connection,
        "Top 10 Highest EPS",
        """
        SELECT
            company_id,
            year,
            eps
        FROM profitandloss
        WHERE eps IS NOT NULL
        ORDER BY eps DESC
        LIMIT 10;
        """
    )

    # ==========================================================
    # Query 9 - Top 10 Companies by Net Profit
    # ==========================================================
    run_query(
        connection,
        "Top 10 Companies by Net Profit",
        """
        SELECT
            company_id,
            year,
            net_profit
        FROM profitandloss
        WHERE net_profit IS NOT NULL
        ORDER BY net_profit DESC
        LIMIT 10;
        """
    )

    # ==========================================================
    # Query 10 - Top 10 Companies by Net Profit (Using JOIN)
    # ==========================================================
    run_query(
        connection,
        "Top 10 Companies by Net Profit (JOIN)",
        """
        SELECT
            c.company_name,
            p.year,
            p.net_profit
        FROM companies c
        INNER JOIN profitandloss p
        ON c.id = p.company_id
        WHERE p.net_profit IS NOT NULL
        ORDER BY p.net_profit DESC
        LIMIT 10;
        """
    )

    # ==========================================================
    # Query 11 - Top 10 Companies by ROE (Using JOIN)
    # ==========================================================
    run_query(
        connection,
        "Top 10 Companies by ROE (JOIN)",
        """
        SELECT
            c.company_name,
            c.roe_percentage
        FROM companies c
        WHERE c.roe_percentage IS NOT NULL
        ORDER BY c.roe_percentage DESC
        LIMIT 10;
        """
    )

    # ==========================================================
    # Query 12 - Number of Financial Records per Company
    # ==========================================================
    run_query(
        connection,
        "Top 10 Companies by Number of Financial Records",
        """
        SELECT
            c.company_name,
            COUNT(p.id) AS total_records
        FROM companies c
        INNER JOIN profitandloss p
        ON c.id = p.company_id
        GROUP BY c.company_name
        ORDER BY total_records DESC
        LIMIT 10;
        """
    )

    # ==========================================================
    # Query 13 - Highest Net Profit by Company
    # ==========================================================
    run_query(
        connection,
        "Top 10 Companies by Highest Net Profit",
        """
        SELECT
            c.company_name,
            MAX(p.net_profit) AS highest_net_profit
        FROM companies c
        INNER JOIN profitandloss p
        ON c.id = p.company_id
        WHERE p.net_profit IS NOT NULL
        GROUP BY c.company_name
        ORDER BY highest_net_profit DESC
        LIMIT 10;
        """
    )

    # ==========================================================
    # Query 14 - Lowest Net Profit by Company
    # ==========================================================
    run_query(
        connection,
        "Top 10 Companies by Lowest Net Profit",
        """
        SELECT
            c.company_name,
            MIN(p.net_profit) AS lowest_net_profit
        FROM companies c
        INNER JOIN profitandloss p
        ON c.id = p.company_id
        WHERE p.net_profit IS NOT NULL
        GROUP BY c.company_name
        ORDER BY lowest_net_profit ASC
        LIMIT 10;
        """
    )

    # ==========================================================
    # Query 15 - Companies with Average Net Profit > 1000
    # ==========================================================
    run_query(
        connection,
        "Companies with Average Net Profit Greater Than 1000",
        """
        SELECT
            c.company_name,
            ROUND(AVG(p.net_profit), 2) AS average_net_profit
        FROM companies c
        INNER JOIN profitandloss p
        ON c.id = p.company_id
        WHERE p.net_profit IS NOT NULL
        GROUP BY c.company_name
        HAVING AVG(p.net_profit) > 1000
        ORDER BY average_net_profit DESC;
        """
    )

    # ==========================================================
    # Query 16 - Company Financial Summary (3-Table JOIN)
    # ==========================================================
    run_query(
        connection,
        "Company Financial Summary",
        """
        SELECT
            c.company_name,
            p.year,
            p.net_profit,
            f.debt_to_equity
        FROM companies c
        INNER JOIN profitandloss p
            ON c.id = p.company_id
        INNER JOIN financial_ratios f
            ON c.id = f.company_id
            AND p.year = f.year
        WHERE p.net_profit IS NOT NULL
        ORDER BY p.net_profit DESC
        LIMIT 20;
        """
    )

    # ==========================================================
    # Query 17 - Companies Above Overall Average Net Profit
    # ==========================================================
    run_query(
        connection,
        "Companies with Above Average Net Profit",
        """
        SELECT
            c.company_name,
            ROUND(AVG(p.net_profit), 2) AS average_net_profit
        FROM companies c
        INNER JOIN profitandloss p
            ON c.id = p.company_id
        WHERE p.net_profit IS NOT NULL
        GROUP BY c.company_name
        HAVING AVG(p.net_profit) >
        (
            SELECT AVG(net_profit)
            FROM profitandloss
            WHERE net_profit IS NOT NULL
        )
        ORDER BY average_net_profit DESC;
        """
    )

    # ==========================================================
    # Query 18 - Company Average Net Profit using CTE
    # ==========================================================
    run_query(
        connection,
        "Top 10 Companies by Average Net Profit (Using CTE)",
        """
        WITH company_profit AS (
            SELECT
                c.company_name,
                AVG(p.net_profit) AS average_net_profit
            FROM companies c
            INNER JOIN profitandloss p
                ON c.id = p.company_id
            WHERE p.net_profit IS NOT NULL
            GROUP BY c.company_name
        )
        SELECT
            company_name,
            ROUND(average_net_profit, 2) AS average_net_profit
        FROM company_profit
        ORDER BY average_net_profit DESC
        LIMIT 10;
        """
    )

    # ==========================================================
    # Query 19 - Rank Companies by Average Net Profit
    # ==========================================================
    run_query(
        connection,
        "Company Ranking by Average Net Profit",
        """
        WITH company_profit AS (
            SELECT
                c.company_name,
                ROUND(AVG(p.net_profit), 2) AS average_net_profit
            FROM companies c
            INNER JOIN profitandloss p
                ON c.id = p.company_id
            WHERE p.net_profit IS NOT NULL
            GROUP BY c.company_name
        )
        SELECT
            company_name,
            average_net_profit,
            RANK() OVER (
                ORDER BY average_net_profit DESC
            ) AS company_rank
        FROM company_profit
        LIMIT 20;
        """
    )

    # ==========================================================
    # Query 20 - Dense Rank Companies by Average Net Profit
    # ==========================================================
    run_query(
        connection,
        "Company Dense Ranking by Average Net Profit",
        """
        WITH company_profit AS (
            SELECT
                c.company_name,
                ROUND(AVG(p.net_profit), 2) AS average_net_profit
            FROM companies c
            INNER JOIN profitandloss p
                ON c.id = p.company_id
            WHERE p.net_profit IS NOT NULL
            GROUP BY c.company_name
        )
        SELECT
            company_name,
            average_net_profit,
            DENSE_RANK() OVER (
                ORDER BY average_net_profit DESC
            ) AS company_rank
        FROM company_profit
        LIMIT 20;
        """
    )

    # ==========================================================
    # Query 21 - Row Number by Average Net Profit
    # ==========================================================
    run_query(
        connection,
        "Company Row Number by Average Net Profit",
        """
        WITH company_profit AS (
            SELECT
                c.company_name,
                ROUND(AVG(p.net_profit), 2) AS average_net_profit
            FROM companies c
            INNER JOIN profitandloss p
                ON c.id = p.company_id
            WHERE p.net_profit IS NOT NULL
            GROUP BY c.company_name
        )
        SELECT
            company_name,
            average_net_profit,
            ROW_NUMBER() OVER (
                ORDER BY average_net_profit DESC
            ) AS row_number
        FROM company_profit
        LIMIT 20;
        """
    )

    # ==========================================================
    # Query 22 - Rank Companies Within Each Year
    # ==========================================================
    run_query(
        connection,
        "Company Ranking Within Each Year",
        """
        SELECT
            company_id,
            year,
            net_profit,
            RANK() OVER (
                PARTITION BY year
                ORDER BY net_profit DESC
            ) AS yearly_rank
        FROM profitandloss
        WHERE net_profit IS NOT NULL
        ORDER BY year, yearly_rank;
        """
    )

    # ==========================================================
    # Query 23 - Running Total of Net Profit
    # ==========================================================
    run_query(
        connection,
        "Running Total of Net Profit",
        """
        SELECT
            company_id,
            year,
            net_profit,
            SUM(net_profit) OVER (
                PARTITION BY company_id
                ORDER BY year
            ) AS running_total_profit
        FROM profitandloss
        WHERE net_profit IS NOT NULL
        ORDER BY company_id, year;
        """
    )

    # ==========================================================
    # Query 24 - Moving Average of Net Profit
    # ==========================================================
    run_query(
        connection,
        "Moving Average of Net Profit",
        """
        SELECT
            company_id,
            year,
            net_profit,
            ROUND(
                AVG(net_profit) OVER (
                    PARTITION BY company_id
                    ORDER BY year
                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                ),
                2
            ) AS moving_average_profit
        FROM profitandloss
        WHERE net_profit IS NOT NULL
        ORDER BY company_id, year;
        """
    )

    # ==========================================================
    # Query 25 - Top 3 Companies by Net Profit Each Year
    # ==========================================================
    run_query(
        connection,
        "Top 3 Companies by Net Profit Each Year",
        """
        WITH ranked_companies AS (
            SELECT
                c.company_name,
                p.year,
                p.net_profit,
                ROW_NUMBER() OVER (
                    PARTITION BY p.year
                    ORDER BY p.net_profit DESC
                ) AS rank_in_year
            FROM companies c
            INNER JOIN profitandloss p
                ON c.id = p.company_id
            WHERE p.net_profit IS NOT NULL
        )
        SELECT
            company_name,
            year,
            net_profit,
            rank_in_year
        FROM ranked_companies
        WHERE rank_in_year <= 3
        ORDER BY year, rank_in_year;
        """
    )

    # ==========================================================
    # Query 26 - Top 5 Companies by Average Net Profit
    # ==========================================================
    run_query(
        connection,
        "Top 5 Companies by Average Net Profit",
        """
        SELECT
            c.company_name,
            ROUND(AVG(p.net_profit), 2) AS average_net_profit,
            COUNT(*) AS total_years
        FROM companies c
        JOIN profitandloss p
            ON c.id = p.company_id
        WHERE p.net_profit IS NOT NULL
        GROUP BY c.company_name
        ORDER BY average_net_profit DESC
        LIMIT 5;
        """
    )

    # ==========================================================
    # Query 27 - Year-over-Year Net Profit Growth (Absolute)
    # ==========================================================
    run_query(
        connection,
        "Year-over-Year Profit Growth (Absolute)",
        """
        SELECT
            c.company_name,
            p.year,
            p.net_profit,
            LAG(p.net_profit) OVER (
                PARTITION BY p.company_id
                ORDER BY p.year
            ) AS previous_year_profit,
            ROUND(
                p.net_profit -
                LAG(p.net_profit) OVER (
                    PARTITION BY p.company_id
                    ORDER BY p.year
                ),
                2
            ) AS profit_growth
        FROM profitandloss p
        JOIN companies c
            ON p.company_id = c.id
        ORDER BY c.company_name, p.year;
        """
    )

    # ==========================================================
    # Query 28 - Latest Financial Dashboard
    # ==========================================================
    run_query(
        connection,
        "Latest Financial Dashboard",
        """
        WITH latest_year AS (
            SELECT
                company_id,
                MAX(year) AS latest_year
            FROM profitandloss
            GROUP BY company_id
        )
        SELECT
            c.company_name,
            p.year,
            p.sales,
            p.net_profit,
            p.eps,
            ROUND((p.net_profit * 100.0) / p.sales, 2) AS profit_margin_pct
        FROM companies c
        JOIN profitandloss p
            ON c.id = p.company_id
        JOIN latest_year l
            ON p.company_id = l.company_id
           AND p.year = l.latest_year
        ORDER BY profit_margin_pct DESC;
        """
    )

    # ==========================================================
    # Query 29 - Sector-wise Company Count
    # ==========================================================
    run_query(
        connection,
        "Sector-wise Company Count",
        """
        SELECT
            broad_sector,
            COUNT(company_id) AS total_companies
        FROM sectors
        GROUP BY broad_sector
        ORDER BY total_companies DESC;
        """
    )

    # ==========================================================
    # Query 30 - Sector-wise Average ROE
    # ==========================================================
    run_query(
        connection,
        "Sector-wise Average ROE",
        """
        SELECT
            s.broad_sector,
            ROUND(AVG(c.roe_percentage), 2) AS avg_roe
        FROM sectors s
        JOIN companies c
            ON s.company_id = c.id
        WHERE c.roe_percentage IS NOT NULL
        GROUP BY s.broad_sector
        ORDER BY avg_roe DESC;
        """
    )

    # ==========================================================
    # Query 31 - Top 5 Sectors by Average Book Value
    # ==========================================================
    run_query(
        connection,
        "Top 5 Sectors by Average Book Value",
        """
        SELECT
            s.broad_sector,
            ROUND(AVG(c.book_value), 2) AS avg_book_value,
            COUNT(c.id) AS total_companies
        FROM sectors s
        JOIN companies c
            ON s.company_id = c.id
        WHERE c.book_value IS NOT NULL
        GROUP BY s.broad_sector
        ORDER BY avg_book_value DESC
        LIMIT 5;
        """
    )

    # ==========================================================
    # Query 32 - Top 10 Companies by Latest Net Profit
    # ==========================================================
    run_query(
        connection,
        "Top 10 Companies by Latest Net Profit",
        """
        WITH latest_profit AS (
            SELECT
                company_id,
                year,
                net_profit,
                ROW_NUMBER() OVER (
                    PARTITION BY company_id
                    ORDER BY year DESC
                ) AS rn
            FROM profitandloss
        )
        SELECT
            c.company_name,
            lp.year,
            lp.net_profit
        FROM latest_profit lp
        JOIN companies c
            ON lp.company_id = c.id
        WHERE lp.rn = 1
        ORDER BY lp.net_profit DESC
        LIMIT 10;
        """
    )

    # ==========================================================
    # Query 33 - Top 10 Companies by Debt-to-Equity Ratio
    # ==========================================================
    run_query(
        connection,
        "Top 10 Companies by Debt-to-Equity Ratio",
        """
        WITH latest_ratio AS (
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
            ROUND(lr.debt_to_equity, 2) AS debt_to_equity
        FROM latest_ratio lr
        JOIN companies c
            ON lr.company_id = c.id
        WHERE lr.rn = 1
          AND lr.debt_to_equity IS NOT NULL
        ORDER BY lr.debt_to_equity DESC
        LIMIT 10;
        """
    )

    # ==========================================================
    # Query 34 - Top 10 Companies by Latest Revenue
    # ==========================================================
    run_query(
        connection,
        "Top 10 Companies by Latest Revenue",
        """
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
            ls.sales
        FROM latest_sales ls
        JOIN companies c
            ON ls.company_id = c.id
        WHERE ls.rn = 1
          AND ls.sales IS NOT NULL
        ORDER BY ls.sales DESC
        LIMIT 10;
        """
    )

    # ==========================================================
    # Query 35 - Year-over-Year Revenue Growth
    # ==========================================================
    run_query(
        connection,
        "Year-over-Year Revenue Growth",
        """
        SELECT
            c.company_name,
            p.year,
            p.sales,
            LAG(p.sales) OVER (
                PARTITION BY p.company_id
                ORDER BY p.year
            ) AS previous_year_sales,
            ROUND(
                (
                    (p.sales - LAG(p.sales) OVER (
                        PARTITION BY p.company_id
                        ORDER BY p.year
                    ))
                    * 100.0
                ) /
                LAG(p.sales) OVER (
                    PARTITION BY p.company_id
                    ORDER BY p.year
                ),
                2
            ) AS yoy_growth_percentage
        FROM profitandloss p
        JOIN companies c
            ON p.company_id = c.id
        ORDER BY
            c.company_name,
            p.year;
        """
    )

    # ==========================================================
    # Query 36 - Year-over-Year Net Profit Growth (Percentage)
    # ==========================================================
    run_query(
        connection,
        "Year-over-Year Net Profit Growth (Percentage)",
        """
        SELECT
            c.company_name,
            p.year,
            p.net_profit,
            LAG(p.net_profit) OVER (
                PARTITION BY p.company_id
                ORDER BY p.year
            ) AS previous_year_profit,
            ROUND(
                (
                    (p.net_profit -
                     LAG(p.net_profit) OVER (
                         PARTITION BY p.company_id
                         ORDER BY p.year
                     )
                    ) * 100.0
                ) /
                LAG(p.net_profit) OVER (
                    PARTITION BY p.company_id
                    ORDER BY p.year
                ),
                2
            ) AS yoy_profit_growth_percentage
        FROM profitandloss p
        JOIN companies c
            ON p.company_id = c.id
        ORDER BY
            c.company_name,
            p.year;
        """
    )

    # ==========================================================
    # Query 37 - Year-over-Year EPS Growth Analysis
    # ==========================================================
    run_query(
        connection,
        "Year-over-Year EPS Growth Analysis",
        """
        SELECT
            c.company_name,
            p.year,
            p.eps,
            LAG(p.eps) OVER (
                PARTITION BY p.company_id
                ORDER BY p.year
            ) AS previous_year_eps,
            ROUND(
                (
                    (p.eps -
                     LAG(p.eps) OVER (
                        PARTITION BY p.company_id
                        ORDER BY p.year
                     )
                    ) * 100.0
                ) /
                LAG(p.eps) OVER (
                    PARTITION BY p.company_id
                    ORDER BY p.year
                ),
                2
            ) AS yoy_eps_growth_percentage
        FROM profitandloss p
        JOIN companies c
            ON p.company_id = c.id
        ORDER BY
            c.company_name,
            p.year;
        """
    )

    # ==========================================================
    # Query 38 - Top 10 Companies by Average ROE (financial_ratios)
    # ==========================================================
    run_query(
        connection,
        "Top 10 Companies by Average ROE (financial_ratios)",
        """
        SELECT
            c.company_name,
            ROUND(AVG(fr.return_on_equity_pct), 2) AS average_roe
        FROM financial_ratios fr
        JOIN companies c
            ON fr.company_id = c.id
        WHERE fr.return_on_equity_pct IS NOT NULL
        GROUP BY
            c.company_name
        ORDER BY
            average_roe DESC
        LIMIT 10;
        """
    )

    # ==========================================================
    # Query 39 - Top 10 Companies by Average ROCE
    # ==========================================================
    run_query(
        connection,
        "Top 10 Companies by Average ROCE",
        """
        SELECT
            c.company_name,
            ROUND(AVG(c.roce_percentage), 2) AS average_roce
        FROM companies c
        WHERE c.roce_percentage IS NOT NULL
        GROUP BY
            c.company_name
        ORDER BY
            average_roce DESC
        LIMIT 10;
        """
    )

    # ==========================================================
    # Query 40 - Companies with Consistent Revenue Growth
    # ==========================================================
    run_query(
        connection,
        "Companies with Consistent Revenue Growth",
        """
        WITH revenue_growth AS (
            SELECT
                company_id,
                year,
                sales,
                LAG(sales) OVER (
                    PARTITION BY company_id
                    ORDER BY year
                ) AS previous_sales
            FROM profitandloss
        )
        SELECT
            c.company_name,
            COUNT(*) AS growth_years
        FROM revenue_growth rg
        JOIN companies c
            ON rg.company_id = c.id
        WHERE previous_sales IS NOT NULL
          AND sales > previous_sales
        GROUP BY c.company_name
        HAVING COUNT(*) >= 3
        ORDER BY growth_years DESC, c.company_name;
        """
    )

    # ==========================================================
    # Query 41 - Top 10 Companies by Average Net Profit (with years)
    # ==========================================================
    run_query(
        connection,
        "Top 10 Companies by Average Net Profit (with years)",
        """
        SELECT
            c.company_name,
            ROUND(AVG(p.net_profit), 2) AS average_net_profit,
            COUNT(p.year) AS total_years
        FROM profitandloss p
        JOIN companies c
            ON p.company_id = c.id
        WHERE p.net_profit IS NOT NULL
        GROUP BY
            c.company_name
        ORDER BY
            average_net_profit DESC
        LIMIT 10;
        """
    )

    # ==========================================================
    # Query 42 - Cash Flow Trend Analysis
    # ==========================================================
    run_query(
        connection,
        "Cash Flow Trend Analysis",
        """
        SELECT
            c.company_name,
            cf.year,
            cf.net_cash_flow,
            LAG(cf.net_cash_flow) OVER (
                PARTITION BY cf.company_id
                ORDER BY cf.year
            ) AS previous_year_cash_flow,
            ROUND(
                (
                    (cf.net_cash_flow -
                     LAG(cf.net_cash_flow) OVER (
                         PARTITION BY cf.company_id
                         ORDER BY cf.year
                     )
                    ) * 100.0
                ) /
                LAG(cf.net_cash_flow) OVER (
                    PARTITION BY cf.company_id
                    ORDER BY cf.year
                ),
                2
            ) AS cash_flow_growth_percentage
        FROM cashflow cf
        JOIN companies c
            ON cf.company_id = c.id
        ORDER BY
            c.company_name,
            cf.year;
        """
    )

    # ==========================================================
    # Query 43 - Companies with Improving Debt-to-Equity Ratio
    # ==========================================================
    run_query(
        connection,
        "Companies with Improving Debt-to-Equity Ratio",
        """
        WITH debt_trend AS (
            SELECT
                company_id,
                year,
                debt_to_equity,
                LAG(debt_to_equity) OVER (
                    PARTITION BY company_id
                    ORDER BY year
                ) AS previous_debt_to_equity
            FROM financial_ratios
        )
        SELECT
            c.company_name,
            dt.year,
            dt.previous_debt_to_equity,
            dt.debt_to_equity,
            ROUND(
                dt.previous_debt_to_equity - dt.debt_to_equity,
                2
            ) AS improvement
        FROM debt_trend dt
        JOIN companies c
            ON dt.company_id = c.id
        WHERE
            dt.previous_debt_to_equity IS NOT NULL
            AND dt.debt_to_equity < dt.previous_debt_to_equity
        ORDER BY
            improvement DESC,
            c.company_name;
        """
    )

    # ==========================================================
    # Query 44 - Revenue vs Net Profit Margin Analysis
    # ==========================================================
    run_query(
        connection,
        "Revenue vs Net Profit Margin Analysis",
        """
        SELECT
            c.company_name,
            p.year,
            p.sales,
            p.net_profit,
            ROUND(
                (p.net_profit * 100.0) / p.sales,
                2
            ) AS net_profit_margin_percentage
        FROM profitandloss p
        JOIN companies c
            ON p.company_id = c.id
        WHERE
            p.sales IS NOT NULL
            AND p.sales > 0
            AND p.net_profit IS NOT NULL
        ORDER BY
            net_profit_margin_percentage DESC;
        """
    )

    # ==========================================================
    # Query 45 - Executive Financial KPI Dashboard
    # ==========================================================
    run_query(
        connection,
        "Executive Financial KPI Dashboard",
        """
        WITH latest_financials AS (
            SELECT
                p.company_id,
                p.year,
                p.sales,
                p.net_profit,
                p.eps,
                ROW_NUMBER() OVER (
                    PARTITION BY p.company_id
                    ORDER BY p.year DESC
                ) AS rn
            FROM profitandloss p
        ),
        latest_ratios AS (
            SELECT
                fr.company_id,
                fr.year,
                fr.debt_to_equity,
                fr.return_on_equity_pct,
                ROW_NUMBER() OVER (
                    PARTITION BY fr.company_id
                    ORDER BY fr.year DESC
                ) AS rn
            FROM financial_ratios fr
        ),
        latest_cashflow AS (
            SELECT
                cf.company_id,
                cf.year,
                cf.net_cash_flow,
                ROW_NUMBER() OVER (
                    PARTITION BY cf.company_id
                    ORDER BY cf.year DESC
                ) AS rn
            FROM cashflow cf
        )
        SELECT
            c.company_name,
            lf.year,
            lf.sales,
            lf.net_profit,
            ROUND(
                (lf.net_profit * 100.0) / lf.sales,
                2
            ) AS net_profit_margin,
            lf.eps,
            lr.return_on_equity_pct,
            lr.debt_to_equity,
            lc.net_cash_flow
        FROM companies c
        LEFT JOIN latest_financials lf
            ON c.id = lf.company_id
            AND lf.rn = 1
        LEFT JOIN latest_ratios lr
            ON c.id = lr.company_id
            AND lr.rn = 1
        LEFT JOIN latest_cashflow lc
            ON c.id = lc.company_id
            AND lc.rn = 1
        ORDER BY
            lf.sales DESC;
        """
    )

    connection.close()
    print("\nAnalytics Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()