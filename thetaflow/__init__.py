"""
ThetaFlow Package Initialization

This file initializes the thetaflow package by importing key modules
used throughout the project. This makes it easier to access functions
directly from the package. For example:

    from thetaflow import get_options_data, select_covered_calls, setup_logging

Modules Imported:
- data_fetch: Contains functions to retrieve live options data using yfinance.
- strategy: Hosts the logic to filter and select low-risk covered call candidates.
- risk_model: Contains risk calculation functions using Black-Scholes model.
- utils: Provides utility functions like logging setup and helper methods.
- backtest: Contains the backtesting framework for strategy evaluation.
"""

from .data_fetch import get_options_data
from .strategy import select_covered_calls, select_low_risk_calls
from .risk_model import estimate_delta
from .utils import setup_logging, log_message

# Import backtest module conditionally to avoid circular imports
try:
    from .backtest import ThetaFlowBacktester
except ImportError:
    # Backtest module might not be available in all environments
    ThetaFlowBacktester = None