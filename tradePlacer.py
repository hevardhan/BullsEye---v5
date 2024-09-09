import tkinter as tk
from tkinter import messagebox
import MetaTrader5 as mt5
import pandas as pd

# MetaTrader5 initialization
mt5.initialize()

# Constants
DEVIATION = 10  # Set your deviation here

def market_order(symbol, volume, order_type, stop_loss, take_profit, **kwargs):
    tick = mt5.symbol_info_tick(symbol)
    order_dict = {'buy': 0, 'sell': 1}
    price_dict = {'buy': tick.ask, 'sell': tick.bid}
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_dict[order_type],
        "price": price_dict[order_type],
        "deviation": DEVIATION,
        "magic": 100,
        "comment": "python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    order_result = mt5.order_send(request)
    print(order_result)

    return order_result

def close_order(ticket, symbol):
    positions = mt5.positions_get()

    for pos in positions:
        tick = mt5.symbol_info_tick(pos.symbol)
        type_dict = {0: 1, 1: 0}  # 0 represents buy, 1 represents sell - inverting order_type to close the position
        price_dict = {0: tick.ask, 1: tick.bid}

        if pos.ticket == ticket and pos.symbol == symbol:
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "position": pos.ticket,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": type_dict[pos.type],
                "price": price_dict[pos.type],
                "deviation": DEVIATION,
                "magic": 100,
                "comment": "python close order",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            order_result = mt5.order_send(request)
            print(order_result)

            return order_result

    return "Ticket doesn't Exist"

def get_exposure(symbol):
    positions = mt5.positions_get(symbol=symbol)
    if positions:
        pos_df = pd.DataFrame(positions, columns=positions[0]._asdict().keys())
        exposure = pos_df['volume'].sum()

        return exposure

# Tkinter GUI
class TradeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trade Application")
        
        # Create widgets
        tk.Label(root, text="Symbol:").grid(row=0, column=0, padx=10, pady=10)
        self.symbol_entry = tk.Entry(root)
        self.symbol_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(root, text="Volume:").grid(row=1, column=0, padx=10, pady=10)
        self.volume_entry = tk.Entry(root)
        self.volume_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(root, text="Order Type (buy/sell):").grid(row=2, column=0, padx=10, pady=10)
        self.order_type_entry = tk.Entry(root)
        self.order_type_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(root, text="Stop Loss:").grid(row=3, column=0, padx=10, pady=10)
        self.stop_loss_entry = tk.Entry(root)
        self.stop_loss_entry.grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(root, text="Take Profit:").grid(row=4, column=0, padx=10, pady=10)
        self.take_profit_entry = tk.Entry(root)
        self.take_profit_entry.grid(row=4, column=1, padx=10, pady=10)
        
        tk.Button(root, text="Place Order", command=self.place_order).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def place_order(self):
        symbol = self.symbol_entry.get()
        volume = float(self.volume_entry.get())
        order_type = self.order_type_entry.get()
        stop_loss = float(self.stop_loss_entry.get())
        take_profit = float(self.take_profit_entry.get())
        
        result = market_order(symbol, volume, order_type, stop_loss, take_profit)
        
        if result:
            messagebox.showinfo("Success", "Order placed successfully!")
        else:
            messagebox.showerror("Error", "Failed to place order.")

# Run Tkinter application
root = tk.Tk()
app = TradeApp(root)
root.mainloop()
