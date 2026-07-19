import streamlit as st
import plotly.express as px
from utils.database import execute_query

st.set_page_config(
    page_title="Financial Ratios",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Financial Ratios Dashboard")

# ==========================================================
# Company Selector
# ==========================================================

companies = execute_query("""
SELECT
    id,
    company_name
FROM companies
ORDER BY company_name
""")

selected_company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company_id = companies.loc[
    companies["company_name"] == selected_company,
    "id"
].iloc[0]

# ==========================================================
# Load Ratios
# ==========================================================

ratio_df = execute_query(f"""
SELECT
    year,
    return_on_equity_pct,
    net_profit_margin_pct,
    operating_profit_margin_pct,
    debt_to_equity,
    interest_coverage,
    asset_turnover
FROM financial_ratios
WHERE company_id='{company_id}'
ORDER BY year
""")

if ratio_df.empty:
    st.warning("No ratio data available.")
    st.stop()

# ==========================================================
# Latest KPIs
# ==========================================================

latest = ratio_df.iloc[-1]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("ROE (%)", round(latest["return_on_equity_pct"], 2))

with c2:
    st.metric("Net Margin (%)", round(latest["net_profit_margin_pct"], 2))

with c3:
    st.metric("Debt / Equity", round(latest["debt_to_equity"], 2))

with c4:
    st.metric("Asset Turnover", round(latest["asset_turnover"], 2))

st.divider()

# ==========================================================
# ROE Trend
# ==========================================================

st.subheader("📈 Return on Equity")

fig = px.line(
    ratio_df,
    x="year",
    y="return_on_equity_pct",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# Net Profit Margin
# ==========================================================

st.subheader("💰 Net Profit Margin")

fig = px.bar(
    ratio_df,
    x="year",
    y="net_profit_margin_pct"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# Operating Profit Margin
# ==========================================================

st.subheader("🏭 Operating Profit Margin")

fig = px.line(
    ratio_df,
    x="year",
    y="operating_profit_margin_pct",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# Debt to Equity
# ==========================================================

st.subheader("🏦 Debt to Equity")

fig = px.bar(
    ratio_df,
    x="year",
    y="debt_to_equity"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# Interest Coverage
# ==========================================================

st.subheader("💳 Interest Coverage")

fig = px.line(
    ratio_df,
    x="year",
    y="interest_coverage",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# Asset Turnover
# ==========================================================

st.subheader("🏢 Asset Turnover")

fig = px.bar(
    ratio_df,
    x="year",
    y="asset_turnover"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# Complete Table
# ==========================================================

st.subheader("📋 Financial Ratios Table")

st.dataframe(
    ratio_df,
    use_container_width=True,
    hide_index=True
)