import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from Simulations import MonteCarlo

def beta(stock_df):
    """
    """
    beta_list = []
    covariance = .0
    covariance_list = []

    daily_returns = stock_df.dropna().pct_change()
    columns = daily_returns.columns.tolist()

    for column in columns:
        if column == columns[0]:
            beta_list.append(1)
            covariance_list.append(1)
            continue

        covariance = daily_returns[column].cov(daily_returns[columns[0]])
        variance = daily_returns[columns[0]].var()        
        
        beta_list.append(covariance / variance)
        covariance_list.append(covariance)

    beta = {"Assets": columns, "Beta": beta_list}

    st.header("")
    st.subheader("Beta of Assets Compared to Index")
    st.dataframe(beta)




def cum_returns(stock_df):
    """
    """
    daily_return = stock_df.dropna().pct_change()
    cumulative_return = (1+daily_return).cumprod()

    st.header("")
    st.subheader("Historical Normalized Cumulative Returns")
    st.line_chart(cumulative_return)


def correlation_heatmap(stock_df, show_dataframe):
    """
    """
    price_correlation = stock_df.corr()
    st.subheader("Assets Correlation heatmap")
     
    fig, ax = plt.subplots()

    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    mask = np.triu(np.ones_like(price_correlation, dtype=bool))
    sns.heatmap(price_correlation, ax=ax, mask=mask, cmap=cmap)
    st.write(fig)

    if show_dataframe:
        st.subheader("Correlation Dataframe")
        st.dataframe(price_correlation)


def display_portfolio_return(stock_df, choices):
    """
    """
    weights, investment = choices["weights"], choices["investment"]
    
    daily_return = stock_df.dropna().pct_change()
    portfolio_returns = daily_return.dot(weights)
    cumulative_return = (1+portfolio_returns).cumprod()
    cumulative_profit = investment * cumulative_return
    cumulative_profit= pd.DataFrame(cumulative_profit, columns=["Investiment"])
    st.header("")
    st.subheader("Historical Cumulative Returns Based on Inputs")
    st.subheader("")
    st.line_chart(cumulative_profit)



def monte_carlo(monte_carlo_df, choices, show_dataframe):
    """
    """
    weights, investment, forecast_years, simulations = choices["weights"], choices["investment"], choices["forecast_years"], choices["simulations"]

    simulation = MonteCarlo(
        data=monte_carlo_df,
        weights=weights,
        initial_investment=investment,
        n_simulation=simulations,
        n_trading_days=252*forecast_years
    )

    # summary_results = simulation.simulated_return
    # simulation.simulated_return *= investment
    
    st.line_chart(simulation.final_returns)
    st.write(simulation.dist())
    # st.plotly_chart(simulation.final_returns.hist())
    # simulation_summary = simulation.summarize_cum_return()

    # st.header("")
    # st.header("")
    # st.subheader(f"Simulation Summary Cumulative Returns {forecast_years} Yr(s) Outlook")
    # st.line_chart(summary_results)
    # lower_cum_return = round(simulation_summary[8] * investment, 2)
    # upper_cum_return = round(simulation_summary[9] * investment, 2)
    # st.write(f"95% of simulations that an initial investment of ${investment} over the next {forecast_years} years might result within the range of {lower_cum_return} and {upper_cum_return} USD!")
    
    # # show_dataframe = st.checkbox("Monte carlo dataframe")
    # if show_dataframe:
    #     st.dataframe(simulation_summary)