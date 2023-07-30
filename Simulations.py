import os
import pytz
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as ex

class MonteCarlo:
    """

    """

    def __init__(self, data, initial_investment, weights="", n_simulation=500, n_trading_days=252):
        """
            Initiate class attributes, check for errors and update attributes if applicable

            Parameters
            ----------
            data: pandas.DataFrame
                DataFrame with the stocks price information
            weights: list(float)
                A list that represents the total insvestiments percentege per asset.
            n_simulation: int
                Number of simulation samples
            n_trading_days: int
                Number of trading days to simulate
        """
        self.data = data
        self.weights = weights
        self.n_sim = n_simulation
        self.n_trading = n_trading_days
        self.initial_investment = initial_investment
        self.simulated_returns = ""

        self.check_errors()
        self.update_weights()
        self.update_daily_ret()
        self.update_cum_return()

    def update_daily_ret(self):
        """ Update the class data with the daily return column if it doesn't exist """
        if not "daily_return" in self.data.columns.get_level_values(1).unique():
            close = self.data.xs("close", level=1, axis=1).pct_change()
            tickers = self.data.columns.get_level_values(0).unique()
            columns = [(x, "daily_return") for x in tickers]
            close.columns = pd.MultiIndex.from_tuples(columns)
            self.data = self.data.merge(close, left_index=True, right_index=True).reindex(columns=tickers, level=0)

    def update_cum_return(self):
        """  Calculate cumulative return if simulated_returns isn't a Pandas DataFrame """
        if not isinstance(self.simulated_returns, pd.DataFrame):
            self.monte_carlo_simulation()

    def update_weights(self):
        """ Update portfolio weights if its empty! """
        if self.weights=="":
            n_stocks = len(self.data.columns.get_level_values(0).unique())
            self.weights = [1.0/n_stocks for it in range(0,n_stocks)]
   
    def check_errors(self):
        """ Raise errors for the given inputs of the class """
        if not isinstance(self.data, pd.DataFrame):
            raise TypeError("The data variable must be a Pandas dataframe")

        if round(sum(self.weights),2) < .99:
            raise AttributeError("Sum of weights must be equal one!")

    def quantile(self):
        """  """ 
        range = self.last_returns.quantile(q=[.025, .25, .5, .75, .975]).T
        range.index = ["Lower", "Q1", "Q2", "Q3", "Upper"]
        return range

    def metrics(self):
        """ Add other metrics later """
        above_initial, below_initial = [], []
        for r in self.last_returns:
            if r >= self.initial_investment:
                above_initial.append(r) 
            else:
                below_initial.append(r)
        percent = lambda data: (len(data)*100)/len(self.last_returns)

        return {
            "above_initial": above_initial, 
            "below_initial": below_initial,
            "below_pct": percent(below_initial),
            "above_pct": percent(above_initial)
        }

    def distribution(self):
        range = self.quantile()
        title = f"Range of simulated returns in next {self.n_trading//252} years, 95% of returns are between {int(range[0])} to {int(range[4])}"
        fig = ex.histogram(data_frame=self.last_returns, marginal="violin",title=title, nbins=30)
        return fig

    def monte_carlo_simulation(self):
        """ 
            Monte carlo simulation from daily returns with Cholesky Decomposition to determine Lower Triangular Matrix
        """
        daily_returns = self.data.xs('daily_return', level=1, axis=1)
        cov = daily_returns.cov()
        mean_returns = daily_returns.mean().tolist() 
        returns = np.full(shape=(self.n_trading, len(self.weights)), fill_value=mean_returns)
        returns = returns.T 
        portfolio_sims = np.full(shape=(self.n_trading, self.n_sim), fill_value=.0)
        
        for sim in range(0, self.n_sim):
            Z =  np.random.normal(size=(self.n_trading, len(self.weights)))
            L = np.linalg.cholesky(cov)
            daily_returns = returns + np.inner(L, Z)
            portfolio_sims[:,sim] = np.cumprod(np.inner(self.weights, daily_returns.T)+1)* self.initial_investment

        self.simulated_returns = pd.DataFrame(portfolio_sims)
        self.last_returns = self.simulated_returns.iloc[-1,:]
        self.last_returns.name = "Value"     


    