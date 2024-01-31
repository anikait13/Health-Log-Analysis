import streamlit as st
import pandas as pd
import time
import Utils
import Plotter
from streamlit_extras.switch_page_button import switch_page

st.title("Calories Analysis 🏋🏻")

# Adding back to Dashboard button
col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
with col6:
    if st.button("Dashboard"):
        switch_page("dashboard")

# loading df from csv file
df = Utils.load_data()
types = ('--None--', '23 December 2017', '24 December 2017', 'All')
date = st.selectbox('Select Date for Analysis', types)

hourly_calories = None
cum_calories = None

if date == "--None--":
    st.warning("Please select a valid date.")
elif date == "23 December 2017":
    hourly_calories = Plotter.createCalorieCountCharts(df, date='2017-12-23')
    cum_calories, max_calories = Plotter.createCaloriesCumulativeChart(df, date='2017-12-23')
elif date == "24 December 2017":
    hourly_calories = Plotter.createCalorieCountCharts(df, date='2017-12-24')
    cum_calories, max_calories = Plotter.createCaloriesCumulativeChart(df, date='2017-12-24')

elif date == "All":
    hourly_calories = Plotter.createCalorieCountCharts(df, date='All')
    cum_calories, max_calories, max_calories_day = Plotter.createCaloriesCumulativeAllDaysChart(df)

if hourly_calories:
    if date != 'All':
        st.write("Total Number of Calories on ", date, "was ", max_calories, " calories.")
    else:
        st.write("Maximum number of Calories of ", max_calories, "was burnt on ", max_calories_day, " .")

    with st.spinner(text='Gathering the best analytics'):
        time.sleep(3)
        st.success('Done')

    st.plotly_chart(hourly_calories)
    st.plotly_chart(cum_calories)
