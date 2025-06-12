"""
Module: risk_model
Purpose: Contains functions for calculating risk metrics using Black-Scholes model.

Black-Scholes Model Assumptions:
1. The stock follows a lognormal random walk (Geometric Brownian Motion)
2. No dividends are paid during the option's life
3. Markets are efficient (no arbitrage)
4. No transaction costs or taxes
5. Risk-free rate is constant
6. All securities are perfectly divisible
7. European-style options (no early exercise)
"""

import numpy as np
from scipy.stats import norm


def estimate_delta(price, strike, time_to_expiry, risk_free_rate, implied_volatility):
    """
    Calculate the option's delta using the Black-Scholes model.

    Args:
        price (float): Current stock price
        strike (float): Option strike price
        time_to_expiry (float): Time to expiration in years
        risk_free_rate (float): Annualized risk-free interest rate (decimal)
        implied_volatility (float): Option implied volatility (decimal)

    Returns:
        float: Delta value between 0 and 1 for calls

    Raises:
        ValueError: If inputs are invalid (negative or zero values)
    """
    # Input validation
    if price <= 0 or strike <= 0 or time_to_expiry <= 0 or implied_volatility <= 0:
        raise ValueError("Price, strike, time to expiry, and volatility must be positive")

    try:
        # Calculate d1 from Black-Scholes formula
        d1 = (np.log(price / strike) +
              (risk_free_rate + implied_volatility**2 / 2) * time_to_expiry) / \
             (implied_volatility * np.sqrt(time_to_expiry))

        # Delta for a call option is N(d1)
        call_delta = norm.cdf(d1)

        return round(call_delta, 4)

    except Exception as e:
        raise ValueError(f"Error calculating delta: {str(e)}")
