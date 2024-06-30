import yfinance as yf
import pandas as pd

class StockDataAdapter:
    def download_data(self, symbol, start_date, end_date):
        data = yf.download(symbol, start=start_date, end=end_date)
        if not data.empty:
            data.reset_index(inplace=True)
            data['Date'] = pd.to_datetime(data['Date'])
            return data
        else:
            return None

    def save_data(self, symbol, data):
        filename = f'{symbol}_data.json'
        data.to_json(filename, date_format='iso')

    def fetch_and_save_data(self, symbol, start_date, end_date):
        data = self.download_data(symbol, start_date, end_date)
        if data is not None:
            self.save_data(symbol, data)
        return data
