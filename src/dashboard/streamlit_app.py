import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from dotenv import load_dotenv
import os

load_dotenv()

DOCS_URL = os.getenv('DOCS_URL')
st.set_page_config(layout="wide")

st.html("""
    <style>
        .stAppHeader {
            background-color: #9c1d50; /* Change to your preferred hex code */
        }
        .st-key-footer_content{
        position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #9c1d50;
            color: white;
            text-align: center;
            height:5rem
    </style>
""")


def navigation():
    # home = st.Page("./pages/home.py", title="Home", default=True)
    # app = st.Page("./pages/app.py", title="App")

    # with st.sidebar:
    #     st.write("## Navigation")
    #     st.page_link(home)
    #     st.page_link(app)

    #     st.divider()  # Adds a visual separator

    #     st.page_link(
    #         "https://github.com/aswathygopan235/xai_drilling_porfolio_17", label="Google", icon="🌎")

    pages = [
        st.Page("pages/home.py", title="Home", default=True),
        st.Page("pages/app.py", title="App"),
        # st.Page("pages/page3.py", title="Page 3"),

    ]

    pg = st.navigation(pages, position="top")
    pg.run()


def footer():
    with st.container(key="footer_content", vertical_alignment="center", horizontal_alignment="center"):
        col1, col2, col3, col4, col5 = st.columns(
            [3, 1, 1, 4, 3], vertical_alignment="center")
        with col2:
            st.page_link(
                "https://github.com/aswathygopan235/xai_drilling_porfolio_17", label="Github")
        with col3:
            st.page_link(
                DOCS_URL+"/docs", label="Docs")
        with col4:
            st.caption("Aswathy Gopan Machine Learning Project XAI Drilling")


def main():
    # table()
    navigation()
    # col1, col2 = st.columns(2)
    # with col1:
    #     plot_pie("Main Failure")
    # with col2:
    #     plot_pie("BEF")

    # col3, col4 = st.columns(2)
    # with col3:
    #     plot_pie("CCF")
    # with col4:
    #     plot_pie("FWF")
    with st._bottom:
        footer()


if __name__ == "__main__":
    main()
