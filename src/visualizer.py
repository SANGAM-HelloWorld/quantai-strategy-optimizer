import matplotlib.pyplot as plt
import pandas as pd
import os


class Visualizer:
    """Plots backtest results and saves charts."""

    def __init__(self, save_dir="results/charts"):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def plot_equity_curves(self, results, show=True):
        """Plot equity curves for multiple strategies."""
        plt.figure(figsize=(12, 6))
        for res in results:
            plt.plot(res["equity_curve"], label=res["strategy"])
        plt.title("Equity Curves")
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value")
        plt.legend()
        plt.grid(True)
        if show:
            plt.show()
        plt.savefig(os.path.join(self.save_dir, "equity_curves.png"))
        plt.close()

    def plot_performance_comparison(self, results, show=True):
        """Bar charts comparing key metrics across strategies."""
        metrics_df = pd.DataFrame([r["metrics"] for r in results])
        metrics_df.set_index("strategy", inplace=True)

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        metrics_df["total_return"].plot(
            kind="bar", ax=axes[0, 0], title="Total Return", color="skyblue"
        )
        axes[0, 0].set_ylabel("Return %")

        metrics_df["win_rate"].plot(
            kind="bar", ax=axes[0, 1], title="Win Rate", color="lightgreen"
        )
        axes[0, 1].set_ylabel("Win Rate %")

        metrics_df["max_drawdown"].plot(
            kind="bar", ax=axes[1, 0], title="Max Drawdown", color="salmon"
        )
        axes[1, 0].set_ylabel("Drawdown %")

        metrics_df["sharpe_ratio"].plot(
            kind="bar", ax=axes[1, 1], title="Sharpe Ratio", color="gold"
        )
        axes[1, 1].set_ylabel("Sharpe Ratio")

        plt.tight_layout()
        if show:
            plt.show()
        plt.savefig(os.path.join(self.save_dir, "performance_comparison.png"))
        plt.close()
        return metrics_df