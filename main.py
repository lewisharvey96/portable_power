import streamlit as st
import pandas as pd

pd.Series([])
# hides the red bar at the top of streamlit apps
st.markdown(
    """
<style>
	[data-testid="stDecoration"] {
		display: none;
	}

</style>""",
    unsafe_allow_html=True,
)

LOGO_PATH = "zenobe_logo.jpg"
TITLE = "Portable Power"

st.set_page_config(page_title=TITLE, page_icon=LOGO_PATH, layout="wide")

st.title(TITLE)

st.markdown(
    """
    This app showcases an example analysis into a battery and generator hybrid system. The goal is to show:
    - How to size a generator
    - How we can model a hybrid system
    - How we could optimize a hybrid system's design
    """
)
