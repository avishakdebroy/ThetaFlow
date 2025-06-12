"""
Module: data_fetch
Purpose: To fetch live TSLA options data using open-source data from yfinance.
"""

import yfinance as yf
import pandas as pd


def get_options_data(ticker_symbol):
    """
    Fetch the options chain for a given ticker (e.g., TSLA) from yfinance.
    Automatically selects the nearest expiration date.

    Args:
        ticker_symbol (str): Stock ticker, e.g., 'TSLA'.

    Returns:
        DataFrame: The call options chain with added columns for current price and expiry.
    """
    # Create a Ticker object
    ticker = yf.Ticker(ticker_symbol)

    # Get the current stock price from the latest trading day
    current_price = ticker.history(period="1d")['Close'].iloc[-1]

    # Get the list of available option expiration dates and choose the nearest one
    expiration_dates = ticker.options
    if not expiration_dates:
        raise ValueError(f"No options data available for {ticker_symbol}")
    nearest_expiry = expiration_dates[0]

    # Fetch option chain for calls from the nearest expiration date
    options_chain = ticker.option_chain(nearest_expiry)
    calls = options_chain.calls

    # Add extra columns for reference
    calls['currentPrice'] = current_price
    calls['expiry'] = nearest_expiry

    return calls
