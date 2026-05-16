import argparse
from src.data_fetcher import DataFetcher
from src.indicators import TechnicalIndicators
from src.strategy_generator import StrategyGenerator
from src.backtester import Backtester
from src.visualizer import Visualizer


def main():
    parser = argparse.ArgumentParser(description="QuantAI Strategy Optimizer")
    parser.add_argument(
        "--symbol", type=str, required=True, help="Ticker symbol (e.g., AAPL, MSFT, BTC-USD)"
    )
    parser.add_argument(
        "--start", type=str, default="2020-01-01", help="Start date YYYY-MM-DD"
    )
    parser.add_argument(
        "--end", type=str, default="2024-01-01", help="End date YYYY-MM-DD"
    )
    parser.add_argument(
        "--strategy",
        type=str,
        help="Single strategy to test (macd_crossover, rsi_oversold_overbought, etc.)",
    )
    parser.add_argument(
        "--compare-all", action="store_true", help="Compare all predefined strategies"
    )
    parser.add_argument(
        "--top", type=int, default=5, help="Number of top strategies to show (by Sharpe)"
    )
    args = parser.parse_args()

    # Fetch data and add indicators
    print(f"\nFetching data for {args.symbol} from {args.start} to {args.end}...")
    fetcher = DataFetcher()
    data = fetcher.get_historical_data(args.symbol, args.start, args.end)
    data = TechnicalIndicators.add_all_indicators(data)

    # Generate strategies
    all_strategies = StrategyGenerator.generate_all_strategies()

    # Select which strategies to run
    if args.strategy:
        selected = [s for s in all_strategies if s["name"] == args.strategy]
        if not selected:
            print(f"Strategy '{args.strategy}' not found.")
            print(f"Available: {[s['name'] for s in all_strategies]}")
            return
        strategies_to_test = selected
    elif args.compare_all:
        strategies_to_test = all_strategies
    else:
        # Default: test the first strategy
        strategies_to_test = [all_strategies[0]]

    # Backtest
    print(f"Running backtests on {len(strategies_to_test)} strategy(ies)...")
    backtester = Backtester(data, initial_capital=10000)
    results = backtester.test_strategies(strategies_to_test)

    # Print summary
    print("\n========== BACKTEST RESULTS ==========")
    for r in results:
        m = r["metrics"]
        print(f"\n{m['strategy']}:")
        print(f"  Total Return : {m['total_return']:.2%}")
        print(f"  Win Rate     : {m['win_rate']:.2%}")
        print(f"  Max Drawdown : {m['max_drawdown']:.2%}")
        print(f"  Sharpe Ratio : {m['sharpe_ratio']:.2f}")
        print(f"  Trades       : {r['trades']:.0f}")

    # Show top strategies if comparing all
    if args.compare_all and args.top > 0:
        sorted_results = sorted(
            results, key=lambda x: x["metrics"]["sharpe_ratio"], reverse=True
        )[: args.top]
        print(f"\nTop {args.top} strategies by Sharpe Ratio:")
        for r in sorted_results:
            print(f"  {r['metrics']['strategy']}: Sharpe = {r['metrics']['sharpe_ratio']:.2f}")

    # Visualize
    viz = Visualizer()
    if len(results) > 1:
        viz.plot_performance_comparison(results)
    viz.plot_equity_curves(results)
    print("\nCharts saved to results/charts/")


if __name__ == "__main__":
    main()