import streamlit as st
import pandas as pd
import Plotter
import time

st.set_page_config(layout="wide")
from streamlit_extras.switch_page_button import switch_page

st.title("Log Health App Data Analysis")
st.subheader("The data was Analyzed along the following lines 🧑‍💻")

types = ('--None--','Screen Time 📲', 'Calorie Count :phone')
selected_page = st.selectbox('Select Analysis Type', types)

if selected_page == 'Screen Time 📲':
    switch_page("screen time analysis")
