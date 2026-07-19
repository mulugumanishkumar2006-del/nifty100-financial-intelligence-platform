import time
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.database import execute_query

st.set_page_config(
    page_title="SQL Analytics",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ SQL Analytics Dashboard")

st.markdown(
    "Run analytical SQL queries against the NIFTY100 database."
)

# ==========================================================
# Example Queries
# ==========================================================

QUERIES = {

    "Total Companies": """
        SELECT COUNT(*) AS total_companies
        FROM companies;
    """,

    "Companies by Sector": """
        SELECT
            broad_sector,
            COUNT(*) AS total
        FROM sectors
        GROUP BY broad_sector
        ORDER BY total DESC;
    """,

    "Top 10 Revenue Companies": """
        SELECT
            c.company_name,
            MAX(p.sales) AS revenue
        FROM companies c
        JOIN profitandloss p
        ON c.id=p.company_id
        GROUP BY c.company_name
        ORDER BY revenue DESC
        LIMIT 10;
    """,

    "Average ROE by Sector": """
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
        ORDER BY avg_roe DESC;
    """,

    "Top Asset Turnover": """
        SELECT
            company_id,
            asset_turnover
        FROM financial_ratios
        ORDER BY asset_turnover DESC
        LIMIT 20;
    """
}

# ==========================================================
# Query Selector
# ==========================================================

selected = st.selectbox(
    "Select SQL Query",
    list(QUERIES.keys())
)

query = QUERIES[selected]

st.code(query, language="sql")

# ==========================================================
# Execute Button
# ==========================================================

if st.button("▶ Execute Query"):

    start = time.time()

    df = execute_query(query)

    end = time.time()

    st.success(
        f"Completed in {round(end-start,3)} seconds"
    )

    st.metric(
        "Rows Returned",
        len(df)
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    # ------------------------------------------------------

    numeric = df.select_dtypes(include="number").columns

    if len(numeric) > 0:

        x = df.columns[0]
        y = numeric[0]

        fig = px.bar(
            df,
            x=x,
            y=y,
            title=selected
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    csv = df.to_csv(index=False)

    st.download_button(
        "⬇ Download CSV",
        csv,
        file_name="analytics.csv",
        mime="text/csv"
    )