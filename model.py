import pandas as pd
from adapter_mvc import StockDataAdapter

class DataHandler:
    def __init__(self):
        self.adapter = StockDataAdapter()

    def load_data(self, symbol):
        filename = f'{symbol}_data.json'
        try:
            data = pd.read_json(filename)
            return data
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return None

    def fetch_data(self, symbol, start_date, end_date):
        data = self.load_data(symbol)
        if data is not None:
            data['Date'] = pd.to_datetime(data['Date'])
            mask = (data['Date'] >= start_date) & (data['Date'] <= end_date)
            filtered_data = data.loc[mask]
            if filtered_data.empty:
                print("Data is not available for the given date range locally. Fetching from Yahoo Finance.")
                data = self.adapter.fetch_and_save_data(symbol, start_date, end_date)
                filtered_data = data.loc[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
            return filtered_data
        else:
            print("Data not available locally. Fetching from Yahoo Finance.")
            data = self.adapter.fetch_and_save_data(symbol, start_date, end_date)
            filtered_data = data.loc[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
            return filtered_data

    def calculate_sma(self, data, window):
        return data['Close'].rolling(window=window).mean()

    def execute_trading_strategy(self, symbol, short_window, long_window, initial_balance=100000):
        data = self.load_data(symbol)
        if data is not None:
            data['SMA_short'] = self.calculate_sma(data, short_window)
            data['SMA_long'] = self.calculate_sma(data, long_window)
            data.loc[data.index[short_window:], 'Signal'] = (data.loc[data.index[short_window:], 'SMA_short'] > data.loc[data.index[short_window:], 'SMA_long']).astype(int)
            data['Position'] = data['Signal'].diff()

            trades = []
            position = 0
            balance = initial_balance
            portfolio_value = []

            for index, row in data.iterrows():
                if row['Position'] == 1:  # Buy signal
                    if position == 0:  # Only buy if we are not already in a position
                        position = balance / row['Close']
                        balance = 0
                        trades.append((row['Date'], symbol, 'Buy', row['Close'], position))
                elif row['Position'] == -1:  # Sell signal
                    if position > 0:  # Only sell if we are in a position
                        balance = position * row['Close']
                        position = 0
                        trades.append((row['Date'], symbol, 'Sell', row['Close'], balance))
                
                # Calculate portfolio value
                portfolio_value.append(balance + (position * row['Close']))

            data['Portfolio Value'] = portfolio_value
            return data, trades, balance
        return None, [], initial_balance

# Example usage in the main application
if __name__ == "__main__":
    model = DataHandler()
    data, trades, final_balance = model.execute_trading_strategy('SOXL', short_window=40, long_window=100)
    for trade in trades:
        print(trade)
    print("Final Portfolio Value:", final_balance)
