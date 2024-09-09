import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from tkinter import ttk
from tkcalendar import DateEntry
import MetaTrader5 as mt5
import pytz
import datetime

# Initialize MetaTrader5
if not mt5.initialize():
    print("MetaTrader5 initialization failed")
    exit()

timezone = pytz.timezone("Etc/UTC")

def scrape_data():
    try:
        # Get the selected start and end dates from the date pickers
        start_date = start_cal.get_date()
        end_date = end_cal.get_date()

        # Convert the selected dates to datetime objects and set timezone
        utc_from = datetime.datetime(start_date.year, start_date.month, start_date.day, tzinfo=timezone)
        utc_to = datetime.datetime(end_date.year, end_date.month, end_date.day, tzinfo=timezone)

        # Fetch rates between the specified dates
        rates = mt5.copy_ticks_range("EURUSD", utc_from, utc_to)
        
        if rates is None:
            raise ValueError("No data returned from MetaTrader5.")

        # Convert the rates to a pandas DataFrame
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')

        # Open a save file dialog box
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save CSV"
        )

        if file_path:
            # Save the DataFrame to a CSV file
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Success", f"Data successfully saved to {file_path}")

    except Exception as e:
        # Display an error message
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Date Range Picker")
root.geometry("350x200")

# Create a frame for the date pickers and button
frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

# Create start date entry
ttk.Label(frame, text="Start Date:").grid(row=0, column=0, padx=5, pady=5)
start_cal = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
start_cal.grid(row=0, column=1, padx=5, pady=5)

# Create end date entry
ttk.Label(frame, text="End Date:").grid(row=1, column=0, padx=5, pady=5)
end_cal = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
end_cal.grid(row=1, column=1, padx=5, pady=5)

# Create a button to scrape data
scrape_btn = ttk.Button(frame, text="Scrape Data", command=scrape_data)
scrape_btn.grid(row=2, columnspan=2, pady=10)

# Run the application
root.mainloop()
