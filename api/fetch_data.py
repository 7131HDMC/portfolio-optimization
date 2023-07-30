import pandas as pd
import yfinance as yf
import investpy as ip
import streamlit as st 
from datetime import datetime, timedelta

class InvestPyHandler:
    """

    """
    def __init__(self):
        """  """
        self.symbols = ""
        
    def get_historical_data(self, symbol, country, from_date, to_date, type, interval="Daily"):
        """  """
        print(from_date)
        if type=="index":
            return ip.get_index_historical_data(index=symbol,
                                    country=country,
                                    from_date=from_date,
                                    to_date=to_date,
                                    interval=interval)

        return ip.get_stock_historical_data(stock=symbol,
                                  country=country,
                                  from_date=from_date,
                                  to_date=to_date,
                                  interval=interval)
    
    def get_assets_list(self, country, type):
        """  """
        if type=="index":
            return ip.get_indices_list(country=country)
        return ip.get_stocks_list(country=country)
    
    def clear(self):
        st.cache_resource.clear()

    def load_st_accessors(self, countries):
        """  """
        self.country = st.sidebar.selectbox("Select a country: ", countries)
        # index_list = self.get_assets_list(self.country, "index")
        self.index = st.sidebar.text_input("Select a index: ", "SPY")

        stocks_list = self.get_assets_list(self.country, "stocks")
        self.symbols = st.sidebar.multiselect("Select 5-10 Stocks:", stocks_list)

        self.symbols.insert(0, self.index)
        if "Brazil" in self.country:
            self.symbols = [ s+".SA" for s in self.symbols]

    @st.cache_data
    def get_data(_self, choices):
        """
        """
        start_date, end_date, symbols = choices["start_date"], choices["end_date"], choices["symbols"]

        monte_carlo_data = []
        tickers_data_list = []
        try:
            for it in range(len(symbols)):
                type = "index" if it==0 else "stock"
                # data = self.get_historical_data(symbols[it], 
                #     self.country,
                #     start_date,
                #     end_date, 
                #     type
                # )
                data = yf.download(
                    symbols[it],
                    start=start_date,
                    end=end_date
                )

                data = data.dropna()

                monte_carlo_data.append(data)
                data =  data.drop(columns=["Open", "High", "Low", "Close", "Volume"])
                data = data.rename(columns={"Adj Close": symbols[it]})
                tickers_data_list.append(data)
        except Exception as err:
            print(f"Exception: {err}")
        
        stock_df = pd.concat(tickers_data_list, axis="columns", join="inner")
        monte_carlo_df  = pd.concat(monte_carlo_data, axis="columns", join="inner") 

        multi_columns = []
        columns = ["Open", "High", 'Low', "Close", "close", "Volume"]
        for ticker in symbols:
            for column in columns:
                multi_columns.append((ticker, column))

        monte_carlo_df.columns = pd.MultiIndex.from_tuples(multi_columns)
        return {
            "monte_carlo_df": monte_carlo_df,
            "stock_df": stock_df
        }
