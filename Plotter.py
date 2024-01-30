import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import Utils
import plotly.graph_objs as go
import Utils


def createScreenStatusTimeline(df):
    screenData = Utils.generateScreenStatusData(df)
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

def createStepcountCharts(df):
    pass

