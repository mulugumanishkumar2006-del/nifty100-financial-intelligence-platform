import streamlit as st
import plotly.express as px

from utils.database import execute_query

st.set_page_config(
    page_title="Sector Analysis",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Sector Analysis Dashboard")

# =====================================================
# Sector Summary
# =====================================================

sector_df = execute_query("""

SELECT

    broad_sector,

    COUNT(*) AS total_companies

FROM sectors

GROUP BY broad_sector

ORDER BY total_companies DESC

""")

st.subheader("Sector Distribution")

st.dataframe(
    sector_df,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# Sector Bar Chart
# =====================================================

fig = px.bar(
    sector_df,
    x="broad_sector",
    y="total_companies",
    text="total_companies",
    title="Companies by Sector"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# Sector Pie Chart
# =====================================================

fig = px.pie(
    sector_df,
    names="broad_sector",
    values="total_companies",
    title="Sector Composition"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# Revenue by Sector
# =====================================================

revenue_df = execute_query("""

SELECT

    s.broad_sector,

    SUM(p.sales) AS total_revenue

FROM profitandloss p

JOIN sectors s

ON p.company_id=s.company_id

GROUP BY s.broad_sector

ORDER BY total_revenue DESC

""")

st.subheader("Revenue by Sector")

fig = px.bar(
    revenue_df,
    x="broad_sector",
    y="total_revenue",
    text_auto=".2s"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# Net Profit by Sector
# =====================================================

profit_df = execute_query("""

SELECT

    s.broad_sector,

    SUM(p.net_profit) AS total_profit

FROM profitandloss p

JOIN sectors s

ON p.company_id=s.company_id

GROUP BY s.broad_sector

ORDER BY total_profit DESC

""")

st.subheader("Net Profit by Sector")

fig = px.bar(
    profit_df,
    x="broad_sector",
    y="total_profit",
    text_auto=".2s"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# Average ROE
# =====================================================

roe_df = execute_query("""

SELECT

    s.broad_sector,

    ROUND(
        AVG(f.return_on_equity_pct),
        2
    ) AS avg_roe

FROM financial_ratios f

JOIN sectors s

ON f.company_id=s.company_id

GROUP BY s.broad_sector

ORDER BY avg_roe DESC

""")

st.subheader("Average ROE by Sector")

fig = px.bar(
    roe_df,
    x="broad_sector",
    y="avg_roe",
    text="avg_roe"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# Sector Details
# =====================================================

selected_sector = st.selectbox(
    "Select Sector",
    sector_df["broad_sector"]
)

companies = execute_query(f"""

SELECT

    c.company_name

FROM companies c

JOIN sectors s

ON c.id=s.company_id

WHERE s.broad_sector='{selected_sector}'

ORDER BY company_name

""")

st.subheader(f"Companies in {selected_sector}")

st.dataframe(
    companies,
    use_container_width=True,
    hide_index=True
)