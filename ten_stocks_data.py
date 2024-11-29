import yfinance as yf
import pandas as pd
import numpy as np

# Define the list of stock tickers
tickers = ['NVDA', 'SPY', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'BRK-B', 'JNJ', 'V']

# Download data for each stock
data = {}
for ticker in tickers:
    data[ticker] = yf.download(ticker, start='2018-01-01', end='2024-11-27', interval='1mo')['Adj Close']

# Download 1-month T-Bill (^IRX) data
rf = yf.download('^IRX', start='2018-01-01', end='2024-11-27', interval='1mo')['Adj Close'] / 100

# Align all data to the same index (the index of NVDA)
common_index = data['NVDA'].index

# Reindex all stocks and RF to match NVDA's index
for ticker in tickers:
    data[ticker] = data[ticker].reindex(common_index)
rf = rf.reindex(common_index)

# Forward-fill and backward-fill missing values in T-bill rate
rf.fillna(method='ffill', inplace=True)
rf.fillna(method='bfill', inplace=True)

# Calculate log returns for each stock
log_returns = {}
for ticker in tickers:
    log_returns[ticker] = np.log(data[ticker] / data[ticker].shift(1)) - rf/12

# Create DataFrame with all aligned data
df_data = {'Date': common_index, '1M_TBill_Rate': rf.values.flatten()}
for ticker in tickers:
    df_data[f'{ticker}_Adj_Close'] = data[ticker].values.flatten()
    df_data[f'{ticker}_rp'] = log_returns[ticker].values.flatten()

df = pd.DataFrame(df_data)

# Display the DataFrame
print(df)
df.to_csv('stocks.csv', index=False)