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


def estimate_profit_probability(price, strike, time_to_expiry, risk_free_rate, implied_volatility):
    """Calculate probability of profit for a covered call"""
    delta = estimate_delta(price, strike, time_to_expiry, risk_free_rate, implied_volatility)
    return 1 - delta  # Probability it expires OTM
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
    # Enhanced input validation
    if not isinstance(price, (int, float)) or price <= 0:
        raise ValueError(f"Price must be a positive number, got: {price}")

    if not isinstance(strike, (int, float)) or strike <= 0:
        raise ValueError(f"Strike must be a positive number, got: {strike}")

    if not isinstance(time_to_expiry, (int, float)) or time_to_expiry <= 0:
        raise ValueError(f"Time to expiry must be positive, got: {time_to_expiry}")

    if not isinstance(implied_volatility, (int, float)) or implied_volatility <= 0:
        raise ValueError(f"Implied volatility must be positive, got: {implied_volatility}")

    if not isinstance(risk_free_rate, (int, float)):
        raise ValueError(f"Risk-free rate must be a number, got: {risk_free_rate}")

    # Additional validation for extreme values
    if implied_volatility > 10:  # 1000% volatility is unrealistic
        raise ValueError(f"Implied volatility too high: {implied_volatility}")

    if time_to_expiry > 10:  # More than 10 years is unrealistic for most options
        raise ValueError(f"Time to expiry too long: {time_to_expiry}")

    try:
        # Calculate d1 from Black-Scholes formula
        sqrt_time = np.sqrt(time_to_expiry)
        if sqrt_time == 0:
            raise ValueError("Time to expiry is too small")

        d1 = (np.log(price / strike) +
              (risk_free_rate + implied_volatility**2 / 2) * time_to_expiry) / \
             (implied_volatility * sqrt_time)

        # Check for overflow/underflow
        if np.isnan(d1) or np.isinf(d1):
            raise ValueError("Invalid d1 calculation result")

        # Delta for a call option is N(d1)
        call_delta = norm.cdf(d1)

        # Ensure result is within expected bounds
        if np.isnan(call_delta) or call_delta < 0 or call_delta > 1:
            raise ValueError("Invalid delta calculation result")

        return round(call_delta, 4)

    except Exception as e:
        raise ValueError(f"Error calculating delta: {str(e)}")


def estimate_profit_probability(price, strike, time_to_expiry, risk_free_rate, implied_volatility):
    """Calculate probability of profit for a covered call"""
    delta = estimate_delta(price, strike, time_to_expiry, risk_free_rate, implied_volatility)
    return 1 - delta  # Probability it expires OTM