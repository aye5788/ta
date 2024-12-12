import streamlit as st
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

# Function to fetch data
def fetch_data(ticker, interval, period='1mo'):
    # Fetch historical data using yfinance
    data = yf.download(tickers=ticker, interval=interval, period=period)
    data['Date'] = data.index  # Add date column for plotting
    return data

# Function to calculate technical indicators and provide interpretations
def analyze_technical_indicators(data):
    analysis = []

    # RSI Analysis
    rsi = RSIIndicator(data['Close']).rsi()
    latest_rsi = rsi.iloc[-1]
    if latest_rsi > 70:
        analysis.append(f"RSI is {latest_rsi:.2f} (Overbought). Price might reverse or consolidate.")
    elif latest_rsi < 30:
        analysis.append(f"RSI is {latest_rsi:.2f} (Oversold). Price might rebound.")
    else:
        analysis.append(f"RSI is {latest_rsi:.2f} (Neutral).")

    # Bollinger Bands Analysis
    bb = BollingerBands(data['Close'])
    high_band = bb.bollinger_hband().iloc[-1]
    low_band = bb.bollinger_lband().iloc[-1]
    close_price = data['Close'].iloc[-1]

    if close_price > high_band:
        analysis.append(f"Price is above the upper Bollinger Band (${high_band:.2f}). Potential overbought condition.")
    elif close_price < low_band:
        analysis.append(f"Price is below the lower Bollinger Band (${low_band:.2f}). Potential oversold condition.")
    else:
        analysis.append(f"Price is within Bollinger Bands (High: ${high_band:.2f}, Low: ${low_band:.2f}). No extremes detected.")

    return analysis

# Streamlit App
st.title("Ticker Technical Analysis and Insights")

# User Inputs
ticker = st.text_input("Enter Ticker Symbol (e.g., AAPL, SPY):", value="AAPL")
interval = st.selectbox("Select Timeframe:", ['1m', '5m', '15m', '1h', '1d', '1wk', '1mo'])
period = st.selectbox("Select Data Range:", ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y'])

# Analyze Button
if st.button("Analyze"):
    st.write(f"Fetching data for {ticker} at {interval} intervals over the past {period}.")

    try:
        # Fetch Data
        data = fetch_data(ticker, interval, period)
        st.write(f"Data Fetched: {data.shape[0]} rows.")

        # Perform Technical Analysis
        analysis = analyze_technical_indicators(data)

        # Display Insights
        st.subheader("Technical Analysis Insights")
        for insight in analysis:
            st.write(f"- {insight}")

        # Plot Close Prices
        st.subheader("Price Chart")
        st.line_chart(data['Close'])

    except Exception as e:
        st.error(f"Error: {e}")
