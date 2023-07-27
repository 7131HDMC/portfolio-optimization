import pandas as pd
import yfinance as yf
import streamlit as st 
from datetime import datetime, date

def get_symbol_data(choices):
    """
    """
    start_date, end_date, symbols = choices["start_date"], choices["end_date"], choices["symbols"]
    print(start_date)
    monte_carlo_data = []
    tickers_data_list = []

    try:
        for ticker in symbols:
            data =  yf.download(
                ticker,
                start=start_date,
                end=end_date
            )

            data = data.dropna()

            monte_carlo_data.append(data)
            data =  data.drop(columns=["Open", "High", "Low", "Close", "Volume"])
            data = data.rename(columns={"Adj Close": ticker})
            tickers_data_list.append(data)
    except Exception as err:
        print(err)
    
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

