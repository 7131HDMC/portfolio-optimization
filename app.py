import pandas as pd
import streamlit as st
from datetime import date, timedelta
from api.fetch_data import (get_symbol_data)
from views.plots import (
    beta, basic_portfolio,
    display_portfolio_return,
    display_heat_map,
    monte_carlo
)

class ProjectDemo():

    def __init__(self):
        self.runs_max = 500
        self.reset = False

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

        years_window = st.sidebar.number_input("How many years? ", min_value=1, max_value=5, value=1)

        tickers = st.sidebar.text_input("Enter 1 index and 3 stock symbols: ", "SPY,APPL,AMZN,NVDA")
        cripto = st.sidebar.text_input("Enter 2 cryoto symbol pair: ",  'BTC-USD,ETH-USD')

        weights = st.sidebar.text_input("Enter the investiment weights: ", "0.2,0.2,0.2,0.2,0.1,0.1")
        investment = st.sidebar.number_input("Enter the initial investment: ", min_value=1000, max_value=100000, value=1000)
        forecast_years = st.sidebar.number_input("Enter the forecast years for the simulation: ", min_value=5, max_value=15, value=5)
        

        start_date = start_date.replace(year=(yesterday.year - years_window), month=yesterday.month, day=yesterday.day)
        end_date = yesterday
        return (years_window, tickers, cripto, weights, investment, forecast_years)

    def get_choices(self):
        """
        """
        

    def get_choices_from_sidebar(self):
        """
        """
        choices = {}
        symbols = []
        self.get_sidebar_options()
        submitted = st.sidebar.button("Submit")
        if submitted:
            return self.get_choices()

    def reset_app(self, error):
        st.sidebar.write(f"{error}!")
        st.sidebar.write(f"Syntax error!")
        self.reset = st.sidebar.button("Reset APP")


    def run(self):
        """
        """
        self.load_heading()
        choices = self.get_choices_from_sidebar()
        if choices:
            pass

if __name__ == "__main__":
    main = ProjectDemo()
    main.run()