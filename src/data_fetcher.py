import yfinance as yf
import pandas as pd
import os


class DataFetcher:
    """
    Fetches historical market data from Yahoo Finance.
    """

    def __init__(self, save_dir="data/raw"):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def get_historical_data(self, symbol, start, end, interval="1d"):
        """
        Download historical OHLCV data for a given symbol.
        """
        print(f"Fetching data for {symbol} from {start} to {end}...")

        # Download data
        df = yf.download(symbol, start=start, end=end, interval=interval)

        if df.empty:
            raise ValueError(f"No data fetched for {symbol}. Check the symbol and dates.")

        # Fix column names - handle newer yfinance tuple format
        new_columns = []
        for col in df.columns:
            if isinstance(col, tuple):
                new_columns.append(col[0].lower())
            else:
                new_columns.append(col.lower())
        df.columns = new_columns

        # Save raw data
        filename = f"{symbol.replace('-', '_')}_{start}_{end}.csv"
        filepath = os.path.join(self.save_dir, filename)
        df.to_csv(filepath)
        print(f"Data saved to {filepath}")

        print(f"Downloaded {len(df)} rows of data")
        return df

    def get_multiple_symbols(self, symbols, start, end, interval="1d"):
        """
        Fetch data for multiple symbols.
        """
        data_dict = {}
        for symbol in symbols:
            try:
                data_dict[symbol] = self.get_historical_data(symbol, start, end, interval)
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
        return data_dict


# ========== TEST CODE ==========
if __name__ == "__main__":
    fetcher = DataFetcher()

    # Test with Apple stock
    data = fetcher.get_historical_data(
        symbol="AAPL",
        start="2023-01-01",
        end="2023-12-31"
    )

    print("\n--- First 5 rows ---")
    print(data.head())

    print("\n--- Last 5 rows ---")
    print(data.tail())

    print(f"\nColumns: {list(data.columns)}")