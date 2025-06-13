"""
Module: strategy
Purpose: To define the covered call selection rules.
"""

import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
from .risk_model import estimate_delta


def select_low_risk_calls(options_df, max_contracts=2, target_probability=0.90):
    """
    Select the safest covered call with specific criteria:
    - High probability of expiring OTM (90%)
    - Avoid earnings dates
    - Limited by number of contracts
    - Weekly options preferred

    Args:
        options_df (DataFrame): Options chain data
        max_contracts (int): Maximum number of contracts (based on shares owned)
        target_probability (float): Desired probability of profit
    """
    # Get current price and next earnings date
    ticker = yf.Ticker("TSLA")
    current_price = options_df['currentPrice'].iloc[0]

    try:
        next_earnings = pd.to_datetime(ticker.calendar.iloc[0]['Earnings Date'])
        earnings_buffer = timedelta(days=5)  # Avoid options expiring near earnings
    except:
        next_earnings = None

    # Filter options
    filtered = options_df[
        (options_df['openInterest'] > 1000) &  # Ensure liquidity
        (options_df['strike'] > current_price)  # OTM calls only
    ].copy()

    # Calculate probability of profit (1 - delta)
    filtered['prob_profit'] = filtered.apply(
        lambda row: 1 - estimate_delta(
            current_price,
            row['strike'],
            (pd.to_datetime(row['expiry']) - pd.Timestamp.now()).days / 365,
            0.05,  # Risk-free rate
            row['impliedVolatility']
        ),
        axis=1
    )

    # Avoid earnings dates
    if next_earnings is not None:
        filtered = filtered[
            abs(pd.to_datetime(filtered['expiry']) - next_earnings) > earnings_buffer
        ]

    # Select options meeting probability target
    candidates = filtered[
        (filtered['prob_profit'] >= target_probability)
    ].sort_values('openInterest', ascending=False)

    # Calculate expected profit after fees
    fee_per_contract = 0.65
    candidates['net_premium'] = candidates['lastPrice'] * 100 - fee_per_contract

    # Return best candidate(s) up to max_contracts
    return candidates.head(max_contracts)


# Alias for clarity if you want to extend further risk filtering later
select_covered_calls = select_low_risk_calls
"""
Module: strategy
Purpose: To define the covered call selection rules.
"""

import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
from .risk_model import estimate_delta


def select_low_risk_calls(options_df, max_contracts=2, target_probability=0.90):
    """
    Select the safest covered call with specific criteria:
    - High probability of expiring OTM (90%)
    - Avoid earnings dates
    - Limited by number of contracts
    - Weekly options preferred

    Args:
        options_df (DataFrame): Options chain data
        max_contracts (int): Maximum number of contracts (based on shares owned)
        target_probability (float): Desired probability of profit
    """
    # Get current price and next earnings date
    ticker = yf.Ticker("TSLA")
    current_price = options_df['currentPrice'].iloc[0]

    try:
        next_earnings = pd.to_datetime(ticker.calendar.iloc[0]['Earnings Date'])
        earnings_buffer = timedelta(days=5)  # Avoid options expiring near earnings
    except:
        next_earnings = None

    # Filter options with basic criteria first
    filtered = options_df[
        (options_df['openInterest'] > 1000) &  # Ensure liquidity
        (options_df['strike'] > current_price)  # OTM calls only
        ].copy()

    # Data validation and cleaning
    current_time = pd.Timestamp.now()
    filtered['expiry_datetime'] = pd.to_datetime(filtered['expiry'])

    # Remove expired options and calculate time to expiry
    filtered = filtered[filtered['expiry_datetime'] > current_time]
    filtered['time_to_expiry'] = (filtered['expiry_datetime'] - current_time).dt.total_seconds() / (365.25 * 24 * 3600)

    # Ensure minimum time to expiry (at least 1 day)
    filtered = filtered[filtered['time_to_expiry'] >= (1/365.25)]

    # Clean implied volatility data
    filtered = filtered[
        (filtered['impliedVolatility'] > 0) &
        (filtered['impliedVolatility'] < 5.0) &  # Remove unrealistic volatility values
        (filtered['impliedVolatility'].notna())
        ]

    if filtered.empty:
        return pd.DataFrame()

    # Calculate probability of profit (1 - delta) with error handling
    def safe_calculate_prob_profit(row):
        try:
            delta = estimate_delta(
                current_price,
                row['strike'],
                row['time_to_expiry'],
                0.05,  # Risk-free rate
                row['impliedVolatility']
            )
            return 1 - delta
        except (ValueError, ZeroDivisionError, OverflowError):
            return 0.0  # Return 0 probability if calculation fails

    filtered['prob_profit'] = filtered.apply(safe_calculate_prob_profit, axis=1)

    # Remove rows where probability calculation failed
    filtered = filtered[filtered['prob_profit'] > 0]

    # Avoid earnings dates
    if next_earnings is not None:
        filtered = filtered[
            abs(filtered['expiry_datetime'] - next_earnings) > earnings_buffer
            ]

    # Select options meeting probability target
    candidates = filtered[
        (filtered['prob_profit'] >= target_probability)
    ].sort_values('openInterest', ascending=False)

    # Calculate expected profit after fees
    fee_per_contract = 0.65
    candidates['net_premium'] = candidates['lastPrice'] * 100 - fee_per_contract

    # Return best candidate(s) up to max_contracts
    return candidates.head(max_contracts)


# Alias for clarity if you want to extend further risk filtering later
select_covered_calls = select_low_risk_calls