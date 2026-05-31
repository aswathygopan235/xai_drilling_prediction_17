import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_extras.chartjs_chart import *

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


def main():
    table()
    col1, col2 = st.columns(2)
    with col1:
        plot_pie("Main Failure")
    with col2:
        plot_pie("BEF")

    col3, col4 = st.columns(2)
    with col3:
        plot_pie("CCF")
    with col4:
        plot_pie("FWF")


if __name__ == "__main__":
    main()
