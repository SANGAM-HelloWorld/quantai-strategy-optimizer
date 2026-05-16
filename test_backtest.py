import sys
sys.path.insert(0, ".")
from src.data_fetcher import DataFetcher
from src.indicators import TechnicalIndicators
from src.strategy_generator import StrategyGenerator
from src.backtester import Backtester

# 1. Get data with indicators
fetcher = DataFetcher()
data = fetcher.get_historical_data("AAPL", "2023-01-03", "2023-12-31")
data = TechnicalIndicators.add_all_indicators(data)

# 2. Generate strategies
strategies = StrategyGenerator.generate_all_strategies()

# 3. Backtest
backtester = Backtester(data, initial_capital=10000)
results = backtester.test_strategies(strategies)

# 4. Print results
print("\n========== BACKTEST RESULTS ==========")
for r in results:
    m = r["metrics"]
    print(f"\n{m['strategy']}:")
    print(f"  Total Return : {m['total_return']:.2%}")
    print(f"  Win Rate     : {m['win_rate']:.2%}")
    print(f"  Max Drawdown : {m['max_drawdown']:.2%}")
    print(f"  Sharpe Ratio : {m['sharpe_ratio']:.2f}")
    print(f"  Trades       : {r['trades']:.0f}")