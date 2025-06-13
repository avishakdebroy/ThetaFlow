"""
ThetaFlow – Income Generation via Options Time Decay
Entry point: Fetch TSLA options data and identify viable covered call candidates.
"""

from thetaflow import data_fetch, strategy, utils


def main():
    utils.setup_logging()
    print("=== ThetaFlow: TSLA Covered Call Strategy ===")

    options_data = data_fetch.get_options_data("TSLA")
    selected_calls = strategy.select_low_risk_calls(
        options_data, 
        max_contracts=2,  # Based on owning 200 shares
        target_probability=0.90
    )

    if not selected_calls.empty:
        print("\nSelected Covered Call Opportunities:")
        print("(Filtered for 90% probability OTM, avoiding earnings)")
        display_cols = [
            'contractSymbol', 'strike', 'lastPrice', 
            'prob_profit', 'net_premium', 'expiry'
        ]
        print(selected_calls[display_cols].to_string(index=False))
    else:
        print("No suitable options found matching criteria")

    utils.log_message("Strategy execution completed")


if __name__ == "__main__":
    main()