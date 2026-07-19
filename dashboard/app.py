import sys
from pathlib import Path

import streamlit as st
import plotly.express as px

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dashboard.utils.database import (
        get_connection,
        get_tables,
        execute_query,
    )
except ImportError:
    from utils.database import (
        get_connection,
        get_tables,
        execute_query,
    )

st.set_page_config(
    page_title="NIFTY100 Financial Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    from dashboard.components.sidebar import render_sidebar
    from dashboard.components.cards import metric_card
    from dashboard.components.charts import bar_chart, line_chart
    from dashboard.utils.queries import (
        get_total_companies,
        get_total_ratios,
        get_total_years,
        get_company_list,
        get_sector_distribution,
        get_company_preview,
        get_top_revenue,
        get_revenue,
        get_profit,
        get_ratios,
        get_latest_snapshot,
    )
except Exception:
    from components.sidebar import render_sidebar
    from components.cards import metric_card
    from components.charts import bar_chart, line_chart
    from utils.queries import (
        get_total_companies,
        get_total_ratios,
        get_total_years,
        get_company_list,
        get_sector_distribution,
        get_company_preview,
        get_top_revenue,
        get_revenue,
        get_profit,
        get_ratios,
        get_latest_snapshot,
    )

render_sidebar()

# ----------------------------------------------------
# Title
# ----------------------------------------------------

st.title("📈 NIFTY100 Financial Intelligence Dashboard")

st.markdown("""
Enterprise Financial Analytics Platform

Built using:

- SQLite
- Streamlit
- Pandas
- Plotly
""")

st.divider()

# ----------------------------------------------------
# Database Status
# ----------------------------------------------------

try:

    connection = get_connection()

    st.success("✅ Database Connected Successfully")

except Exception as e:

    st.error(f"❌ Database Connection Failed\n\n{e}")

    st.stop()

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

companies = get_total_companies().iloc[0, 0]

tables = len(get_tables())

ratios = get_total_ratios().iloc[0, 0]

years = get_total_years().iloc[0, 0]

with col1:
    metric_card("Companies", companies)

with col2:
    metric_card("Database Tables", tables)

with col3:
    metric_card("Financial Ratios", ratios)

with col4:
    metric_card("Financial Years", years)

st.divider()

# ----------------------------------------------------
# Available Tables
# ----------------------------------------------------

# ----------------------------------------------------
# Companies by Sector (Plotly)
# ----------------------------------------------------

st.subheader("📊 Companies by Sector")

sector_df = get_sector_distribution()

bar_chart(
    sector_df,
    "broad_sector",
    "total_companies",
    "Companies in Each Sector"
)


st.subheader("Database Tables")

st.divider()

st.subheader("🏆 Top 10 Companies by Revenue")

top_companies = get_top_revenue()

st.dataframe(
    top_companies,
    use_container_width=True,
    hide_index=True
)

bar_chart(
    top_companies,
    "company_name",
    "revenue",
    "Top 10 Companies by Revenue"
)

# ----------------------------------------------------
# Company Selector + Trends + Ratios + Snapshot
# ----------------------------------------------------

st.divider()

st.subheader("🏢 Company Analysis Preview")

company_list = get_company_list()

if company_list.empty:
    st.info("No companies available in the database.")
else:

    selected_company = st.selectbox(
        "Select a Company",
        company_list["company_name"]
    )

    company_id = company_list.loc[
        company_list["company_name"] == selected_company,
        "id"
    ].iloc[0]

    # Revenue Trend
    revenue_df = get_revenue(company_id)

    st.subheader("📈 Revenue Trend")

    if revenue_df.empty:
        st.info("No revenue data for the selected company.")
    else:
        line_chart(
            revenue_df,
            "year",
            "sales",
            f"{selected_company} Revenue"
        )

    # Net Profit Trend
    profit_df = get_profit(company_id)

    st.subheader("💰 Net Profit Trend")

    if profit_df.empty:
        st.info("No net profit data for the selected company.")
    else:
        line_chart(
            profit_df,
            "year",
            "net_profit",
            f"{selected_company} Net Profit"
        )

    # Financial Ratios
    ratio_df = get_ratios(company_id)

    st.subheader("📊 Financial Ratios")

    if ratio_df.empty:
        st.info("No financial ratios available for the selected company.")
    else:
        st.dataframe(
            ratio_df,
            use_container_width=True,
            hide_index=True
        )

    # Latest Financial Snapshot
    latest = get_latest_snapshot(company_id)

    if not latest.empty:

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            metric_card("Revenue", f"{latest.iloc[0]['sales']:,.2f}")

        with c2:
            metric_card("Net Profit", f"{latest.iloc[0]['net_profit']:,.2f}")

        with c3:
            metric_card("ROE %", f"{latest.iloc[0]['return_on_equity_pct']:.2f}")

        with c4:
            metric_card("Debt/Equity", f"{latest.iloc[0]['debt_to_equity']:.2f}")

table_df = get_tables()

st.dataframe(
    table_df,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# Sample Companies
# ----------------------------------------------------

st.subheader("Companies Table Structure")

columns = execute_query("""

PRAGMA table_info(companies);

""")

st.dataframe(columns, use_container_width=True)

st.divider()

st.info(
    "Use the left sidebar to explore different dashboard modules."
)

# ----------------------------------------------------
# Companies Preview
# ----------------------------------------------------

st.subheader("🏢 Companies Preview")

company_df = get_company_preview()

st.dataframe(company_df, use_container_width=True)

st.divider()