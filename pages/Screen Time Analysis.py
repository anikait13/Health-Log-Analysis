import streamlit as st
import pandas as pd
import time
import Plotter
import Utils

# title of page
st.title("Screen Time Analysis 📲")

#loading df from csv file
df = Utils.load_data()

#importing charts and on/off times
timelineChart, doughnutChart, total_screen_on_time, total_screen_off_time = Plotter.createScreenStatusTimeline(df)

# Print total time on and off
st.write(f'Total Screen On Time: {total_screen_on_time:.2f} minutes')
st.write(f'Total Screen Off Time: {total_screen_off_time:.2f} minutes')

# spinner for Loading UI
with st.spinner(text='Gathering the best analytics'):
    time.sleep(3)
    st.success('Done')

# Display charts
st.plotly_chart(doughnutChart)
st.plotly_chart(timelineChart)






