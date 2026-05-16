import pandas as pd
import numpy as np
from src.metrics import MetricsCalculator


class Backtester:
    """
    Simulates trading based on strategy signals.
    """

    def __init__(self, data, initial_capital=10000, commission=0.001, slippage=0.0005):
        self.data = data
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage

    def run(self, strategy):
        """
        Run backtest for a single strategy dict {name, signal_func}.
        Returns a dict with results.
        """
        df = self.data.copy()
        # 1. Get signals
        df["signal"] = strategy["signal_func"](df)

        # 2. Position: carry forward last signal, fill gaps with 0
        df["position"] = df["signal"].replace(0, np.nan).ffill().fillna(0)
        df["position"] = df["position"].clip(-1, 1)  # only long/short for simplicity

        # 3. Daily returns of the asset
        df["asset_returns"] = df["close"].pct_change()

        # 4. Strategy returns = yesterday's position × today's return
        df["strategy_returns"] = df["position"].shift(1) * df["asset_returns"]

        # 5. Transaction costs on position changes
        df["trade"] = df["position"].diff().abs()
        df["strategy_returns"] -= df["trade"] * self.commission
        df["strategy_returns"] -= df["trade"] * self.slippage

        # 6. Equity curve
        df["equity_curve"] = (1 + df["strategy_returns"]).cumprod() * self.initial_capital

        # 7. Metrics
        metrics = MetricsCalculator.compute(
            df["equity_curve"],
            df["strategy_returns"],
            self.initial_capital,
            strategy["name"],
        )

        return {
            "strategy": strategy["name"],
            "metrics": metrics,
            "equity_curve": df["equity_curve"],
            "returns": df["strategy_returns"],
            "trades": df["trade"].sum(),
        }

    def test_strategies(self, strategies):
        """Run backtest on a list of strategies, return list of results."""
        results = []
        for strat in strategies:
            res = self.run(strat)
            results.append(res)
        return results