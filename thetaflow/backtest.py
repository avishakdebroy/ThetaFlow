"""
Module: backtest
Purpose: Simulates the covered call strategy performance using historical data.
"""

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from .strategy import select_low_risk_calls


class CoveredCallBacktest:
    def __init__(self, symbol="TSLA", start_date=None, end_date=None):
        """Initialize backtesting parameters."""
        self.symbol = symbol

        # Default to last 90 days if no dates provided
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")

        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.transaction_fee = 0.65

    def run(self, initial_shares=200):
        """Run backtest simulation"""
        trades = []
        ticker = yf.Ticker(self.symbol)

        try:
            # Get historical data
            stock_data = yf.download(
                self.symbol,
                start=self.start_date.strftime("%Y-%m-%d"),
                end=self.end_date.strftime("%Y-%m-%d"),
                interval="1d",
            )

            if stock_data.empty:
                print(f"No historical data found for {self.symbol}")
                return pd.DataFrame()

            # Get available options expirations
            expiration_dates = ticker.options

            if not expiration_dates:
                print(f"No options data available for {self.symbol}")
                return pd.DataFrame()

            # Process each expiration date
            for expiry in expiration_dates:
                expiry_date = pd.to_datetime(expiry)

                # Skip if expiry is outside our range
                if not (self.start_date <= expiry_date <= self.end_date):
                    continue

                try:
                    # Get option chain
                    opt_chain = ticker.option_chain(expiry)
                    calls_df = pd.DataFrame(opt_chain.calls)

                    # Add current stock price
                    current_date = expiry_date - timedelta(days=1)  # Day before expiry
                    if current_date in stock_data.index:
                        current_price = stock_data.loc[current_date, "Close"]
                        calls_df["currentPrice"] = current_price
                        calls_df["expiry"] = expiry

                        # Apply strategy
                        selected = select_low_risk_calls(
                            calls_df,
                            max_contracts=initial_shares // 100,
                            target_probability=0.90,
                        )

                        if not selected.empty:
                            # Record trade
                            trade = {
                                "date": expiry,
                                "strike": selected["strike"].iloc[0],
                                "premium": selected["lastPrice"].iloc[0] * 100,
                                "success": stock_data["Close"].loc[expiry_date]
                                <= selected["strike"].iloc[0],
                                "net_profit": (selected["lastPrice"].iloc[0] * 100)
                                - self.transaction_fee,
                                "stock_price": stock_data["Close"].loc[expiry_date],
                            }
                            trades.append(trade)
                            print(f"Found trade for expiry {expiry}")  # Debug line

                except Exception as e:
                    print(f"Error processing expiry {expiry}: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error in backtest: {str(e)}")
            return pd.DataFrame()

        results = pd.DataFrame(trades)
        if not results.empty:
            results["win_rate"] = results["success"].astype(float)
            print(f"Successfully processed {len(results)} trades")  # Debug line

        return results