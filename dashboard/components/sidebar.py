import streamlit as st

def render_sidebar():
    """
    Render the dashboard sidebar.
    """

    with st.sidebar:

        st.title("📊 NIFTY100")

        st.markdown("---")

        st.success("🟢 Database Connected")

        st.markdown("### Navigation")

        st.page_link("app.py", label="🏠 Home")

        st.page_link(
            "pages/1_Company_Analysis.py",
            label="🏢 Company Analysis"
        )

        st.page_link(
            "pages/2_Sector_Analysis.py",
            label="🏭 Sector Analysis"
        )

        st.page_link(
            "pages/3_Financial_Ratios.py",
            label="📈 Financial Ratios"
        )

        st.page_link(
            "pages/4_SQL_Analytics.py",
            label="🗃 SQL Analytics"
        )

        st.page_link(
            "pages/5_Database_Explorer.py",
            label="🗄 Database Explorer"
        )

        st.markdown("---")

        st.caption("Version 1.0")
import streamlit as st


def render_sidebar():
    """
    Render the dashboard sidebar.
    """

    with st.sidebar:

        st.title("📊 NIFTY100")

        st.markdown("---")

        st.success("🟢 Database Connected")

        st.markdown("### Navigation")

        st.page_link("app.py", label="🏠 Home")

        st.page_link(
            "pages/1_Company_Analysis.py",
            label="🏢 Company Analysis"
        )

        st.page_link(
            "pages/2_Sector_Analysis.py",
            label="🏭 Sector Analysis"
        )

        st.page_link(
            "pages/3_Financial_Ratios.py",
            label="📈 Financial Ratios"
        )

        st.page_link(
            "pages/4_SQL_Analytics.py",
            label="🗃 SQL Analytics"
        )

        st.page_link(
            "pages/5_Database_Explorer.py",
            label="🗄 Database Explorer"
        )

        st.markdown("---")

        st.caption("Version 1.0")