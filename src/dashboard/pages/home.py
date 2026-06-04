import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

df = pd.read_csv(
    "https://raw.githubusercontent.com/aswathygopan235/xai_drilling_porfolio_17/refs/heads/main/src/data/XAI_Drilling_Dataset.csv")


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

#     # st.write("### Pie Chart")
#     # spec = {
#     #     "type": "pie",
#     #     "data": {
#     #         "labels": labels,
#     #         "datasets": [{"data": sizes}],
#     #     },
#     # }
#     # chartjs_chart(spec)


def table():
    st.title("Data")
    st.dataframe(df, key="table_data")


def main():
    table()
    with st.container():
        st.title("Failure percent")
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            plot_pie("Main Failure")
        with col2:
            plot_pie("BEF")

        col3, col4, col6 = st.columns([1, 1, 3])
        with col3:
            plot_pie("CCF")
        with col4:
            plot_pie("FWF")


if __name__ == "__main__":
    main()
