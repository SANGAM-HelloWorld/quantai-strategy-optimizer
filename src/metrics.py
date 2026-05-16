import numpy as np
import pandas as pd


class MetricsCalculator:
    """Calculates performance metrics from backtest results."""

    @staticmethod
    def compute(equity_curve, strategy_returns, initial_capital, strategy_name):
        """Return a dict of metrics."""
        if len(strategy_returns.dropna()) < 2:
            return {
                "strategy": strategy_name,
                "total_return": 0,
                "win_rate": 0,
                "max_drawdown": 0,
                "sharpe_ratio": 0,
            }

        final_equity = equity_curve.dropna().iloc[-1]
        total_return = (final_equity - initial_capital) / initial_capital

        # Win rate on days where a position was held
        trading_days = strategy_returns[strategy_returns != 0]
        if len(trading_days) > 0:
            win_rate = (trading_days > 0).sum() / len(trading_days)
        else:
            win_rate = 0

        # Max drawdown
        rolling_max = equity_curve.cummax()
        drawdown = (equity_curve - rolling_max) / rolling_max
        max_drawdown = drawdown.min()

        # Sharpe ratio (annualized)
        if strategy_returns.std() != 0:
            sharpe = np.sqrt(252) * strategy_returns.mean() / strategy_returns.std()
        else:
            sharpe = 0

        return {
            "strategy": strategy_name,
            "total_return": total_return,
            "win_rate": win_rate,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe,
        }