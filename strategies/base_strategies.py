import pandas as pd


class BaseStrategies:
    """
    Collection of predefined trading strategies.
    Each returns a pandas Series of signals: 1 (buy), -1 (sell), 0 (hold).
    """

    @staticmethod
    def get_all():
        """Return list of (name, signal_function) tuples."""
        return [
            ("macd_crossover", BaseStrategies.macd_crossover),
            ("rsi_oversold_overbought", BaseStrategies.rsi_oversold_overbought),
            ("sma_crossover", BaseStrategies.sma_crossover),
            ("bollinger_breakout", BaseStrategies.bollinger_breakout),
            ("ema_crossover", BaseStrategies.ema_crossover),
        ]

    @staticmethod
    def macd_crossover(df):
        """Buy when MACD crosses above Signal line, sell when below."""
        signal = pd.Series(0, index=df.index)
        signal[df["macd"] > df["macd_signal"]] = 1
        signal[df["macd"] < df["macd_signal"]] = -1
        return signal

    @staticmethod
    def rsi_oversold_overbought(df):
        """Buy when RSI < 30, sell when RSI > 70."""
        signal = pd.Series(0, index=df.index)
        signal[df["rsi"] < 30] = 1
        signal[df["rsi"] > 70] = -1
        return signal

    @staticmethod
    def sma_crossover(df):
        """Buy when SMA20 > SMA50, sell when SMA20 < SMA50."""
        signal = pd.Series(0, index=df.index)
        signal[df["sma_20"] > df["sma_50"]] = 1
        signal[df["sma_20"] < df["sma_50"]] = -1
        return signal

    @staticmethod
    def bollinger_breakout(df):
        """Buy when close > upper band, sell when close < lower band."""
        signal = pd.Series(0, index=df.index)
        signal[df["close"] > df["bb_high"]] = 1
        signal[df["close"] < df["bb_low"]] = -1
        return signal

    @staticmethod
    def ema_crossover(df):
        """Buy when EMA12 > EMA26, sell when EMA12 < EMA26."""
        signal = pd.Series(0, index=df.index)
        signal[df["ema_12"] > df["ema_26"]] = 1
        signal[df["ema_12"] < df["ema_26"]] = -1
        return signal


# ========== TEST ==========
if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from src.data_fetcher import DataFetcher
    from src.indicators import TechnicalIndicators

    # Fetch and prepare
    fetcher = DataFetcher()
    df = fetcher.get_historical_data("AAPL", "2023-01-03", "2023-12-31")
    df = TechnicalIndicators.add_all_indicators(df)

    strategies = BaseStrategies.get_all()
    print("Available strategies:")
    for name, func in strategies:
        sig = func(df)
        print(f"{name}: {sig.value_counts().to_dict()}")