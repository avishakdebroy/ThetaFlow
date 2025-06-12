import pytest
from thetaflow.backtest import CoveredCallBacktest

def test_backtest_initialization():
    """Test backtest object creation"""
    bt = CoveredCallBacktest(
        symbol="TSLA",
        start_date="2020-01-01",
        end_date="2025-01-01"
    )
    assert bt.symbol == "TSLA"
    assert bt.transaction_fee == 0.65