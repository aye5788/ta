import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from ta import add_all_ta_features

# Function to fetch data
def fetch_data(ticker, interval, period='1mo'):
    # Use yfinance to fetch historical data
    data = yf.download(tickers=ticker, interval=interval, period=period)
    data['Date'] = data.index
    return data

# Function to calculate technical indicators
def calculate_indicators(data):
    data = data.copy()
    data = add_all_ta_features(
        df=data,
        open="Open",
        high="High",
        low="Low",
        close="Close",
        volume="Volume",
        fillna=True
    )
    return data

# Function to plot data
def plot_chart(data, indicators):
    plt.figure(figsize=(12, 6))
    plt.plot(data['Date'], data['Close'], label='Close Price', color='blue', linewidth=2)
    
    # Add selected indicators to the plot
    for ind in indicators:
        if ind in data.columns:
            plt.plot(data['Date'], data[ind], label=ind, linewidth=1)
    
    plt.title("Technical Analysis")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()
    st.pyplot(plt)

# Streamlit App
st.title("Ticker Technical Analysis Tool")

# User Inputs
ticker = st.text_input("Enter Ticker Symbol (e.g., AAPL, SPY):", value="AAPL")
interval = st.selectbox("Select Timeframe:", ['1m', '5m', '15m', '1h', '1d', '1wk', '1mo'])
period = st.selectbox("Select Data Range:", ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y'])

# Submit Button
if st.button("Analyze"):
    st.write(f"Fetching data for {ticker} at {interval} intervals over the past {period}.")
    
    try:
        # Fetch Data
        data = fetch_data(ticker, interval, period)
        st.write(f"Data Fetched: {data.shape[0]} rows.")
        
        # Calculate Indicators
        data_with_indicators = calculate_indicators(data)
        
        # Select Indicators to Plot
        all_indicators = ['Close', 'trend_macd', 'trend_macd_signal', 'volatility_bbm', 'volatility_bbh', 'volatility_bbl']
        selected_indicators = st.multiselect("Select Indicators to Plot:", all_indicators, default=['Close'])
        
        # Plot Chart
        plot_chart(data_with_indicators, selected_indicators)
    except Exception as e:
        st.error(f"Error: {e}")
