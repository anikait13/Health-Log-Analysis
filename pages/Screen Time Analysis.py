import streamlit as st
import pandas as pd
import time
import Plotter

st.title("Users Screen time Analysis")

file_path = 'Dataset/HealthApp_2k.log_structured.csv'
df = pd.read_csv(file_path)
df['Time'] = pd.to_datetime(df['Time'], format='%Y%m%d-%H:%M:%S:%f')
df['Date'] = df['Time'].dt.date
df['Hour'] = pd.to_datetime(df['Time'], format='%Y%m%d-%H:%M:%S:%f').dt.hour

with st.spinner(text='Getting the best analytics'):
    time.sleep(3)
    st.success('Done')

timelineChart, doughnutChart = Plotter.createScreenStatusTimeline(df)

# Display charts
st.plotly_chart(doughnutChart)
st.plotly_chart(timelineChart)






