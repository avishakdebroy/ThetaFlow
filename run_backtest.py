"""
run_backtest.py
Simple script to run the ThetaFlow backtest
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from thetaflow.backtest import ThetaFlowBacktester
from thetaflow.utils import setup_logging
import pandas as pd


def main():
    # Setup logging
    setup_logging()

    print("=== ThetaFlow Backtesting System ===")

    # Create and run backtester
    backtester = ThetaFlowBacktester(
        ticker="TSLA",
        start_date="2023-01-01",  # Shorter period for faster testing
        end_date="2024-12-31"
    )

    try:
        # Run the backtest
        backtester.run_backtest()

        # Get and print results
        portfolio_df, trades_df = backtester.print_results()

        # Save results if we have trades
        if not trades_df.empty:
            # Ensure data directory exists
            os.makedirs('data', exist_ok=True)

            # Save to CSV
            trades_df.to_csv('data/backtest_trades.csv', index=False)
            portfolio_df.to_csv('data/backtest_portfolio.csv')

            print(f"\nResults saved to:")
            print(f"- data/backtest_trades.csv ({len(trades_df)} trades)")
            print(f"- data/backtest_portfolio.csv ({len(portfolio_df)} days)")

            # Try to create a simple performance chart
            try:
                import matplotlib.pyplot as plt

                plt.figure(figsize=(12, 6))
                plt.subplot(1, 2, 1)
                plt.plot(portfolio_df.index, portfolio_df['total_value'])
                plt.title('Portfolio Value Over Time')
                plt.xlabel('Date')
                plt.ylabel('Portfolio Value ($)')
                plt.xticks(rotation=45)
                plt.grid(True, alpha=0.3)

                plt.subplot(1, 2, 2)
                plt.plot(portfolio_df.index, portfolio_df['stock_price'])
                plt.title('TSLA Stock Price')
                plt.xlabel('Date')
                plt.ylabel('Stock Price ($)')
                plt.xticks(rotation=45)
                plt.grid(True, alpha=0.3)

                plt.tight_layout()
                plt.savefig('data/backtest_performance.png', dpi=300, bbox_inches='tight')
                print(f"- data/backtest_performance.png (performance chart)")

            except ImportError:
                print("matplotlib not available - skipping chart generation")
                print("Install with: pip install matplotlib")
            except Exception as e:
                print(f"Error creating chart: {e}")

        else:
            print("\nNo trades were executed. Troubleshooting info:")
            print("1. The moneyness buffer (1.05) might be too restrictive")
            print("2. Simulated options data might not meet selection criteria")
            print("3. Insufficient capital for trades")

            # Diagnostic information
            print(f"\nDiagnostic Info:")
            print(f"- Initial Capital: ${backtester.initial_capital:,}")
            print(f"- Final Capital: ${backtester.current_capital:,}")
            print(f"- Stock Position: {backtester.stock_position} shares")
            print(f"- Option Positions: {len(backtester.option_positions)}")

            # Show portfolio tracking
            if backtester.portfolio_value:
                portfolio_df = pd.DataFrame(backtester.portfolio_value)
                print(f"- Portfolio tracking: {len(portfolio_df)} days")
                print(
                    f"- TSLA price range: ${portfolio_df['stock_price'].min():.2f} - ${portfolio_df['stock_price'].max():.2f}")

    except Exception as e:
        print(f"Error running backtest: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()