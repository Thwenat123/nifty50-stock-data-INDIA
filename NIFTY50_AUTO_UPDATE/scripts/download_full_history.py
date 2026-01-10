import yfinance as yf
import pandas as pd
import numpy as np
import time
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

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

os.makedirs(DATA_DIR, exist_ok=True)

all_data = []
failed = []

for i, ticker in enumerate(TICKERS, 1):
    print(f"{i:2d}/{len(TICKERS)} {ticker:20s}", end=" ")

    try:
        hist = yf.download(
            ticker,
            start="2010-01-01",
            end=datetime.now().strftime("%Y-%m-%d"),
            interval="1d",
            auto_adjust=False,
            progress=False,
            threads=False
        )

        if isinstance(hist.columns, pd.MultiIndex):
            hist.columns = hist.columns.get_level_values(0)

        if hist.empty:
            failed.append(ticker)
            print("✗ No data returned")
            continue

        df = hist.reset_index()
        df["Ticker"] = ticker

        closes = df["Close"].tolist()
        returns = []

        for j in range(len(closes)):
            if j == 0 or closes[j - 1] == 0:
                returns.append(None)
            else:
                returns.append(
                    ((closes[j] - closes[j - 1]) / closes[j - 1]) * 100
                )

        df["Daily_Return_%"] = returns
        all_data.append(df)

        print(
            f"✓ {len(df):,} rows "
            f"({df['Date'].min().date()} to {df['Date'].max().date()})"
        )

    except Exception as e:
        failed.append(ticker)
        print("✗ Error")

    time.sleep(0.5)

if all_data:
    final_df = pd.concat(all_data, ignore_index=True)

    filename = os.path.join(DATA_DIR, "NIFTY50_2010_20XX.csv")
    final_df.to_csv(filename, index=False)

    print("\n" + "=" * 60)
    print("✅ DOWNLOAD COMPLETE!")
    print("=" * 60)
    print(f"File: {filename}")
    print(f"Rows: {len(final_df):,}")
    print(
        f"Date range: "
        f"{final_df['Date'].min().date()} to {final_df['Date'].max().date()}"
    )
    print(f"Stocks: {final_df['Ticker'].nunique()}")

    if failed:
        print(f"\nFailed: {len(failed)} stocks")
        for f in failed[:5]:
            print(f"  {f}")

    print("\n💰 VERIFICATION:")
    for ticker in ["RELIANCE.NS", "TCS.NS"]:
        data = final_df[final_df["Ticker"] == ticker]
        first = data.iloc[0]
        last = data.iloc[-1]
        print(f"  {ticker}:")
        print(f"    First: {first['Date'].date()} - ₹{first['Close']:,.2f}")
        print(f"    Last:  {last['Date'].date()} - ₹{last['Close']:,.2f}")

print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')}")
print("=" * 60)








