import pandas as pd
import streamlit as st
from datetime import date, timedelta
from api.fetch_data import (get_symbol_data)
from views.plots import (
    beta, correlation_heatmap,
    display_portfolio_return,
    cum_returns,
    monte_carlo
)

class ProjectDemo():

    def __init__(self):
        self.runs_max = 500
        self.reset = False
        self.err=False

    def load_heading(self):
        """
        """
        with st.container():
            st.title("Portfolio Analysis")
            h = st.subheader("This app performs portfolio analysis with monte carllo simulation.")

    def get_sidebar_options(self):
        """
        """
        start_date =date.today()
        yesterday = start_date - timedelta(days=1)

        self.years_window_el = st.sidebar.number_input("How many years? ", min_value=1, max_value=5, value=1)

        self.tickers_el = st.sidebar.text_input("Enter 1 index and 3 stock symbols: ", "SPY,AAPL,AMZN,NVDA")
        self.crypto_el = st.sidebar.text_input("Enter 2 cryoto symbol pair: ",  'BTC-USD,ETH-USD')

        self.weights_el = st.sidebar.text_input("Enter the investiment weights: ", "0.2,0.2,0.2,0.2,0.1,0.1")
        self.investment_el = st.sidebar.number_input("Enter the initial investment: ", min_value=1000, max_value=100000, value=1000)
        self.forecast_years_el = st.sidebar.number_input("Enter the forecast years for the simulation: ", min_value=5, max_value=15, value=5)
        

        self.start_date = start_date.replace(year=(yesterday.year - self.years_window_el), month=yesterday.month, day=yesterday.day)
        self.end_date = yesterday

    def get_choices(self):
        """
        """
        symbols = []
        
        tickers_list = self.tickers_el.split(",")
        weights = self.weights_el.split(",")
        crypto_list = self.crypto_el.split(",")

        symbols.extend(tickers_list)
        symbols.extend(crypto_list)

        weights_list = []  
        for w in weights:
            weights_list.append(float(w))
        
        self.check_to_reset(tickers_list, crypto_list, weights_list)

        if not self.reset:
            choices = {
                'user_start_date': date.today(),
                'start_date': self.start_date,
                'end_date': self.end_date,
                'symbols': symbols,
                'weights': weights_list,
                'investment': self.investment_el,
                'forecast_years': self.forecast_years_el,
                'simulations': self.runs_max
            }

            df = get_symbol_data(choices)# run 

            return {
                "choices": choices,
                "combined_df": df
            }

        self.reset_app()

    def get_choices_from_sidebar(self):
        """
        """

        self.get_sidebar_options()
        submitted = st.sidebar.button("Submit")
        if submitted:
            return self.get_choices()

    def reset_app(self):
        self.tickers_el = st.sidebar.text_input('Enter 1 index and 3 stock symbols.', 'SPY,AMZN,TSLA,NVDA')
        self.crypto_el = st.sidebar.text_input('Enter 2 crypto symbols only as below', 'BTC-USD,ETH-USD')
        self.weights_el = st.sidebar.text_input('Enter The Investment Weights', '0.2,0.2 ,0.2,0.2,0.1,0.1')
        st.experimental_singleton.clear()

    def pop_error(self, error):
        st.sidebar.write(f"{error}!")
        st.sidebar.write(f"Syntax error!")
        self.err=True
        self.reset = st.sidebar.button("Reset APP")

    def check_to_reset(self, tickers, crypto, weights):
        if len(tickers)!=4:
            self.pop_error("Check stock tickers")
        if len(crypto)!=2:
            self.pop_error("Check crypto tickers")
        if sum(weights)!=1:
            self.pop_error("Check weights")

    def run(self):
        """
        """
        self.load_heading()
        choices = self.get_choices_from_sidebar()
        if (not self.err) and choices:
            print(choices)
            beta(choices['combined_df']["stock_df"])
            cum_returns(choices['combined_df']["stock_df"])
            correlation_heatmap(choices['combined_df']["stock_df"])
            display_portfolio_return(choices['combined_df']["stock_df"], choices['choices'])


if __name__ == "__main__":
    main = ProjectDemo()
    main.run()