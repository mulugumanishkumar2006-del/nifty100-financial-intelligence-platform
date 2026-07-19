import streamlit as st
import plotly.express as px

from utils.queries import (
    get_company_list,
    get_revenue,
    get_profit,
    get_ratios
)

st.set_page_config(
    page_title="Company Analysis",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Company Financial Analysis")

# -------------------------------------------------------
# Company Selection
# -------------------------------------------------------

companies = get_company_list()

selected_company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company_id = companies.loc[
    companies["company_name"] == selected_company,
    "id"
].iloc[0]

# -------------------------------------------------------
# Revenue Trend
# -------------------------------------------------------

st.subheader("📈 Revenue Trend")

revenue_df = get_revenue(company_id)

if not revenue_df.empty:

    fig = px.line(
        revenue_df,
        x="year",
        y="sales",
        markers=True,
        title="Revenue Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------------------------------
# Net Profit Trend
# -------------------------------------------------------

st.subheader("💰 Net Profit Trend")

profit_df = get_profit(company_id)

if not profit_df.empty:

    fig = px.bar(
        profit_df,
        x="year",
        y="net_profit",
        title="Net Profit"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------------------------------
# Financial Ratios
# -------------------------------------------------------

st.subheader("📊 Financial Ratios")

ratio_df = get_ratios(company_id)

st.dataframe(
    ratio_df,
    use_container_width=True,
    hide_index=True
)

# -------------------------------------------------------
# ROE Trend
# -------------------------------------------------------

if not ratio_df.empty:

    fig = px.line(
        ratio_df,
        x="year",
        y="return_on_equity_pct",
        markers=True,
        title="ROE Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------------------------------
# Debt to Equity
# -------------------------------------------------------

if not ratio_df.empty:

    fig = px.bar(
        ratio_df,
        x="year",
        y="debt_to_equity",
        title="Debt to Equity"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )