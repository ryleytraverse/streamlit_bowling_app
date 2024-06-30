import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import helper_functions as hf
from scipy.signal import savgol_filter
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def main():
    # Define wanted number of dashboard tabs and give them names
    overall_tab, league_tab, prediction_tab, add_data_tab = st.tabs(['All Time Analysis', 'League by League Analysis', 'Score Predictions', 'Adding Data'])

    # Load Data:
    df_bowling = pd.read_csv('Bowling.csv')
    df_bowling['scratch'] = df_bowling['Game1'] + df_bowling['Game2'] + df_bowling['Game3']
    df_bowling['average'] = df_bowling['scratch'].astype(float)/3

    with st.sidebar:
        st.header('This streamlit dashboard was made for my personal use and allows for updates, tracking, and prediction my bowling performance.')
        st.subheader('The first tab shows my all time bowling score analysis.')
        st.subheader('The second tab shows my bowling score analysis on a league by league basis.')
        st.subheader('The third tab shows my predicted bowling score for the following week.')
        st.subheader('The fourth tab allows for me to update the data with my scores after I bowl.')

    with overall_tab:
        title_container = st.container()
        with title_container:
            st.title('Ryley Traverse Bowling League Analysis Interactive Dashboard')

        hf.create_analysis_tab(df_bowling, 'All Time Game Average')

    with league_tab:
        title_container = st.container()
        with title_container:
            st.title('Ryley Traverse Bowling League Analysis Interactive Dashboard')
        league_select = st.container()
        with league_select:
            league = st.selectbox('Which season of league do you want to examine?', list(df_bowling.League.unique()))
        df_league = df_bowling[df_bowling['League']==league]
        hf.create_analysis_tab(df_league, 'Selected League Game Average')

    with prediction_tab:
        title_container = st.container()
        smooth_plot = st.container()
        prediction_container = st.container()


        with title_container:
            st.title('Ryley Traverse Bowling League Analysis Interactive Dashboard')

        with smooth_plot:
            df_bowling_smooth = hf.calculate_all_time_weeks(df_bowling)
            # Smooth scratch recordings
            window_size = st.slider("Choose Smoothing Window Size", 3, 30, 7)
            poly_order = st.number_input("Choose Smoothing Polynomial Order", min_value=1, max_value=5, value=2)
            df_bowling_smooth['scratch_smoothed'] = savgol_filter(df_bowling_smooth['scratch'].to_numpy(), window_size, poly_order)
            fig_go = go.Figure()
            fig_go.add_trace(go.Scatter(x=df_bowling_smooth['week_num_all_time'], y=df_bowling_smooth['scratch'], mode='lines+markers', name='Scratch', line=dict(color='magenta')))
            fig_go.add_trace(go.Scatter(x=df_bowling_smooth['week_num_all_time'], y=df_bowling_smooth['scratch_smoothed'], mode='lines+markers', name='Scratch Smoothed', line=dict(color='indigo')))
            t = 'Plot of Scratch over Time after Smoothing'
            fig_go.update_layout(title=t, xaxis_title='All Time Week Number', yaxis_title='Score')
            st.plotly_chart(fig_go)

        with prediction_container:
            X = df_bowling_smooth['week_num_all_time'].to_numpy().reshape(-1, 1)
            y = df_bowling_smooth['scratch'].to_numpy()
            model_poly_order = st.number_input("Choose Regression Model Polynomial Order", min_value=1, max_value=10, value=1)
            poly_reg = PolynomialFeatures(degree=model_poly_order)
            X_poly = poly_reg.fit_transform(X)
            lin_reg = LinearRegression()
            lin_reg.fit(X_poly, y)
            next_time_step = max(df_bowling_smooth['week_num_all_time']) + 1
            X_pred = np.array(next_time_step).reshape(1, -1)
            X_pred_poly = poly_reg.transform(X_pred)
            pred = lin_reg.predict(X_pred_poly)
            preds = lin_reg.predict(X_poly)
            t = 'Scratch Prediction for Next Week of Bowling: ' + str(round(pred[0]))
            st.write(t)

            fig_go = go.Figure()
            fig_go.add_trace(go.Scatter(x=df_bowling_smooth['week_num_all_time'], y=df_bowling_smooth['scratch'], mode='lines+markers', name='Scratch', line=dict(color='magenta')))
            fig_go.add_trace(go.Scatter(x=df_bowling_smooth['week_num_all_time'], y=preds, mode='lines', name='Fitted Regression Line', line=dict(color='indigo')))
            fig_go.add_trace(go.Scatter(x=[next_time_step], y=pred, mode='markers', name='Next League Scratch Prediction', line=dict(color='indigo')))
            t = 'Plot of Scratch with Regression Line and Prediction Shown'
            fig_go.update_layout(title=t, xaxis_title='All Time Week Number', yaxis_title='Score')
            st.plotly_chart(fig_go)

        with add_data_tab:
            df_saved = pd.read_csv('Bowling.csv')
            league_name = st.text_input("League Name: ", "thab_summer_24")
            league_date = st.text_input("Date: ", "1/1/24")
            league_week = st.text_input("Week Number: ")
            game1 = st.text_input("Game 1 Score: ")
            game2 = st.text_input("Game 2 Score: ")
            game3 = st.text_input("Game 3 Score: ")
            if st.button("Update Bowling Data", type="primary"):
                df_saved.loc[len(df_saved)] = [league_name, league_date, int(league_week), int(game1), int(game2), int(game3)]
                df_saved.to_csv('Bowling.csv')

    #     with plot_container_plt:
    #         fig_plt, ax = plt.subplots()
    #         ax.scatter(idk, idk2, s=10, color='cyan', label='Data')
    #         plt.title('This is a plot')
    #         plt.xlabel('X')
    #         plt.ylabel('Y')
    #         leg = plt.legend()
    #         for lh in leg.legendHandles:
    #             lh.set_alpha(1)
    #         st.pyplot(fig_plt)

if __name__ == '__main__':
    main()
