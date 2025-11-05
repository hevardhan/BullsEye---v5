import pandas as pd
import numpy as np

def calculate_sma(data, window):
    """Calculate the Simple Moving Average (SMA) for a given window."""
    return data['close'].rolling(window=window).mean()

def sma_crossover_strategy(data, short_window=50, long_window=200):
    """Implement a simple SMA crossover strategy."""
    data['SMA_short'] = calculate_sma(data, short_window)
    data['SMA_long'] = calculate_sma(data, long_window)
    data['signal'] = 0
    data['signal'][short_window:] = np.where(data['SMA_short'][short_window:] > data['SMA_long'][short_window:], 1, 0)  
    data['positions'] = data['signal'].diff()
    return data

def rsi(data, period=14):
    """Calculate the Relative Strength Index (RSI)."""
    delta = data['close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    return data

def calculate_macd(data, short_period=12, long_period=26, signal_period=9):
    """Calculate the MACD and signal line."""
    data['ema_short'] = data['close'].ewm(span=short_period, adjust=False).mean()
    data['ema_long'] = data['close'].ewm(span=long_period, adjust=False).mean()
    data['MACD'] = data['ema_short'] - data['ema_long']
    data['signal_line'] = data['MACD'].ewm(span=signal_period, adjust=False).mean()
    data['MACD_histogram'] = data['MACD'] - data['signal_line']
    return data

def heiken_ashi(data):
    """Calculate Heiken Ashi candles."""
    ha_data = pd.DataFrame(index=data.index)
    ha_data['HA_close'] = (data['open'] + data['high'] + data['low'] + data['close']) / 4
    ha_data['HA_open'] = (data['open'].shift(1) + data['close'].shift(1)) / 2
    ha_data['HA_high'] = data[['high', 'HA_open', 'HA_close']].max(axis=1)
    ha_data['HA_low'] = data[['low', 'HA_open', 'HA_close']].min(axis=1)
    ha_data['HA_open'].iloc[0] = data['open'].iloc[0]
    return ha_data[['HA_open', 'HA_high', 'HA_low', 'HA_close']]

def stochastic_oscillator(data, k_period=9, d_period=6):
    """Calculate Stochastic Oscillator."""
    data['low_min'] = data['low'].rolling(window=k_period).min()
    data['high_max'] = data['high'].rolling(window=k_period).max()
    data['%K'] = 100 * (data['close'] - data['low_min']) / (data['high_max'] - data['low_min'])
    data['%D'] = data['%K'].rolling(window=d_period).mean()
    return data

def atr(data, period=14):
    """Calculate the Average True Range (ATR)."""
    data['H-L'] = data['high'] - data['low']
    data['H-C'] = np.abs(data['high'] - data['close'].shift())
    data['L-C'] = np.abs(data['low'] - data['close'].shift())
    tr = data[['H-L', 'H-C', 'L-C']].max(axis=1)
    data['ATR'] = tr.rolling(window=period).mean()
    return data

def adx(data, period=14):
    """Calculate the Average Directional Index (ADX)."""
    data['H-L'] = data['high'] - data['low']
    data['H-C'] = np.abs(data['high'] - data['close'].shift())
    data['L-C'] = np.abs(data['low'] - data['close'].shift())
    tr = data[['H-L', 'H-C', 'L-C']].max(axis=1)
    data['ATR'] = tr.rolling(window=period).mean()
    data['+DM'] = np.where((data['high'] - data['high'].shift(1)) > (data['low'].shift(1) - data['low']), data['high'] - data['high'].shift(1), 0)
    data['-DM'] = np.where((data['low'].shift(1) - data['low']) > (data['high'] - data['high'].shift(1)), data['low'].shift(1) - data['low'], 0)
    data['+DI'] = 100 * (data['+DM'].rolling(window=period).sum() / data['ATR'])
    data['-DI'] = 100 * (data['-DM'].rolling(window=period).sum() / data['ATR'])
    data['DX'] = (abs(data['+DI'] - data['-DI']) / (data['+DI'] + data['-DI'])) * 100
    data['ADX'] = data['DX'].rolling(window=period).mean()
    return data

def williams_r(data, period=14):
    """Calculate Williams %R."""
    data['highest_high'] = data['high'].rolling(window=period).max()
    data['lowest_low'] = data['low'].rolling(window=period).min()
    data['Williams %R'] = -100 * (data['highest_high'] - data['close']) / (data['highest_high'] - data['lowest_low'])
    return data

def cci(data, period=14):
    """Calculate Commodity Channel Index (CCI)."""
    tp = (data['high'] + data['low'] + data['close']) / 3
    ma = tp.rolling(window=period).mean()
    md = tp.rolling(window=period).apply(lambda x: np.fabs(x - x.mean()).mean(), raw=True)
    data['CCI'] = (tp - ma) / (0.015 * md)
    return data

def roc(data, period=14):
    """Calculate Rate of Change (ROC)."""
    data['ROC'] = ((data['close'] - data['close'].shift(period)) / data['close'].shift(period)) * 100
    return data

def ultimate_oscillator(data, short_period=7, medium_period=14, long_period=28):
    """Calculate Ultimate Oscillator."""
    bp = data['close'] - pd.DataFrame({'low': data['low'], 'close_shift': data['close'].shift(1)}).min(axis=1)
    tr = pd.DataFrame({'high': data['high'], 'low': data['low'], 'close_shift': data['close'].shift(1)}).max(axis=1) - data[['low', 'close']].min(axis=1)
    avg7 = bp.rolling(window=short_period).sum() / tr.rolling(window=short_period).sum()
    avg14 = bp.rolling(window=medium_period).sum() / tr.rolling(window=medium_period).sum()
    avg28 = bp.rolling(window=long_period).sum() / tr.rolling(window=long_period).sum()
    data['Ultimate Oscillator'] = 100 * (4 * avg7 + 2 * avg14 + avg28) / (4 + 2 + 1)
    return data


def add_time_features(df, time_column):
    """
    Adds time-based columns to a DataFrame.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing a datetime column.
    time_column (str): The name of the column with datetime data.
    
    Returns:
    pd.DataFrame: The DataFrame with new time-based columns.
    """
    # Ensure the time_column is in datetime format
    df[time_column] = pd.to_datetime(df[time_column], errors='coerce')

    # Extract time features
    df['minute'] = df[time_column].dt.minute
    df['hour'] = df[time_column].dt.hour
    df['day'] = df[time_column].dt.day
    df['month'] = df[time_column].dt.month
    df['year'] = df[time_column].dt.year

    return df

def generate_macd_signals(df):
    """
    Adds a 'signal' column to the DataFrame based on MACD strategy.
    
    Parameters:
        df (pd.DataFrame): A DataFrame containing the MACD line, Signal line, and other columns.
    
    Returns:
        pd.DataFrame: The input DataFrame with an additional 'signal' column.
    """
    # Initialize the 'signal' column with 0 (no signal)
    df['Signal'] = 0

    # Generate buy (1) and sell (-1) signals
    for i in range(1, len(df)):
        # Bullish crossover (Buy)
        if df.loc[i, 'MACD'] > df.loc[i, 'signal_line']:
            df.loc[i, 'Signal'] = 1

        # Bearish crossover (Sell)
        elif df.loc[i, 'MACD'] <= df.loc[i, 'signal_line']:
            df.loc[i, 'Signal'] = 0
        # if df.loc[i, 'MACD'] > df.loc[i, 'signal_line'] and df.loc[i - 1, 'MACD'] <= df.loc[i - 1, 'signal_line']:
        #     df.loc[i, 'Signal'] = 1

        # # Bearish crossover (Sell)
        # elif df.loc[i, 'MACD'] < df.loc[i, 'signal_line'] and df.loc[i - 1, 'MACD'] >= df.loc[i - 1, 'signal_line']:
        #     df.loc[i, 'Signal'] = -1

    return df

def add_next_close_price_on_signal(df):
    """
    Adds a new column to the DataFrame with the close price of the next signal (1 or -1).
    Sets next_close to 0 if the current signal is 0.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame with 'close' and 'Signal' columns.
    
    Returns:
    pd.DataFrame: The DataFrame with the new column 'next_close'.
    """
    # Initialize a new column
    df['next_close'] = None
    
    # Loop through the DataFrame to find the next signal's close price
    for i in range(len(df)):
        if df.at[i, 'Signal'] == 0:
            df.at[i, 'next_close'] = 0  # Set next_close to 0 if Signal is 0
        elif df.at[i, 'Signal'] in [1, -1]:  # Check for buy or sell signal
            # Find the next row with either a 1 or -1 signal
            for j in range(i + 1, len(df)):
                if df.at[j, 'Signal'] in [1, -1]:
                    df.at[i, 'next_close'] = df.at[j, 'close']
                    break  # Exit the inner loop once the next signal is found

    return df

# Usage example for each function
# df = sma_crossover_strategy(df)
# df = rsi(df)
# df = calculate_macd(df)
# df_ha = heiken_ashi(df)
# df = stochastic_oscillator(df)
# df = atr(df)
# df = adx(df)
# df = williams_r(df)
# df = cci(df)
# df = roc(df)
# df = ultimate_oscillator(df)