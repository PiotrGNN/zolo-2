@echo off
REM ZoL0 Trading System - API Server Startup
REM This script starts both API servers for real data access

title ZoL0 API Servers

echo.
echo ================================================================
echo            ZoL0 TRADING SYSTEM - API SERVER STARTUP
echo ================================================================
echo.

cd /d "C:\Users\piotr\Desktop\Zol0"

echo 🚀 Starting Main API Server (port 5000)...
start "ZoL0-Main-API" cmd /k "cd ZoL0-master && python dashboard_api.py"
timeout /t 3 /nobreak >nul

echo 🚀 Starting Enhanced API Server (port 5001)...
start "ZoL0-Enhanced-API" cmd /k "python enhanced_dashboard_api.py"
timeout /t 3 /nobreak >nul

echo.
echo ✅ API servers are starting...
echo.
echo 🌐 API Endpoints:
echo   • Main API:     http://localhost:5000
echo   • Enhanced API: http://localhost:5001
echo.
echo 📊 Next steps:
echo   1. Wait 10 seconds for APIs to fully start
echo   2. Run: python launch_all_dashboards.py
echo   3. Or manually start dashboards on ports 8501-8509
echo.
echo 💡 API servers will run in separate windows
echo    Close those windows to stop the servers
echo.

pause
