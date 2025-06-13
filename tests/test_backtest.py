import pytest
from thetaflow.backtest import ThetaFlowBacktester

def test_backtest_initialization():
    """Test backtest object creation"""
    bt = ThetaFlowBacktester(
        ticker="TSLA",
        start_date="2020-01-01",
        end_date="2025-01-01"
    )
    assert bt.ticker == "TSLA"
    # Initial capital should be 100000
    assert bt.initial_capital == 100000
