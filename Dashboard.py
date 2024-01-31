import streamlit as st
import pandas as pd
import Plotter
import time

st.set_page_config(layout="wide")
from streamlit_extras.switch_page_button import switch_page

st.title("Log Health App Data Analysis")
st.subheader("The data was Analyzed along the following lines 🧑‍💻")

types = ('--None--', 'Screen Time 📲', 'Calories Burnt 🏋🏻', 'Step Count 🏃')
selected_page = st.selectbox('Select Analysis Type', types)

if selected_page == 'Screen Time 📲':
    switch_page("screen time analysis")
if selected_page == 'Step Count 🏃':
    switch_page("step count analysis")
if selected_page == 'Calories Burnt 🏋🏻':
    switch_page("calories analysis")

st.write()
st.write()

st.subheader("Important Notes 📌")
st.markdown("- Certain necessary assumptions were considered during the calculation of analytics.")
st.markdown("- All graphs and charts are interactive, allowing for further exploration.")
st.markdown("- Source Code is seen by clicking the Github logo on the top-right ↗️. ")

st.("The repository was plagarized by others as it was set to public for deployment.")
st.write("Repository is set to private now. Source code will be sent as a .zip file")
st.image("images/Clones.png")

