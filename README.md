NIFTY 50 STOCK DATA PIPELINE - INDIA

Project Overview:
Complete automated pipeline for downloading and updating all NIFTY 50 Indian stocks data from 2010 to present. Daily automatic updates via Windows Task Scheduler.

Dataset:
File: nifty50_2010_2025.csv
Rows: Approximately 190,000 daily observations
Stocks: All 50 NIFTY constituents
Period: January 2010 - December 2025
Columns: Date, Open, High, Low, Close, Volume, Daily_Return_%, Log_Return, Ticker

Setup:
1. Clone repository
2. Install requirements: pip install -r requirements.txt
3. Run initial download: python scripts/download_full_history.py

Automation:
Windows Task Scheduler runs daily at 18:00 (6:00 PM) after market closes.
Batch file: scripts/run_daily_update.bat

Project Structure:
data/ - Historical CSV files
scripts/ - Python and batch scripts
docs/ - Setup instructions
requirements.txt - Python dependencies

Technical Stack:
Python, Jupyter, Pandas, yFinance, Windows Task Scheduler, Batch Scripting

Use Cases:
Portfolio analysis, backtesting, market research, academic studies

Author: Pradyumna Banerjee
GitHub: Thwenat123/nifty50-stock-data-INDIA
