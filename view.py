import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from subscriber import Subscriber

class DataView(Subscriber):
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("Stock Data Viewer")

        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.soxl_var = tk.BooleanVar()
        self.soxs_var = tk.BooleanVar()
        self.start_year_var = tk.StringVar()
        self.start_month_var = tk.StringVar()
        self.start_day_var = tk.StringVar()
        self.end_year_var = tk.StringVar()
        self.end_month_var = tk.StringVar()
        self.end_day_var = tk.StringVar()

        self.error_label = ttk.Label(self.frame, text="", foreground="red")
        self.error_label.grid(column=0, row=5, columnspan=7, sticky=(tk.W, tk.E), pady=10)

        self.description_label = ttk.Label(self.frame, text="", foreground="black")
        self.description_label.grid(column=0, row=6, columnspan=7, sticky=(tk.W, tk.E), pady=10)

        self.percent_diff_label = ttk.Label(self.frame, text="", foreground="black")
        self.percent_diff_label.grid(column=0, row=7, columnspan=7, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(self.frame, text="Select Symbols:").grid(column=0, row=0, sticky=tk.W, padx=5)
        soxl_check = ttk.Checkbutton(self.frame, text="SOXL", variable=self.soxl_var)
        soxl_check.grid(column=1, row=0, sticky=tk.W, padx=5)
        soxs_check = ttk.Checkbutton(self.frame, text="SOXS", variable=self.soxs_var)
        soxs_check.grid(column=2, row=0, sticky=tk.W, padx=5)

        years = list(range(2021, 2025))  # Include 2024
        months = list(range(1, 13))
        days = list(range(1, 32))

        ttk.Label(self.frame, text="Start Date:").grid(column=0, row=1, sticky=tk.W, padx=5)
        ttk.Label(self.frame, text="Year").grid(column=1, row=1, sticky=tk.W, padx=5)
        self.start_year_entry = ttk.Combobox(self.frame, textvariable=self.start_year_var, values=years, state="readonly")
        self.start_year_entry.grid(column=2, row=1, sticky=(tk.W, tk.E), padx=5)

        ttk.Label(self.frame, text="Month").grid(column=3, row=1, sticky=tk.W, padx=5)
        self.start_month_entry = ttk.Combobox(self.frame, textvariable=self.start_month_var, values=months, state="readonly")
        self.start_month_entry.grid(column=4, row=1, sticky=(tk.W, tk.E), padx=5)

        ttk.Label(self.frame, text="Day").grid(column=5, row=1, sticky=tk.W, padx=5)
        self.start_day_entry = ttk.Combobox(self.frame, textvariable=self.start_day_var, values=days, state="readonly")
        self.start_day_entry.grid(column=6, row=1, sticky=(tk.W, tk.E), padx=5)

        ttk.Label(self.frame, text="End Date:").grid(column=0, row=2, sticky=tk.W, padx=5)
        ttk.Label(self.frame, text="Year").grid(column=1, row=2, sticky=tk.W, padx=5)
        self.end_year_entry = ttk.Combobox(self.frame, textvariable=self.end_year_var, values=years, state="readonly")
        self.end_year_entry.grid(column=2, row=2, sticky=(tk.W, tk.E), padx=5)

        ttk.Label(self.frame, text="Month").grid(column=3, row=2, sticky=tk.W, padx=5)
        self.end_month_entry = ttk.Combobox(self.frame, textvariable=self.end_month_var, values=months, state="readonly")
        self.end_month_entry.grid(column=4, row=2, sticky=(tk.W, tk.E), padx=5)

        ttk.Label(self.frame, text="Day").grid(column=5, row=2, sticky=tk.W, padx=5)
        self.end_day_entry = ttk.Combobox(self.frame, textvariable=self.end_day_var, values=days, state="readonly")
        self.end_day_entry.grid(column=6, row=2, sticky=(tk.W, tk.E), padx=5)

        plot_button = ttk.Button(self.frame, text="Plot", command=self.on_plot)
        plot_button.grid(column=1, row=3, columnspan=2, sticky=tk.W, pady=10)

        trade_button = ttk.Button(self.frame, text="Execute Trading Strategy", command=self.on_trade)
        trade_button.grid(column=3, row=3, columnspan=2, sticky=tk.W, pady=10)

        self.plot_frame = ttk.Frame(self.root, padding=10)
        self.plot_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.plot_frame.grid_rowconfigure(0, weight=1)
        self.plot_frame.grid_columnconfigure(0, weight=1)

        self.trades_label = ttk.Label(self.frame, text="", foreground="black")
        self.trades_label.grid(column=0, row=8, columnspan=7, sticky=(tk.W, tk.E), pady=10)

    def on_plot(self):
        if self.controller:
            self.controller.on_plot()
        else:
            self.error_label.config(text="Controller not set.")

    def on_trade(self):
        if self.controller:
            self.controller.on_trade(40, 100)  # Example window sizes
        else:
            self.error_label.config(text="Controller not set.")

    def update(self, data):
        if 'symbols' in data and 'data' in data:
            self.plot_data(data['symbols'], data['data'])
        if 'trades' in data:
            self.display_trades(data['trades'])
        if 'final_balance' in data:
            self.display_final_balance(data['final_balance'])
        if 'description' in data:
            self.display_description(data['description'])
        if 'percent_diff' in data:
            self.display_percent_diff(data['percent_diff'])

    def display_trades(self, trades):
        trade_str = "Trades executed:\n"
        for trade in trades:
            trade_str += f"Date: {trade[0]}, Symbol: {trade[1]}, Action: {trade[2]}, Price: {trade[3]}, Amount: {trade[4]}\n"
        self.trades_label.config(text=trade_str)

    def display_final_balance(self, final_balance):
        self.trades_label.config(text=self.trades_label.cget("text") + f"\nFinal Portfolio Value: {final_balance}")

    def display_description(self, description):
        self.description_label.config(text=description)

    def display_percent_diff(self, percent_diff):
        self.percent_diff_label.config(text=f"Percentage Difference: {percent_diff:.2f}%")

    def plot_data(self, symbols, data):
        colors = {"SOXL": "blue", "SOXS": "red"}
        fig, ax = plt.subplots(figsize=(10, 6))

        for symbol in symbols:
            if data.empty:
                self.error_label.config(text=f"No data available for the given date range for {symbol}.")
                continue

            ax.plot(data['Date'], data['Close'], label=f'{symbol} Close Price', color=colors[symbol])

            ma_40 = data['Close'].rolling(window=40).mean()
            ma_100 = data['Close'].rolling(window=100).mean()

            ax.plot(data['Date'], ma_40, label=f'{symbol} 40-day MA', linestyle='--', color=colors[symbol])
            ax.plot(data['Date'], ma_100, label=f'{symbol} 100-day MA', linestyle=':', color=colors[symbol])

        if not ax.has_data():
            self.error_label.config(text="No data available for the given date range.")
            return None

        ax.set_title('Historical Prices with Moving Averages')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()

        self.error_label.config(text="")
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
