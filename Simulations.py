import os
import pytz
import numpy as np
import pandas as pd
import datetime as dt

class MonteCarlo:
    """

    """

    def __init__(self, data, weights="", n_simulation=500, n_trading_days=252):
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
        self.simulated_return = ""

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
        """  Calculate cumulative return if simulated_return isn't a Pandas DataFrame """
        if not isinstance(self.simulated_return, pd.DataFrame):
            self.cum_return()

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

    def plot_simulation(self):
        """  """

        title = f"{self.n_sim} Simulations of Cumulative Return Trajectories Over the Next {self.n_trading} Trading Days."
        return self.simulated_return.plot(legend=None, title=title)
    
    def plot_distribution(self):
        """  """
        title = f"Distribution of Final Cumulative Returns Across {self.n_sims} Simulations!"
        plt = self.simulated_return.iloc[-1, :].plot(kind="hist", bins=10, density=True, title=title)
        plt.axvline(self.confidence_interval.iloc[0], color='r')
        plt.axvline(self.confidence_interval.iloc[1], color='r')
        return plt
    
    def summarize_cum_return(self):
        """  """
        metrics = self.simulated_return.iloc[-1].describe()
        ci_series = self.confidence_interval
        ci_series.index = ["95% CI Lower", "95% CI Upper"]
        return metrics.append(ci_series)

    def cum_return(self):
        """  """
        last_prices = self.data.xs('close', level=1, axis=1)[-1:].values.tolist()[0]
        daily_returns = self.data.xs('daily_return', level=1, axis=1)
        mean_returns = daily_returns.mean().tolist()        
        std_returns = daily_returns.std().tolist()
        cum_returns = pd.DataFrame()

        for sim_it in range(self.n_sim):
            sim_vals = [[price] for price in last_prices]
            for price_it in range(len(last_prices)):
                for trading_it in range(self.n_trading):
                    simulated_price = sim_vals[price_it][-1] * ( 1 + np.random.normal(mean_returns[price_it], std_returns[price_it]))
                    sim_vals[price_it].append(simulated_price)
            sim_df = pd.DataFrame(sim_vals).T.pct_change()
            sim_df = (sim_df.dot(self.weights)).fillna(0)
            cum_returns[sim_it] = (1 + sim_df).cumprod()

        self.simulated_return = cum_returns
        self.confidence_interval =  cum_returns.iloc[-1, :].quantile(q=[.025, .975])
        return cum_returns


    