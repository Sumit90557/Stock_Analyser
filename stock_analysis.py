import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mpf

# 1. Load and Inspect the Data
df = pd.read_csv('infy_stock.csv')

# Display the first 10 rows
print("First 10 rows of the dataset:")
print(df.head(10))

# Check for missing values
missing_values = df.isnull().sum()
print("\nMissing values in each column:")
print(missing_values)

# Handle missing values (if any) using forward fill
df.fillna(method='ffill', inplace=True)

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# 2. Data Visualization

# a) Plot the Closing Price over time
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Close'], label='Closing Price')
plt.title('Stock Closing Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price (INR)')
plt.legend()
plt.show()

# b) Candlestick Chart (last 100 days)
df.set_index('Date', inplace=True)  # Set 'Date' as index for plotting
mpf.plot(df[-100:], type='candle', style='charles', volume=True, title="Candlestick Chart (Last 100 Days)")

# 3. Statistical Analysis

# a) Daily Return Percentage
df['Daily Return (%)'] = ((df['Close'] - df['Open']) / df['Open']) * 100
print("\nDaily Return Percentage:")
print(df[['Open', 'Close', 'Daily Return (%)']].head())

# b) Average and Median of Daily Returns
average_return = df['Daily Return (%)'].mean()
median_return = df['Daily Return (%)'].median()
print(f"\nAverage Daily Return: {average_return:.2f}%")
print(f"Median Daily Return: {median_return:.2f}%")

# c) Standard Deviation of Closing Prices
std_dev_close = df['Close'].std()
print(f"Standard Deviation of Closing Price: {std_dev_close:.2f}")

# 4. Moving Averages

# a) Calculate the 50-day and 200-day moving averages
df['50_MA'] = df['Close'].rolling(window=50).mean()
df['200_MA'] = df['Close'].rolling(window=200).mean()

# Plot Closing Price with Moving Averages
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Close'], label='Closing Price')
plt.plot(df.index, df['50_MA'], label='50-day MA', color='orange')
plt.plot(df.index, df['200_MA'], label='200-day MA', color='red')
plt.title('Stock Closing Price with 50-day and 200-day Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price (INR)')
plt.legend()
plt.show()

# 5. Volatility Analysis

# a) Rolling Standard Deviation (30-day window)
df['30_Rolling_STD'] = df['Close'].rolling(window=30).std()

# Plot the volatility (rolling standard deviation)
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['30_Rolling_STD'], label='30-day Rolling Std Dev', color='purple')
plt.title('Stock Volatility (30-day Rolling Std Dev)')
plt.xlabel('Date')
plt.ylabel('Standard Deviation')
plt.legend()
plt.show()

# 6. Trend Analysis

# a) Identify and mark Bullish and Bearish Trends
df['Trend'] = 'Neutral'
df.loc[df['50_MA'] > df['200_MA'], 'Trend'] = 'Bullish'
df.loc[df['50_MA'] < df['200_MA'], 'Trend'] = 'Bearish'

# Plot trends with bullish and bearish highlighting
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Close'], label='Closing Price')
plt.plot(df.index, df['50_MA'], label='50-day MA', color='orange')
plt.plot(df.index, df['200_MA'], label='200-day MA', color='red')

# Highlight Bullish/Bearish trends
bullish = df[df['Trend'] == 'Bullish']
bearish = df[df['Trend'] == 'Bearish']
plt.fill_between(bullish.index, df['Close'], color='green', alpha=0.3, label='Bullish')
plt.fill_between(bearish.index, df['Close'], color='red', alpha=0.3, label='Bearish')

plt.title('Stock Trends (Bullish/Bearish)')
plt.xlabel('Date')
plt.ylabel('Price (INR)')
plt.legend()
plt.show()
