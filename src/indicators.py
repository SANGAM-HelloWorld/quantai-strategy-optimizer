import pandas as pd
import ta


class TechnicalIndicators:
    """
    Adds popular technical indicators to market data.
    """

    @staticmethod
    def add_all_indicators(df):
        """
        Add RSI, MACD, SMA, EMA, Bollinger Bands to a DataFrame.
        Expects columns: 'close', 'high', 'low', 'open', 'volume'.
        Returns a new DataFrame with indicators (drops NaN rows).
        """
        df = df.copy()

        # --- RSI (14-day) ---
        df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()

        # --- MACD ---
        macd = ta.trend.MACD(df["close"])
        df["macd"] = macd.macd()
        df["macd_signal"] = macd.macd_signal()
        df["macd_diff"] = macd.macd_diff()

        # --- Simple Moving Averages (20 & 50) ---
        df["sma_20"] = ta.trend.SMAIndicator(df["close"], window=20).sma_indicator()
        df["sma_50"] = ta.trend.SMAIndicator(df["close"], window=50).sma_indicator()

        # --- Exponential Moving Averages (12 & 26) ---
        df["ema_12"] = ta.trend.EMAIndicator(df["close"], window=12).ema_indicator()
        df["ema_26"] = ta.trend.EMAIndicator(df["close"], window=26).ema_indicator()

        # --- Bollinger Bands (20-day, 2 std) ---
        bb = ta.volatility.BollingerBands(df["close"], window=20, window_dev=2)
        df["bb_high"] = bb.bollinger_hband()
        df["bb_low"] = bb.bollinger_lband()
        df["bb_mid"] = bb.bollinger_mavg()

        # Drop rows with NaN (from indicator warm-up periods)
        df.dropna(inplace=True)

        return df


# ========== TEST CODE ==========
if __name__ == "__main__":
    from data_fetcher import DataFetcher

    # Fetch some data
    fetcher = DataFetcher()
    data = fetcher.get_historical_data("AAPL", "2023-01-01", "2023-12-31")

    # Add indicators
    df = TechnicalIndicators.add_all_indicators(data)

    # Show a few columns
    print("\n--- Data with indicators (tail) ---")
    print(df[["close", "rsi", "macd", "sma_20", "bb_high", "bb_low"]].tail())

    print(f"\nNew columns: {list(df.columns)}")