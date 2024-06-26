import streamlit as st
import pandas as pd
import time
import Utils
import Plotter
from streamlit_extras.switch_page_button import switch_page


st.title("Step Count Analysis 🏃‍")

col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
with col6:
    if st.button("Dashboard"):
        switch_page("dashboard")

st.markdown("Analysis of how many steps a person walked 🚶🏻‍")


# loading df from csv file
df = Utils.load_data()
types = ('Click here to select date', '23 December 2017', '24 December 2017', 'All')
date = st.selectbox('Select Date for Analysis', types)


hourly_steps = None
cum_steps = None

if date == "--None--":
    st.warning("Please select a valid date.")
elif date == "23 December 2017":
    hourly_steps = Plotter.createStepcountCharts(df, date='2017-12-23')
    cum_steps, max_steps = Plotter.createStepcountCumCharts(df, date='2017-12-23')
elif date == "24 December 2017":
    hourly_steps = Plotter.createStepcountCharts(df, date='2017-12-24')
    cum_steps, max_steps = Plotter.createStepcountCumCharts(df, date='2017-12-24')

elif date == "All":
    hourly_steps = Plotter.createStepcountCharts(df, date='All')

if hourly_steps:
    with st.spinner(text='Gathering the best analytics'):
        time.sleep(1)
        st.success('Done')
    if date != 'All':
        st.write("Total Number of Steps on ", date, "was ", max_steps, " steps.")
    st.plotly_chart(hourly_steps)
    if cum_steps:
        st.plotly_chart(cum_steps)
    else:
        st.warning("For Cumulative step count select a specific date")
