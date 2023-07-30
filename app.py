import pandas as pd
import streamlit as st
from datetime import date, timedelta, datetime
from api.fetch_data import InvestPyHandler
from views.plots import (
    beta, correlation_heatmap,
    display_portfolio_return,
    cum_returns,
    monte_carlo
)

class ProjectDemo():

    def __init__(self):
        self.countries = ['United States', 'Brazil']
        self.interval = "Daily"
        self.ip = InvestPyHandler()
        self.runs_max = 100
        self.reset = False
        self.err=False

    def load_heading(self):
        """
        """
        with st.container():
            st.title("Portfolio Analysis")
            h = st.subheader("This app performs portfolio analysis and use monte carlo simulation.")

    def get_sidebar_options(self):
        """
        """
        start_date =date.today()
        yesterday = start_date - timedelta(days=1)

        self.years_window_el = st.sidebar.number_input("How many years? ", min_value=1, max_value=5, value=1)

        self.ip.load_st_accessors(self.countries)

        self.weights_el = st.sidebar.text_input("Enter the investiment weights: ", "20,20,20,20,20")
        self.investment_el = st.sidebar.number_input("Enter the initial investment: ", min_value=1000, max_value=100000, value=1000)
        self.forecast_years_el = st.sidebar.number_input("Enter the forecast years for the simulation: ", min_value=2, max_value=5, value=2)
        

        self.start_date = start_date.replace(year=(yesterday.year - self.years_window_el), month=yesterday.month, day=yesterday.day)#.strftime('%d/%m/%Y')
        self.end_date = yesterday

        self.show_dataframe = st.sidebar.checkbox("Show dataframes?")

        self.run_simulations = st.sidebar.checkbox("Run Monte Carlo Simulation with default runs")

        self.submitted = st.sidebar.button("Submit")


    def get_choices(self):
        """
        """
        if (not self.err):
            choices = {
                'user_start_date': date.today(),
                'start_date': self.start_date,
                'end_date': self.end_date,
                'symbols': self.ip.symbols,
                'weights': self.weights_el,
                'investment': self.investment_el,
                'forecast_years': self.forecast_years_el,
                'simulations': self.runs_max
            }

            df = self.ip.get_data(choices)# run 

            return {
                "choices": choices,
                "combined_df": df
            }

        # self.reset_app()

    def get_choices_from_sidebar(self):
        """
        """
        self.get_sidebar_options()
        if self.submitted:
            self.check_to_reset()
            return self.get_choices()

    def reset_app(self):
        if self.reset:
            st.cache_resource.clear()
            st.session_state.clear()

    def pop_error(self, error):
        st.sidebar.write(f"{error}!")
        st.sidebar.write(f"Syntax error!")
        self.err=True
        # self.reset = st.sidebar.button("Reset APP")

    def check_to_reset(self):
        try:
            self.weights_el = [ float(w)/100 for w in self.weights_el.split(",")]
            print(self.ip.symbols)
            if len(self.ip.symbols)==0:
                self.pop_error("Check stocks list!")
            if sum(self.weights_el)!=1:
                self.pop_error("Check weights sum!")
            if len(self.weights_el) != len(self.ip.symbols):
                self.pop_error("Check weights amount!")

        except ValueError as err:
            self.pop_error("Check weights format!")
            # st.error(e)

    def run(self):
        """
        """
        self.load_heading()
        choices = self.get_choices_from_sidebar()
        if (not self.err) and choices:
            # beta(choices['combined_df']["stock_df"])
            # cum_returns(choices['combined_df']["stock_df"])
            # correlation_heatmap(choices['combined_df']["stock_df"], self.show_dataframe)
            # display_portfolio_return(choices['combined_df']["stock_df"], choices['choices'])

            if self.run_simulations:
                with st.spinner("Running Monte Carlo Simulation... "):
                    monte_carlo(choices['combined_df']["monte_carlo_df"], choices['choices'], self.show_dataframe)

if __name__ == "__main__":
    main = ProjectDemo()
    main.run()