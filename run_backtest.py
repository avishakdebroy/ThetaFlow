from thetaflow.backtest import CoveredCallBacktest

def main():
    # Initialize backtest
    backtest = CoveredCallBacktest(
        symbol="TSLA",
        start_date="2020-01-01",
        end_date="2025-01-01"
    )
    
    # Run simulation
    results = backtest.run(initial_shares=200)
    
    # Display results
    print("\n=== ThetaFlow Backtest Results ===")
    print(f"Period: 2020-2025")
    print(f"Total Trades: {len(results)}")
    
    if not results.empty:
        print(f"Win Rate: {results['win_rate'].mean():.2%}")
        print(f"Total Premium Collected: ${results['premium'].sum():.2f}")
        print(f"Net Profit (after fees): ${results['net_profit'].sum():.2f}")
        print("\nTrade Details:")
        print(results[['date', 'strike', 'premium', 'success']].head())
    else:
        print("No trades were executed during the backtest period")

if __name__ == "__main__":
    main()