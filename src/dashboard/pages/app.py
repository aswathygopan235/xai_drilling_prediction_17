import streamlit as st
import os
from dotenv import load_dotenv
import requests
import time


st.set_page_config(layout="wide")
load_dotenv()
PREDICT_URL = os.getenv('PREDICT_URL')
DOCS_URL = os.getenv('DOCS_URL')


@st.dialog("Result", dismissible=False, width="medium")
def result_modal(res, inp):
    """modal to show result"""
    inp_col, out_col = st.columns([1, 2])

    input_mk = f'''
        ### Input
        | label          | value |
        | -------------- | ----- |
        |cutting_speed|{inp['cutting_speed_vc']}|
        |spindle_speed|{inp['spindle_speed_n']}|
        |feed|{inp['feed_f']}|
        |feed rate|{inp['feed_rate_vf']}|
        |power|{inp['power_pc']}|
        |cooling|{inp['cooling']}|
        |material|{inp['material']}|
        |drill bit|{inp['drill_bit_type']}|
        |process time|{inp['process_time']}|



        '''
    out = res["result"][0]
    output_mk = f'''
        ### Output
        | label          | value |
        | -------------- | ----- |
        | main failure | {out['main_failure']}    |
        | buildup edge failure | {out['buildup_edge_failure']}     |
        | compression chip failure | {out['compression_chip_failure']}     |
        | flank wear failure| {out['flank_wear_failure']}     |
        | wrong rill bit_failure*| {out['wrong_drill_bit_failure']}     |'''
    with inp_col:
        st.markdown(input_mk)
    with out_col:
        st.markdown(output_mk)

    if (st.button("close")):
        st.rerun()


def construct_error_message(result):
    """create colour coded error message"""
    error_log = result["errors"]
    msg = ""
    for error in error_log:
        log = f'\n:gray[{error["field"]}]: :red[{error["msg"]}]'
        msg = msg+log
    return msg


def initial_wake():

    if ("loaded" not in st.session_state):
        st.session_state["loaded"] = False

    if (st.session_state["loaded"] is False):
        wake_api()
        st.session_state["loaded"] = True


def wake_api():
    """API called to wake server"""

    url = PREDICT_URL
    with st.spinner("loading"):
        requests.post(url, timeout=60).json()
        time.sleep(5)


def call_api():
    """API called to predict price"""
    url = PREDICT_URL+"/predict"
    inp = {
        "cutting_speed_vc": st.session_state["cutting_speed"],
        "spindle_speed_n": st.session_state["spindle_speed"],
        "feed_f": st.session_state["feed"],
        "feed_rate_vf": st.session_state["feed_rate"],
        "power_pc": st.session_state["power"],
        "cooling": st.session_state["cooling_rate"],
        "material": st.session_state["material"],
        "drill_bit_type": st.session_state["drill_bit_type"],
        "process_time": st.session_state["process_time"],
    }
    with st.spinner("Calculating"):
        data = requests.post(url, json=inp, timeout=60).json()
        time.sleep(5)

    if (result_modal not in st.session_state):
        result_modal(data, inp)


def form_area():

    col1, col2 = st.columns(2)

    with st.form("drilling_instance_form", enter_to_submit=False, border=False, clear_on_submit=True):
        with col1:

            st.number_input("Pick the cutting speed (m/min)?",
                            min_value=16.0, max_value=35.0, key="cutting_speed", step=.01)
            st.number_input("Pick the spindle speed (1/min)?",
                            min_value=400, max_value=830, key="spindle_speed")
            st.number_input("Pick the feed (mm/rev)?",
                            min_value=0.100, max_value=0.325, key="feed", step=.001, format="%0.3f")

            st.number_input("Pick the feed rate (mm/min)?",
                            min_value=60, max_value=265, key="feed_rate")

            st.number_input("Pick the power (kW)?",
                            min_value=45.00, max_value=310.00, key="power", step=.01)
        with col2:
            st.selectbox(
                "Select cooling rate (%)",
                (0, 25, 50, 75, 100),
                key="cooling_rate",
                placeholder="Select a rate"
            )
            st.selectbox(
                "Select material",
                ("N", "P", "K"),
                key="material",
                placeholder="Select a material"
            )
            st.selectbox(
                "Select drill bit type",
                ("W", "N", "H"),
                key="drill_bit_type",
                placeholder="Select drill bit type"
            )

            st.number_input("Pick the process time (sec)?",
                            min_value=15.0, max_value=40.0, key="process_time", step=.01)

        st.form_submit_button(
            "Submit", key="submit_drill_form", on_click=call_api)


def main():
    initial_wake()

    with st.container(vertical_alignment="center"):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            with st.container(vertical_alignment="center"):
                col_title, empty_col,  github_col, docs_col =
                st.columns([1, 2, 1, 1], vertical_alignment="center")
                with col_title:
                    st.title("App", text_alignment="left")
                with github_col:
                    st.link_button(
                        url="https://github.com/aswathygopan235/xai_drilling_porfolio_17", label="Github", type="primary")
                with docs_col:
                    st.link_button(url=DOCS_URL+"/docs",
                                   label="Docs", type="primary")

            form_area()


if __name__ == "__main__":
    main()
