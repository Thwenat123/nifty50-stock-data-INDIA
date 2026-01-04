@echo off
echo ===========================================
echo    NIFTY 50 DAILY UPDATE
echo    Date: %date% Time: %time%
echo ===========================================

cd /d "C:\NIFTY50_AUTO_UPDATE"

python scripts/daily_nifty.py

if %errorlevel% equ 0 (
    echo.
    echo ✅ UPDATE COMPLETED
) else (
    echo.
    echo ⚠ NO NEW DATA (Market holiday)
)

echo.
echo Script completed at %time%
pause