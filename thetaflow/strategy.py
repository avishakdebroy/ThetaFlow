"""
Module: strategy
Purpose: To define the covered call selection rules.
"""


def select_low_risk_calls(options_df, moneyness_buffer=1.05):
    """
    Filters call options to select low-risk, out-of-the-money (OTM) candidates for a covered call strategy.

    Args:
        options_df (DataFrame): Options chain data (calls).
        moneyness_buffer (float): Factor above the current price to define OTM (e.g., 1.05 means 5% above the spot price).

    Returns:
        DataFrame: Top candidate options sorted by open interest.
    """
    # Get the current TSLA price
    current_price = options_df['currentPrice'].iloc[0]

    # Filter for calls whose strike price is higher than the current price * moneyness_buffer
    filtered = options_df[options_df['strike'] > current_price * moneyness_buffer]

    # Sort by open interest (to ensure liquidity) in descending order
    filtered = filtered.sort_values(by='openInterest', ascending=False)

    # Return top 5 candidates; you can adjust this as desired.
    return filtered.head(5)


# Alias for clarity if you want to extend further risk filtering later
select_covered_calls = select_low_risk_calls
