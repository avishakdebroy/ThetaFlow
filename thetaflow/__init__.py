"""
ThetaFlow Package Initialization

This file initializes the thetaflow package by importing key modules
used throughout the project. This makes it easier to access functions
directly from the package. For example:

    from thetaflow import get_options_data, select_covered_calls, setup_logging

Modules Imported:
- data_fetch: Contains functions to retrieve live options data using yfinance.
- strategy: Hosts the logic to filter and select low-risk covered call candidates.
- risk_model: (Placeholder for future development) Contains risk calculation functions.
- utils: Provides utility functions like logging setup and helper methods.
"""

from .data_fetch import get_options_data
from .strategy import select_covered_calls, select_low_risk_calls
from .risk_model import estimate_delta
from .utils import setup_logging, log_message
from .backtest import CoveredCallBacktest 
