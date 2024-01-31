import streamlit as st
import time
import Plotter
import Utils
from streamlit_extras.switch_page_button import switch_page


# title of page
st.title("Stand Count Analysis 🧍‍")

# Adding back to Dashboard button
col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
with col6:
    if st.button("Dashboard"):
        switch_page("dashboard")

st.markdown("Analysis of how many times a person stood up from their seat 🪑")

# loading df from csv file
df = Utils.load_data()
types = ('Click here to select date', '23 December 2017', '24 December 2017', 'All')
date = st.selectbox('Select Date for Analysis', types)


hourly_stands = None
cum_stands = None

if date == "--None--":
    st.warning("Please select a valid date.")
elif date == "23 December 2017":
    hourly_stands = Plotter.createStandcountCharts(df, date='2017-12-23')
elif date == "24 December 2017":
    hourly_stands = Plotter.createStandcountCharts(df, date='2017-12-24')
elif date == "All":
    hourly_stands = Plotter.createStandcountCharts(df, date='All')

if hourly_stands:
    with st.spinner(text='Gathering the best analytics'):
        time.sleep(1)
        st.success('Done')
    st.plotly_chart(hourly_stands)
