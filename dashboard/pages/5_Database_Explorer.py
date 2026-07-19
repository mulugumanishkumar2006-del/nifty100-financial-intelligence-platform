import streamlit as st
import pandas as pd

from utils.database import (
    execute_query,
    get_tables
)

st.set_page_config(
    page_title="Database Explorer",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ Database Explorer")

st.markdown(
    "Browse every table inside the NIFTY100 SQLite database."
)

# =====================================================
# Select Table
# =====================================================

tables = get_tables()

selected_table = st.selectbox(
    "Select Table",
    tables
)

# =====================================================
# Row Count
# =====================================================

rows = execute_query(f"""

SELECT COUNT(*) AS total_rows

FROM {selected_table}

""")

st.metric(
    "Rows",
    int(rows.iloc[0]["total_rows"])
)

# =====================================================
# Columns
# =====================================================

columns = execute_query(f"""

PRAGMA table_info({selected_table})

""")

st.subheader("Columns")

st.dataframe(
    columns,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# Data Preview
# =====================================================

limit = st.slider(
    "Rows to Display",
    5,
    100,
    20
)

df = execute_query(f"""

SELECT *

FROM {selected_table}

LIMIT {limit}

""")

st.subheader("Table Preview")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# Search
# =====================================================

search = st.text_input(
    "Search (optional)"
)

if search:

    string_columns = []

    for col in columns["name"]:

        if df[col].dtype == object:

            string_columns.append(col)

    if string_columns:

        condition = " OR ".join(
            [
                f"{c} LIKE '%{search}%'"
                for c in string_columns
            ]
        )

        result = execute_query(f"""

        SELECT *

        FROM {selected_table}

        WHERE {condition}

        LIMIT 100

        """)

        st.subheader("Search Results")

        st.dataframe(
            result,
            use_container_width=True
        )

# =====================================================
# Download
# =====================================================

csv = df.to_csv(index=False)

st.download_button(
    "⬇ Download CSV",
    csv,
    file_name=f"{selected_table}.csv",
    mime="text/csv"
)