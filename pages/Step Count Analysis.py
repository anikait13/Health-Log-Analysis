import streamlit as st
import pandas as pd
import Utils
import Plotter

st.title("Step Count Analysis 🏃‍")

#loading df from csv file
df = Utils.load_data()
types = ('--None--', '23 December 2017', '24 December 2017', 'All')
date = st.selectbox('Select Date for Analysis', types)

hourly_steps = None  # Initialize the variable

if date == "--None--":
    pass
elif date == "23 December 2017":
    hourly_steps = Plotter.createStepcountCharts(df, date='2017-12-23')
elif date == "24 December 2017":
    hourly_steps = Plotter.createStepcountCharts(df, date='2017-12-24')
elif date == "All":
    hourly_steps = Plotter.createStepcountCharts(df, date='all')

if hourly_steps:
    st.plotly_chart(hourly_steps)




