import pytest
import numpy as np
from thetaflow.risk_model import estimate_delta

def test_at_the_money_call_delta():
    """Test that ATM call options have delta close to 0.5"""
    delta = estimate_delta(
        price=100.0,
        strike=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.05,
        implied_volatility=0.2
    )
    assert 0.45 <= delta <= 0.55

def test_deep_itm_call_delta():
    """Test that deep ITM calls have delta close to 1"""
    delta = estimate_delta(
        price=150.0,
        strike=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.05,
        implied_volatility=0.2
    )
    assert delta > 0.9

def test_deep_otm_call_delta():
    """Test that deep OTM calls have delta close to 0"""
    delta = estimate_delta(
        price=50.0,
        strike=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.05,
        implied_volatility=0.2
    )
    assert delta < 0.1

def test_invalid_inputs():
    """Test that invalid inputs raise ValueError"""
    with pytest.raises(ValueError):
        estimate_delta(
            price=-100.0,
            strike=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.05,
            implied_volatility=0.2
        )

def test_zero_time_to_expiry():
    """Test handling of zero time to expiry"""
    with pytest.raises(ValueError):
        estimate_delta(
            price=100.0,
            strike=100.0,
            time_to_expiry=0,
            risk_free_rate=0.05,
            implied_volatility=0.2
        )