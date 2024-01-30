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


import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import Utils

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import Utils

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import Utils
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import Utils

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
