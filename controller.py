import datetime
import pandas as pd
from publisher import Publisher

class DataController(Publisher):
    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model
        self.subscribe(view)  # Subscribe the view to updates

        # Descriptions for symbols
        self.descriptions = {
            "SOXL": "SOXL is a leveraged ETF that aims to provide three times the daily performance of the semiconductor sector.",
            "SOXS": "SOXS is a leveraged ETF that aims to provide three times the inverse daily performance of the semiconductor sector."
        }

    def on_plot(self):
        selected_symbols = []
        if self.view.soxl_var.get():
            selected_symbols.append("SOXL")
        if self.view.soxs_var.get():
            selected_symbols.append("SOXS")

        if not selected_symbols:
            self.view.error_label.config(text="Please select at least one symbol.")
            return

        start_year = int(self.view.start_year_var.get())
        start_month = int(self.view.start_month_var.get())
        start_day = int(self.view.start_day_var.get())

        end_year = int(self.view.end_year_var.get())
        end_month = int(self.view.end_month_var.get())
        end_day = int(self.view.end_day_var.get())

        start_date = datetime.date(start_year, start_month, start_day)
        end_date = datetime.date(end_year, end_month, end_day)

        if not start_date or not end_date:
            self.view.error_label.config(text="Please fill out all fields.")
            return

        # Convert the dates from datetime.date to pandas.Timestamp
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)

        # Validate that the start date is before or equal to the end date
        if start_date > end_date:
            self.view.error_label.config(text="Start date must be before or equal to end date.")
            return

        for symbol in selected_symbols:
            data = self.model.fetch_data(symbol, start_date, end_date)
            description = self.descriptions.get(symbol, "")

            # Find the closest available dates to start_date and end_date
            closest_start_date = data['Date'].iloc[(data['Date'] - start_date).abs().argsort()[:1]].values[0]
            closest_end_date = data['Date'].iloc[(data['Date'] - end_date).abs().argsort()[:1]].values[0]

            start_price = data[data['Date'] == closest_start_date]['Close'].values[0]
            end_price = data[data['Date'] == closest_end_date]['Close'].values[0]
            percent_diff = ((end_price - start_price) / start_price) * 100

            self.notify({'symbols': [symbol], 'data': data, 'description': description, 'percent_diff': percent_diff})

    def on_trade(self, short_window, long_window):
        selected_symbols = []
        if self.view.soxl_var.get():
            selected_symbols.append("SOXL")
        if self.view.soxs_var.get():
            selected_symbols.append("SOXS")

        if not selected_symbols:
            self.view.error_label.config(text="Please select at least one symbol.")
            return

        for symbol in selected_symbols:
            data, trades, final_balance = self.model.execute_trading_strategy(symbol, short_window, long_window)
            description = self.descriptions.get(symbol, "")
            self.notify({'symbols': [symbol], 'data': data, 'trades': trades, 'final_balance': final_balance, 'description': description})
