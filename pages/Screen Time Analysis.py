import streamlit as st
import time
import Plotter
import Utils
from streamlit_extras.switch_page_button import switch_page


# title of page
st.title("Screen Time Analysis 📲")

# Adding back to Dashboard button
col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
with col6:
    if st.button("Dashboard"):
        switch_page("dashboard")

st.markdown("Analysis of the time person spent with Screen ON or OFF")

# loading df from csv file
df = Utils.load_data()

types = ('Click here to select date', '23 December 2017', '24 December 2017', 'All')
selected_date = st.selectbox('Select Date for Analysis', types)

if selected_date == "--None--":
    st.warning("Please select a valid date.")
else:
    date = None  # Initialize the variable

    if selected_date == "23 December 2017":
        date = '2017-12-23'
    elif selected_date == "24 December 2017":
        date = '2017-12-24'
    elif selected_date == "All":
        date = 'All'

    if date is not None:
        timelineChart, doughnutChart, total_screen_on_time, total_screen_off_time = Plotter.createScreenStatusTimeline(
            df, date)

    if date is not None or date == 'All':
        # Print total time on and off
        st.write(f'Total Screen On Time: {total_screen_on_time:.2f} minutes')
        st.write(f'Total Screen Off Time: {total_screen_off_time:.2f} minutes')

        # spinner for Loading UI
        with st.spinner(text='Gathering the best analytics'):
            time.sleep(1)
            st.success('Done')

        # Display charts
        st.plotly_chart(doughnutChart)
        st.plotly_chart(timelineChart)
