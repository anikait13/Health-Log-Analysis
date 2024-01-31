import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import Utils


def createScreenStatusTimeline(df, date):
    if date == 'All':
        screenData = Utils.generateScreenStatusDataAll(df)
    else:
        screenData = Utils.generateScreenStatusData(df, date)

    color_map = {'Screen On': 'blue', 'Screen Off': 'red'}
    screenData['color'] = screenData['ScreenStatusCat'].map(color_map)

    timelineFig = px.timeline(screenData,
                              x_start='Time',
                              x_end='timeShifted',
                              y='yVal',
                              color='ScreenStatusCat',
                              color_discrete_map=color_map)

    # Add a doughnut chart for screen on and off times
    doughnutFig = go.Figure()

    screen_status_counts = screenData['ScreenStatusCat'].value_counts()
    labels = screen_status_counts.index
    values = screen_status_counts.values

    doughnutFig.add_trace(go.Pie(labels=labels, values=values, hole=0.5, marker=dict(colors=['blue', 'red'])))

    # Update layout for doughnut chart
    doughnutFig.update_layout(
        title_text='Screen On/Off Distribution',
        title_font_size=16,
        showlegend=True,
    )

    # Update layout for timeline chart
    timelineFig.update_layout(
        width=1000,
        title_text='Event Timeline of Screen Status',
        title_font_size=16,
        title_xanchor='left',
        xaxis=dict(showgrid=False, linecolor='black', linewidth=2, mirror=True),
        yaxis=dict(showgrid=False, linecolor='black', linewidth=2, mirror=True, title_text=''),
        font=dict(family="Arial, sans-serif", size=12, color="black"),
    )

    # Calculate total time in 'Screen On' and 'Screen Off' states
    total_screen_on_time = screenData.loc[screenData['ScreenStatusCat'] == 'Screen On', 'duration'].sum()
    total_screen_off_time = screenData.loc[screenData['ScreenStatusCat'] == 'Screen Off', 'duration'].sum()

    return timelineFig, doughnutFig, total_screen_on_time, total_screen_off_time


def createStepcountCharts(df, date):
    if 'df' in locals() and not df.empty:
        step_events = df[df['EventId'] == 'E22'].copy()

        step_events['StepCount'] = step_events['Content'].apply(Utils.extract_step_count)
        step_events['Date'] = pd.to_datetime(step_events['Time']).dt.date
        step_events['Hour12'] = pd.to_datetime(step_events['Time']).dt.strftime('%I %p')
        step_events['Hour'] = pd.to_datetime(step_events['Time']).dt.hour

        # Removing Bad entries
        step_events = step_events.drop(
            step_events[(step_events['LineId'] == 1791) | (step_events['LineId'] == 1796)].index)

        if date.lower() != 'all':
            # Select a specific date for analysis
            selected_date = date
            # Calculate hourly step count as max - min for log data
            hourly_step_count = (
                step_events[step_events['Date'] == pd.to_datetime(selected_date).date()]
                .groupby(['Hour12', 'Hour'])['StepCount']
                .apply(lambda x: x.max() - x.min())
                .reset_index(name='HourlyStepCount')
            )
        else:
            # For 'all' case, calculate hourly step count for all days
            hourly_step_count = (
                step_events
                .groupby(['Hour12', 'Hour'])['StepCount']
                .apply(lambda x: x.max() - x.min())
                .reset_index(name='HourlyStepCount')
            )
            selected_date = 'All'

        # Check if 'hourly_step_count' is not empty before plotting
        if not hourly_step_count.empty:
            # Create an interactive bar chart with Plotly Express
            if selected_date == 'All':
                fig = px.bar(hourly_step_count, x='Hour12', y='HourlyStepCount',
                             title=f'Hourly Step Count Overall',
                             labels={'HourlyStepCount': 'Number of Steps'},
                             color='HourlyStepCount',  # Color by step count for additional insight
                             color_continuous_scale='blues')
            else:
                fig = px.bar(hourly_step_count, x='Hour12', y='HourlyStepCount',
                             title=f'Hourly Step Count on {selected_date}',
                             labels={'HourlyStepCount': 'Number of Steps'},
                             color='HourlyStepCount',  # Color by step count for additional insight
                             color_continuous_scale='blues')

            # Customize the layout
            fig.update_layout(
                xaxis=dict(title='Hour of the Day'),
                yaxis=dict(title='Number of Steps'),
                height=500,
                width=900
            )

            return fig
        else:
            print(f"No step count data available for {selected_date}.")
            return None
    else:
        print("DataFrame 'df' is not defined or is empty.")
        return None


def createStepcountCumCharts(df, date=None):
    if 'df' in locals() and not df.empty:
        step_events = df[df['EventId'] == 'E22'].copy()

        step_events['StepCount'] = step_events['Content'].apply(Utils.extract_step_count)
        step_events['Date'] = pd.to_datetime(step_events['Time']).dt.date
        step_events['Hour12'] = pd.to_datetime(step_events['Time']).dt.strftime('%I %p')

        # Removing Bad entries
        step_events = step_events.drop(
            step_events[(step_events['LineId'] == 1791) | (step_events['LineId'] == 1796)].index)

        if date and date.lower() != 'all':
            # Select a specific date for analysis
            selected_date = pd.to_datetime(date).date()
            cumulative_step_count = (
                step_events[step_events['Date'] == selected_date]
                .sort_values(by='Time')  # Sort by time for a continuous line chart
                .assign(AdjustedSteps=lambda x: x['StepCount'] - x['StepCount'].min())
                .assign(CumulativeSteps=lambda x: x['AdjustedSteps'])
            )

            # Check if 'cumulative_step_count' is not empty before plotting
            if not cumulative_step_count.empty:
                # Create an interactive line chart with Plotly Express
                fig = px.line(cumulative_step_count, x='Time', y='CumulativeSteps',
                              title=f'Cumulative Steps on {selected_date}',
                              labels={'CumulativeSteps': 'Cumulative Number of Steps'},
                              line_shape='linear',
                              markers=True)

                # Customize the layout
                fig.update_layout(
                    xaxis=dict(title='Time'),
                    yaxis=dict(title='Cumulative Number of Steps'),
                    # height=600,
                    # width=800
                )

                return fig, cumulative_step_count['CumulativeSteps'].max()
            else:
                print(f"No step count data available for {selected_date}.")
                return None
        else:
            print("Invalid date provided or 'all' specified. No plot generated.")
            return None
    else:
        print("DataFrame 'df' is not defined or is empty.")
        return None


def createCalorieCountCharts(df, date):
    if 'df' in locals() and not df.empty:
        calorie_events = df[df['EventId'] == 'E4'].copy()

        calorie_events['Calories'] = calorie_events['Content'].apply(Utils.extract_calories)
        calorie_events['Date'] = pd.to_datetime(calorie_events['Time']).dt.date
        calorie_events['Hour12'] = pd.to_datetime(calorie_events['Time']).dt.strftime('%I %p')
        calorie_events['Hour'] = pd.to_datetime(calorie_events['Time']).dt.hour

        if date.lower() != 'all':
            # Select a specific date for analysis
            selected_date = date
            # Calculate hourly calorie count as sum for 'E4' log data
            hourly_calorie_count = (
                calorie_events[calorie_events['Date'] == pd.to_datetime(selected_date).date()]
                .groupby(['Hour12', 'Hour'])['Calories']
                .apply(lambda x: x.max() - x.min())
                .reset_index(name='HourlyCalorieCount')
            )
        else:
            # For 'all' case, calculate hourly calorie count for all days
            hourly_calorie_count = (
                calorie_events
                .groupby(['Hour12', 'Hour'])['Calories']
                .apply(lambda x: x.max() - x.min())
                .reset_index(name='HourlyCalorieCount')
            )
            selected_date = 'All'

        # Check if 'hourly_calorie_count' is not empty before plotting
        if not hourly_calorie_count.empty:
            # Create an interactive bar chart with Plotly Express
            if selected_date == 'All':
                fig = px.bar(hourly_calorie_count, x='Hour12', y='HourlyCalorieCount',
                             title=f'Hourly Calorie Count Overall',
                             labels={'HourlyCalorieCount': 'Calories'},
                             color='HourlyCalorieCount',  # Color by calorie count for additional insight
                             color_continuous_scale='reds')
            else:
                fig = px.bar(hourly_calorie_count, x='Hour12', y='HourlyCalorieCount',
                             title=f'Hourly Calorie Count on {selected_date}',
                             labels={'HourlyCalorieCount': 'Calories'},
                             color='HourlyCalorieCount',  # Color by calorie count for additional insight
                             color_continuous_scale='reds')

            # Customize the layout
            fig.update_layout(
                xaxis=dict(title='Hour of the Day'),
                yaxis=dict(title='Calories'),
                height=500,
                width=900
            )

            return fig
        else:
            print(f"No calorie count data available for {selected_date}.")
            return None
    else:
        print("DataFrame 'df' is not defined or is empty.")
        return None


def createCaloriesCumulativeChart(df, date=None):
    if 'df' in locals() and not df.empty:
        calorie_events = df[df['EventId'] == 'E4'].copy()

        # Assuming 'extract_calories_from_e4' is a function that extracts calories from 'E4' event content
        calorie_events['Calories'] = calorie_events['Content'].apply(Utils.extract_calories)

        calorie_events['Date'] = pd.to_datetime(calorie_events['Time']).dt.date
        calorie_events['Hour12'] = pd.to_datetime(calorie_events['Time']).dt.strftime('%I %p')

        # Removing Bad entries
        calorie_events = calorie_events.drop(
            calorie_events[(calorie_events['LineId'] == 1791) | (calorie_events['LineId'] == 1796)].index)

        if date and date.lower() != 'all':
            # Select a specific date for analysis
            selected_date = pd.to_datetime(date).date()

            # Filter data for the selected date
            selected_data = calorie_events[calorie_events['Date'] == selected_date].copy()

            # Calculate cumulative calories over time and adjust by subtracting the minimum cumulative calories
            cumulative_calories = selected_data.groupby('Time')['Calories'].cumsum()
            cumulative_calories -= cumulative_calories.min()

            # Create an interactive line chart with Plotly Express
            fig = px.line(selected_data, x='Time', y=cumulative_calories,
                          title=f'Cumulative Calories on {selected_date}',
                          labels={'y': 'Cumulative Calories'},
                          line_shape='linear',
                          markers=True)

            # Customize the layout
            fig.update_layout(
                xaxis=dict(title='Time'),
                yaxis=dict(title='Cumulative Calories'),
            )

            return fig, cumulative_calories.max()
        else:
            print("Invalid date provided or 'all' specified. No plot generated.")
            return None
    else:
        print("DataFrame 'df' is not defined or is empty.")
        return None


def createCaloriesCumulativeAllDaysChart(df):
    if 'df' in locals() and not df.empty:
        calorie_events = df[df['EventId'] == 'E4'].copy()

        # Assuming 'extract_calories_from_e4' is a function that extracts calories from 'E4' event content
        calorie_events['Calories'] = calorie_events['Content'].apply(Utils.extract_calories)

        calorie_events['Date'] = pd.to_datetime(calorie_events['Time']).dt.date
        calorie_events['Hour12'] = pd.to_datetime(calorie_events['Time']).dt.strftime('%I %p')

        # Removing Bad entries
        calorie_events = calorie_events.drop(
            calorie_events[(calorie_events['LineId'] == 1791) | (calorie_events['LineId'] == 1796)].index)

        # Calculate cumulative calories over time and adjust by subtracting the minimum cumulative calories
        cumulative_calories = calorie_events.groupby('Time')['Calories'].cumsum()
        cumulative_calories -= cumulative_calories.min()

        # Create an interactive line chart with Plotly Express
        fig = px.line(calorie_events, x='Time', y=cumulative_calories,
                      title='Cumulative Calories for All Days',
                      labels={'y': 'Cumulative Calories'},
                      line_shape='linear',
                      markers=True)

        # Customize the layout
        fig.update_layout(
            xaxis=dict(title='Time'),
            yaxis=dict(title='Cumulative Calories'),
        )
        # Find the day with the maximum cumulative calories
        max_calories_day = calorie_events.loc[cumulative_calories.idxmax()]['Date']
        max_calories_value = cumulative_calories.max()

        return fig, max_calories_value, max_calories_day
    else:
        print("DataFrame 'df' is not defined or is empty.")
        return None
def createStandcountCharts(df, date):
    if 'df' in locals() and not df.empty:
        stand_events = df[df['EventId'] == 'E42'].copy()

        stand_events['StandCount'] = stand_events['Content'].apply(Utils.extract_stand_count)
        stand_events['Date'] = pd.to_datetime(stand_events['Time']).dt.date
        stand_events['Hour12'] = pd.to_datetime(stand_events['Time']).dt.strftime('%I %p')
        stand_events['Hour'] = pd.to_datetime(stand_events['Time']).dt.hour

        # Removing Bad entries
        stand_events = stand_events.drop(
            stand_events[(stand_events['LineId'] == 3579)].index)

        if date.lower() != 'all':
            # Select a specific date for analysis
            selected_date = date
            # Calculate hourly stand count as max - min for log data
            hourly_stand_count = (
                stand_events[stand_events['Date'] == pd.to_datetime(selected_date).date()]
                .groupby(['Hour12', 'Hour'])['StandCount']
                .apply(lambda x: x.max() - x.min())
                .reset_index(name='HourlyStandCount')
            )
        else:
            # For 'all' case, calculate hourly stand count for all days
            hourly_stand_count = (
                stand_events
                .groupby(['Hour12', 'Hour'])['StandCount']
                .apply(lambda x: x.max() - x.min())
                .reset_index(name='HourlyStandCount')
            )
            selected_date = 'All'

        # Check if 'hourly_stand_count' is not empty before plotting
        if not hourly_stand_count.empty:
            # Create an interactive bar chart with Plotly Express
            if selected_date == 'All':
                fig = px.bar(hourly_stand_count, x='Hour12', y='HourlyStandCount',
                             title=f'Hourly Stand Count Overall',
                             labels={'HourlyStandCount': 'Number of Stand Steps'},
                             color='HourlyStandCount',  # Color by stand count for additional insight
                             color_continuous_scale='greens')
            else:
                fig = px.bar(hourly_stand_count, x='Hour12', y='HourlyStandCount',
                             title=f'Hourly Stand Count on {selected_date}',
                             labels={'HourlyStandCount': 'Number of Stand Steps'},
                             color='HourlyStandCount',  # Color by stand count for additional insight
                             color_continuous_scale='greens')

            # Customize the layout
            fig.update_layout(
                xaxis=dict(title='Hour of the Day'),
                yaxis=dict(title='Number of Stand Steps'),
                height=500,
                width=900
            )

            return fig
        else:
            print(f"No stand count data available for {selected_date}.")
            return None
    else:
        print("DataFrame 'df' is not defined or is empty.")
        return None

