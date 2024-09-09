import pandas as pd

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

    return data[['time', 'close', 'SMA_short', 'SMA_long', 'signal', 'positions']]

# Usage
# df = sma_crossover_strategy(df)

def calculate_macd(data, short_period=12, long_period=26, signal_period=9):
    """Calculate the MACD and signal line."""
    data['ema_short'] = data['close'].ewm(span=short_period, adjust=False).mean()
    data['ema_long'] = data['close'].ewm(span=long_period, adjust=False).mean()

    data['MACD'] = data['ema_short'] - data['ema_long']
    data['signal_line'] = data['MACD'].ewm(span=signal_period, adjust=False).mean()

    data['MACD_histogram'] = data['MACD'] - data['signal_line']

    return data[['time', 'MACD', 'signal_line', 'MACD_histogram']]

# Usage
# df = calculate_macd(df)

def heiken_ashi(data):
    """Calculate Heiken Ashi candles."""
    ha_data = pd.DataFrame(index=data.index)
    ha_data['HA_close'] = (data['open'] + data['high'] + data['low'] + data['close']) / 4
    ha_data['HA_open'] = (data['open'].shift(1) + data['close'].shift(1)) / 2
    ha_data['HA_high'] = data[['high', 'HA_open', 'HA_close']].max(axis=1)
    ha_data['HA_low'] = data[['low', 'HA_open', 'HA_close']].min(axis=1)

    # Handle first row initialization (use the original open and close for the first row)
    ha_data['HA_open'].iloc[0] = data['open'].iloc[0]

    return ha_data[['HA_open', 'HA_high', 'HA_low', 'HA_close']]

# Usage
# df_ha = heiken_ashi(df)