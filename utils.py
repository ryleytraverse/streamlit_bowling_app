import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
    
# Create analysis tabs for all time and league by league performance breakdowns
def create_analysis_tab(df:pd.DataFrame, title_name:str):
    scratch_over_time = st.container()
    games_over_time = st.container()
    game_average = st.container()

    # Plot Average Bowling Scratch Over Time
    with scratch_over_time:
        fig_go = go.Figure()
        fig_go.add_trace(go.Scatter(x=df['Date'], y=df['average'], mode='lines+markers', name='Average Over Time', line=dict(color='magenta')))
        t = 'Plot of Bowling Average over Time'
        fig_go.update_layout(title=t, xaxis_title='Date', yaxis_title='Bowling Average')
        st.plotly_chart(fig_go)

    # Plot of Scratch Performance in Each Game over Time
    with games_over_time:
        fig_go = go.Figure()
        fig_go.add_trace(go.Scatter(x=df['Date'], y=df['Game1'], mode='lines+markers', name='Game 1 Score', line=dict(color='blue')))
        fig_go.add_trace(go.Scatter(x=df['Date'], y=df['Game2'], mode='lines+markers', name='Game 2 Score', line=dict(color='cyan')))
        fig_go.add_trace(go.Scatter(x=df['Date'], y=df['Game3'], mode='lines+markers', name='Game 3 Score', line=dict(color='lime')))
        t = 'Plot of Bowling Score over Time for Each Game'
        fig_go.update_layout(title=t, xaxis_title='Date', yaxis_title='Score')
        st.plotly_chart(fig_go)

    # Plot of Game Averages
    with game_average:
        x_values = ['Game 1', 'Game 2', 'Game 3']
        y_values = []
        y_values.append(np.mean(df['Game1']))
        y_values.append(np.mean(df['Game2']))
        y_values.append(np.mean(df['Game3']))
        fig_go = go.Figure()
        fig_go.add_trace(go.Bar(x=x_values, y=y_values, marker=dict(color= ['blue', 'cyan', 'lime'])))
        fig_go.update_layout(title=title_name, xaxis_title='Game', yaxis_title='Average Score')
        st.plotly_chart(fig_go)

def calculate_all_time_weeks(df):
    # Calculate all time week number
    week_nums = []
    count = 0
    for l in df.League.unique():
        df_temp = df[df['League']==l]
        max_week = int(df_temp['Week'].iloc[-1])
        weeks = list(df_temp['Week'])
        weeks = [x+count for x in weeks]
        count += max_week
        week_nums = week_nums + weeks
    df['week_num_all_time'] = week_nums
    return df       