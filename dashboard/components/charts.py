import plotly.express as px
import streamlit as st

def bar_chart(df, x, y, title):

    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def line_chart(df, x, y, title):

    fig = px.line(
        df,
        x=x,
        y=y,
        markers=True,
        title=title
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
import plotly.express as px
import streamlit as st


def bar_chart(df, x, y, title):

    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def line_chart(df, x, y, title):

    fig = px.line(
        df,
        x=x,
        y=y,
        markers=True,
        title=title
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )