NIFTY 50 STOCK DATA PIPELINE - INDIA

Project Overview:
Complete automated pipeline for downloading and updating all NIFTY 50 Indian stocks data from 2010 to present. Daily automatic updates via Windows Task Scheduler.

Dataset:
File: NIFTY50_2010_20XX.csv

Rows: Approximately 190,000 daily observations

Stocks: All 49 NIFTY constituents

Period: January 2010 - current

Columns: Date, Open, High, Low, Close, Volume, Daily_Return_%

Local Setup (MUST have Python 3.8+):
1. Clone repository
2. Open cmd or powershell (as admin)
3. Install requirements: pip install -r requirements.txt
4. Run initial download: python scripts/download_full_history.py
5. Automation: Setup Windows Task Scheduler to run this file daily at 1800 IST (6:00 PM) after market closes- Batch file: scripts/run_daily_update.bat

For others, direct download of data/NIFTY50_2010_20XX should suffice (but will not update automatically, will have to be redownloaded every market-open for new data)

Project Structure:

data/Historical CSV files

scripts/Python and batch scripts

docs/changelogs

requirements.txt - Python dependencies

Technical Stack:
Python, Jupyter, Pandas, yFinance, Windows Task Scheduler, Batch Scripting

Use Cases:
Portfolio analysis, backtesting, market research, academic studies

Author: Pradyumna Banerjee
GitHub: Thwenat123/nifty50-stock-data-INDIA
