import yfinance as yf
import pandas as pd
import numpy as np
import time
import os
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

print("=" * 70)
print("NIFTY 50 DAILY UPDATER")
print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

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

MASTER_FILE = os.path.join(DATA_DIR, "NIFTY50_2010_20XX.csv")

if not os.path.exists(MASTER_FILE):
    print(f"❌ ERROR: {MASTER_FILE} not found!")
    exit(1)

print(f"📂 Loading {MASTER_FILE}...")
try:
    df = pd.read_csv(MASTER_FILE)
    df['Date'] = pd.to_datetime(df['Date'], format="mixed", dayfirst=True)
    latest = df['Date'].max()
    total_rows = len(df)
    print(f"   ✓ Loaded: {total_rows:,} rows")
    print(f"   📅 Latest date: {latest.date()}")
    print(f"   🏢 Unique stocks: {df['Ticker'].nunique()}")
except Exception as e:
    print(f"❌ Error loading file: {e}")
    exit(1)

start_date = (latest - timedelta(days=60)).strftime('%Y-%m-%d')
print(f"\n📥 Downloading new data from {start_date}...")
print("-" * 70)

all_new_data = []
failed = []

for i, ticker in enumerate(TICKERS, 1):
    print(f"[{i:2d}/{len(TICKERS)}] {ticker:20s}", end="")

    try:
        data = yf.download(ticker, start=start_date, progress=False)

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        if not data.empty:
            new_df = data.reset_index()
            new_df['Ticker'] = ticker

            new_df['Date'] = pd.to_datetime(new_df['Date'])

            new_df['Daily_Return_%'] = new_df['Close'].pct_change() * 100

            all_new_data.append(new_df)
            print(f" ✓ {len(new_df):,} rows")
        else:
            failed.append(ticker)
            print(" ✗ No data")

    except Exception as e:
        failed.append(ticker)
        print(f" ✗ Error: {str(e)[:50]}")

    time.sleep(0.2)

if all_new_data:
    existing = pd.read_csv(MASTER_FILE)
    existing['Date'] = pd.to_datetime(existing['Date'], format="mixed", dayfirst=True)

    new_df = pd.concat(all_new_data, ignore_index=True)
    new_df['Date'] = pd.to_datetime(new_df['Date'])

    combined = pd.concat([existing, new_df], ignore_index=True)
    combined = combined.drop_duplicates(subset=['Date', 'Ticker'], keep='last')
    final_df = combined.sort_values(['Ticker', 'Date'])

    final_df.to_csv(MASTER_FILE, index=False)

    today = datetime.now().strftime("%Y%m%d_%H%M")
    backup_file = os.path.join(DATA_DIR, f"NIFTY50_BACKUP_{today}.csv")
    final_df.to_csv(backup_file, index=False)

    print("\n" + "=" * 70)
    print("✅ UPDATE COMPLETE!")
    print("=" * 70)

    with open(os.path.join(LOG_DIR, "update_log.txt"), "a") as f:
        f.write(
            f"{datetime.now():%Y-%m-%d %H:%M:%S} | "
            f"UPDATE | Added {len(new_df):,} rows | "
            f"Total: {len(final_df):,} | "
            f"Latest: {final_df['Date'].max().date()}\n"
        )

else:
    print("\n❌ No new data (market holiday?)")
    with open(os.path.join(LOG_DIR, "update_log.txt"), "a") as f:
        f.write(
            f"{datetime.now():%Y-%m-%d %H:%M:%S} | NO DATA | Market holiday\n"
        )

print("=" * 70)
