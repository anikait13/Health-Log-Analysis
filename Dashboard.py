import streamlit as st
import pandas as pd
import Plotter
import time

st.set_page_config(layout="wide")
from streamlit_extras.switch_page_button import switch_page

st.title("Log Health App Data Analysis")
st.subheader("The data was Analyzed along the following lines 🧑‍💻")

types = ('--None--','Screen Time 📲', 'Calorie Count :phone','Step Count 🏃‍')
selected_page = st.selectbox('Select Analysis Type', types)

if selected_page == 'Screen Time 📲':
    switch_page("screen time analysis")


st.write("Important Notes")
st.markdown("Some Necessary assumptions were made while calculating the analytics")
st.markdown("All graphics are intractable and can be explored further using")
st.markdown("- Item 3")