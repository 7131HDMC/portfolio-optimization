import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from Simulations import MonteCarlo

def beta(stock_df, weights):
    """
    """
    beta_stocks = []
    beta_weight = []
    covariance = .0
    covariance_list = []

    daily_returns = stock_df.dropna().pct_change()
    columns = daily_returns.columns.tolist()
    i=0
    for column in columns:

        if column == columns[0]:
            beta_stocks.append(1)
            beta_weight.append(1*weights[i])
            covariance_list.append(1)
            continue

        covariance = daily_returns[column].cov(daily_returns[columns[0]])
        variance = daily_returns[columns[0]].var() 
        print(variance)       
        beta = covariance / variance
        beta_stocks.append(beta)
        beta_weight.append(beta*weights[i])
        covariance_list.append(covariance)
        i+=1
    

    beta = {"Assets": columns, "Beta": beta_stocks, "Beta Weight": beta_weight}

    beta_weight = np.array(beta_weight)

    container = st.container()

    container.header("")
    container.subheader("Beta of Assets Compared to Index")

    col1, col2, col3 = container.columns([3,3,3])

    col1.subheader("")
    col1.dataframe(beta)
    portfolio_beta = {"Portfolio Beta": beta_weight.sum()}
    col1.dataframe(portfolio_beta)




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
    st.subheader("Historical Cumulative Returns!")
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

    st.header("")
    st.header("")
    st.subheader(f"Simulation Cumulative Returns {forecast_years} Yr(s) Outlook")
    st.subheader("")
    st.line_chart(simulation.simulated_returns)
    st.plotly_chart(simulation.distribution())
    metrics = simulation.metrics()
    st.write(f"%.0f percent of the simulations have an estimated return above the initial investment! "%metrics["above_pct"])
