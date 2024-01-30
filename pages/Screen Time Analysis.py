import streamlit as st
import pandas as pd
import time
import Plotter

st.title("User's Screen Time Analysis")

file_path = 'Dataset/HealthApp_2k.log_structured.csv'
df = pd.read_csv(file_path)
df['Time'] = pd.to_datetime(df['Time'], format='%Y%m%d-%H:%M:%S:%f')
df['Date'] = df['Time'].dt.date
df['Hour'] = pd.to_datetime(df['Time'], format='%Y%m%d-%H:%M:%S:%f').dt.hour


timelineChart, doughnutChart, total_screen_on_time, total_screen_off_time = Plotter.createScreenStatusTimeline(df)
# Print total time on and off
st.write(f'Total Screen On Time: {total_screen_on_time:.2f} minutes')
st.write(f'Total Screen Off Time: {total_screen_off_time:.2f} minutes')
with st.spinner(text='Getting the best analytics'):
    time.sleep(3)
    st.success('Done')
# Display charts
st.plotly_chart(doughnutChart)
st.plotly_chart(timelineChart)






