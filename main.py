"""
ThetaFlow – Income Generation via Options Time Decay
Entry point: Fetch TSLA options data and identify viable covered call candidates.
"""

from thetaflow import data_fetch, strategy, utils


def main():
    utils.setup_logging()
    print("=== ThetaFlow: TSLA Covered Call Strategy ===")

    # Fetch live options chain data for TSLA from yfinance
    options_data = data_fetch.get_options_data("TSLA")

    # Select candidate options for a low-risk covered call strategy.
    # We consider 'out-of-the-money' options (using a moneyness buffer) and sort by open interest.
    selected_calls = strategy.select_covered_calls(options_data, moneyness_buffer=1.05)

    # Show the key details of the selected options
    if not selected_calls.empty:
        print("Selected Covered Call Opportunities:")
        print(selected_calls[['contractSymbol', 'strike', 'lastPrice', 'impliedVolatility', 'openInterest']])
    else:
        print("No candidate options were found based on the current parameters.")

    # Log the event for audit / debugging purposes.
    utils.log_message("Fetched and processed TSLA options data.")


if __name__ == "__main__":
    main()
