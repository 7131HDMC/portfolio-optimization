import os
import pytz
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

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
        self.final_returns = ""

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
        """  Calculate cumulative return if final_returns isn't a Pandas DataFrame """
        if not isinstance(self.final_returns, pd.DataFrame):
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

    def summarize_cum_return(self):
        """  """
        metrics = self.final_returns.iloc[-1].describe()
        ci_series = self.confidence_interval
        ci_series.index = ["95% CI Lower", "95% CI Upper"]
        return metrics.append(ci_series)

    def dist(self):
        # last = self.final_returns.columns[-1:].values[0]
        # print(last)
        last = self.final_returns.iloc[-1,:]
        print(last)
        fig, ax = plt.subplots()
        sns.histplot(data=last, ax=ax)
        return fig

    def monte_carlo_simulation(self):
        """ 
        
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

        self.final_returns = pd.DataFrame(portfolio_sims)


    