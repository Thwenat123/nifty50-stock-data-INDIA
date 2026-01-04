
import yfinance as yf
import pandas as pd
import numpy as np
import time
import os
from datetime import datetime, timedelta

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

MASTER_FILE = "data/NIFTY50_2010_2026_20260103_1510.csv"

if not os.path.exists(MASTER_FILE):
    print(f"❌ ERROR: {MASTER_FILE} not found!")
    print("   Make sure the file exists in this folder.")
    exit(1)

print(f"📂 Loading {MASTER_FILE}...")
try:
    df = pd.read_csv(MASTER_FILE)
    df['Date'] = pd.to_datetime(df['Date'])
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
print(f"   Stocks: {len(TICKERS)}")
print("-" * 70)

all_new_data = []
failed = []

for i, ticker in enumerate(TICKERS, 1):
    print(f"[{i:2d}/{len(TICKERS)}] {ticker:20s}", end="")

    try:
        data = yf.download(ticker, start=start_date, progress=False, auto_adjust=False)

        if not data.empty:
            new_df = data.reset_index()
            new_df['Ticker'] = ticker

            new_df['Date'] = pd.to_datetime(new_df['Date']).dt.date

            closes = new_df['Close'].values
            returns = np.full(len(closes), np.nan)

            for j in range(1, len(closes)):
                if closes[j-1] != 0:
                    returns[j] = ((closes[j] - closes[j-1]) / closes[j-1]) * 100

            new_df['Daily_Return_%'] = returns

            all_new_data.append(new_df)
            print(f" ✓ {len(new_df):,} rows")
        else:
            failed.append(ticker)
            print(f" ✗ No data")

    except Exception as e:
        failed.append(ticker)
        print(f" ✗ Error")

    time.sleep(0.2)

if all_new_data:
    existing = pd.read_csv(MASTER_FILE)
    existing['Date'] = pd.to_datetime(existing['Date'])

    new_df = pd.concat(all_new_data, ignore_index=True)
    new_df['Date'] = pd.to_datetime(new_df['Date'])

    combined = pd.concat([existing, new_df], ignore_index=True)
    combined = combined.drop_duplicates(subset=['Date', 'Ticker'], keep='last')
    final_df = combined.sort_values(['Ticker', 'Date'])

    final_df.to_csv(MASTER_FILE, index=False)

    today = datetime.now().strftime("%Y%m%d_%H%M")
    backup_file = f"NIFTY50_BACKUP_{today}.csv"
    final_df.to_csv(backup_file, index=False)

    print("\n" + "=" * 70)
    print("✅ UPDATE COMPLETE!")
    print("=" * 70)
    print(f"📁 Master file updated: {MASTER_FILE}")
    print(f"📁 Daily backup: {backup_file}")
    print(f"📈 Total rows: {len(final_df):,} (was {total_rows:,})")
    print(f"📅 Date range: {final_df['Date'].min().date()} to {final_df['Date'].max().date()}")
    print(f"➕ New rows added: {len(new_df):,}")

    if failed:
        print(f"\n⚠ Failed: {len(failed)} stocks")
        for f in failed[:3]:
            print(f"   {f}")
        if len(failed) > 3:
            print(f"   ... and {len(failed)-3} more")

    print(f"\n💰 LATEST MARKET DATA:")
    for ticker in ["RELIANCE.NS", "TCS.NS"][:2]:
        stock_data = final_df[final_df['Ticker'] == ticker].tail(1)
        if not stock_data.empty:
            row = stock_data.iloc[0]
            ret = row['Daily_Return_%']
            ret_str = f"{ret:+.2f}%" if pd.notna(ret) else "N/A"
            print(f"  {ticker}: {row['Date'].date()} - ₹{row['Close']:,.2f} ({ret_str})")

    with open("update_log.txt", "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
               f"UPDATE | Added {len(new_df):,} rows | "
               f"Total: {len(final_df):,} | "
               f"Latest: {final_df['Date'].max().date()}\n")

else:
    print("\n❌ No new data (market holiday?)")
    with open("docs/update_log.txt", "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | NO DATA | Market holiday\n")

print(f"\n⏰ Next update scheduled: Tomorrow 18:00")
print("=" * 70)






