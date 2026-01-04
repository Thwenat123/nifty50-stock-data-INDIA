
import yfinance as yf
import pandas as pd
import numpy as np
import time
import os
from datetime import datetime

print("=" * 60)
print("NIFTY 50 COMPLETE DOWNLOAD (2010-2026)")
print("=" * 60)

TICKERS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS",
    "ITC.NS", "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS",
    "KOTAKBANK.NS", "LT.NS", "HINDUNILVR.NS", "AXISBANK.NS",
    "MARUTI.NS", "BAJFINANCE.NS", "WIPRO.NS", "ONGC.NS",
    "TITAN.NS", "NTPC.NS", "ULTRACEMCO.NS", "SUNPHARMA.NS",
    "POWERGRID.NS", "NESTLEIND.NS", "INDUSINDBK.NS",
    "BAJAJFINSV.NS", "JSWSTEEL.NS", "TATASTEEL.NS", "HCLTECH.NS",
    "DRREDDY.NS", "ASIANPAINT.NS", "TECHM.NS", "HINDALCO.NS",
    "GRASIM.NS", "DIVISLAB.NS", "ADANIENT.NS", "CIPLA.NS",
    "M&M.NS", "ADANIPORTS.NS", "BRITANNIA.NS", "EICHERMOT.NS",
    "BAJAJ-AUTO.NS", "SBILIFE.NS", "SHREECEM.NS", "COALINDIA.NS",
    "UPL.NS", "APOLLOHOSP.NS", "TATACONSUM.NS", "BPCL.NS",
    "HEROMOTOCO.NS", "IOC.NS"
]

print(f"Downloading {len(TICKERS)} stocks from 2010-01-01...")

all_data = []
failed = []

for i, ticker in enumerate(TICKERS, 1):
    print(f"{i:2d}/{len(TICKERS)} {ticker:20s}", end=" ")

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start="2010-01-01")

        if len(hist) > 1000:   
            df = hist.reset_index()
            df['Ticker'] = ticker

            closes = df['Close'].tolist()
            returns = []
            for j in range(len(closes)):
                if j == 0:
                    returns.append(None)
                elif closes[j-1] != 0:
                    ret = ((closes[j] - closes[j-1]) / closes[j-1]) * 100
                    returns.append(ret)
                else:
                    returns.append(None)

            df['Daily_Return_%'] = returns

            all_data.append(df)
            print(f"✓ {len(df):,} rows ({df['Date'].min().date()} to {df['Date'].max().date()})")
        else:
            failed.append(ticker)
            print(f"✗ Not enough data: {len(hist)} rows")

    except Exception as e:
        failed.append(ticker)
        print(f"✗ Error")

    time.sleep(0.3)

if all_data:
    final_df = pd.concat(all_data, ignore_index=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"data/NIFTY50_2010_2026_{timestamp}.csv"
    final_df.to_csv(filename, index=False)

    print(f"\n" + "=" * 60)
    print("✅ DOWNLOAD COMPLETE!")
    print("=" * 60)
    print(f"File: {filename}")
    print(f"Rows: {len(final_df):,}")
    print(f"Date range: {final_df['Date'].min().date()} to {final_df['Date'].max().date()}")
    print(f"Stocks: {final_df['Ticker'].nunique()}")

    if failed:
        print(f"\nFailed: {len(failed)} stocks")
        for f in failed[:5]:
            print(f"  {f}")

    print(f"\n💰 VERIFICATION:")
    for ticker in ["RELIANCE.NS", "TCS.NS"]:
        data = final_df[final_df['Ticker'] == ticker]
        first = data.iloc[0]
        last = data.iloc[-1]
        print(f"  {ticker}:")
        print(f"    First: {first['Date'].date()} - ₹{first['Close']:,.2f}")
        print(f"    Last:  {last['Date'].date()} - ₹{last['Close']:,.2f}")

print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')}")
print("=" * 60)







