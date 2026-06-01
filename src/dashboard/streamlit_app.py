from streamlit_extras.chartjs_chart import *
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")

df = pd.read_csv("src/data/XAI_Drilling_Dataset.csv")


def plot_pie(feature):
    """Pie chart example."""
    res = df[feature].value_counts()
    labels = res.keys()
    sizes = res.values

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.axis('equal')
    ax1.set_title(feature)
    ax1.legend()

    st.pyplot(fig1)

    # st.write("### Pie Chart")
    # spec = {
    #     "type": "pie",
    #     "data": {
    #         "labels": labels,
    #         "datasets": [{"data": sizes}],
    #     },
    # }
    # chartjs_chart(spec)


def table():

    st.dataframe(df, key="table_data")


def navigation():

    pages = [
        st.Page("pages/home.py", title="Home", default=True),
        st.Page("pages/page2.py", title="Page 2"),
        st.Page("pages/page3.py", title="Page 3")
    ]

    pg = st.navigation(pages, position="top")
    pg.run()


def footer():
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
