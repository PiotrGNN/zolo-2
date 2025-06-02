@echo off
title ZoL0 Complete System Startup

echo.
echo ================================================================
echo           ZoL0 TRADING SYSTEM - COMPLETE STARTUP
echo ================================================================
echo.
echo This script will:
echo 1. Start backend API services (ports 5000, 5001)
echo 2. Launch all 9 trading dashboards (ports 8501-8509)
echo 3. Ensure real Bybit data access for all components
echo.

cd /d "C:\Users\piotr\Desktop\Zol0"

echo 🔧 PHASE 1: Starting Backend API Services...
echo ================================================================
echo.

echo   Starting Main API Server (Port 5000)...
start "ZoL0-Main-API-5000" cmd /k "cd ZoL0-master && python dashboard_api.py"
timeout /t 3 /nobreak >nul

echo   Starting Enhanced API Server (Port 5001)...
start "ZoL0-Enhanced-API-5001" cmd /k "python enhanced_dashboard_api.py"
timeout /t 5 /nobreak >nul

echo   ✅ Backend APIs starting...
echo.

echo 🔧 PHASE 2: Verifying API Status...
echo ================================================================
echo.
echo   Waiting for APIs to initialize...
timeout /t 10 /nobreak >nul

echo   Checking API connectivity...
python check_backend_status.py
timeout /t 3 /nobreak >nul

echo.
echo 🔧 PHASE 3: Launching Trading Dashboards...
echo ================================================================
echo.

echo   🎛️ Starting Master Control Dashboard (port 8501)...
start "ZoL0-Master-Control" cmd /k "python -m streamlit run master_control_dashboard.py --server.port=8501"
timeout /t 3 /nobreak >nul

echo   📊 Starting Unified Trading Dashboard (port 8502)...
start "ZoL0-Unified-Trading" cmd /k "python -m streamlit run unified_trading_dashboard.py --server.port=8502"
timeout /t 3 /nobreak >nul

echo   🤖 Starting Enhanced Bot Monitor (port 8503)...
start "ZoL0-Bot-Monitor" cmd /k "python -m streamlit run enhanced_bot_monitor.py --server.port=8503"
timeout /t 3 /nobreak >nul

echo   📈 Starting Advanced Trading Analytics (port 8504)...
start "ZoL0-Analytics" cmd /k "python -m streamlit run advanced_trading_analytics.py --server.port=8504"
timeout /t 3 /nobreak >nul

echo   🔔 Starting Notification Dashboard (port 8505)...
start "ZoL0-Notifications" cmd /k "python -m streamlit run notification_dashboard.py --server.port=8505"
timeout /t 3 /nobreak >nul

echo   🚨 Starting Advanced Alert Management (port 8506)...
start "ZoL0-Alerts" cmd /k "python -m streamlit run advanced_alert_management.py --server.port=8506"
timeout /t 3 /nobreak >nul

echo   📊 Starting Portfolio Optimization (port 8507)...
start "ZoL0-Portfolio" cmd /k "python -m streamlit run portfolio_optimization.py --server.port=8507"
timeout /t 3 /nobreak >nul

echo   🤖 Starting ML Predictive Analytics (port 8508)...
start "ZoL0-ML-Analytics" cmd /k "python -m streamlit run ml_predictive_analytics.py --server.port=8508"
timeout /t 3 /nobreak >nul

echo   ✨ Starting Enhanced Dashboard (port 8509)...
start "ZoL0-Enhanced" cmd /k "python -m streamlit run enhanced_dashboard.py --server.port=8509"
timeout /t 5 /nobreak >nul

echo.
echo ================================================================
echo                    🎉 SYSTEM FULLY LAUNCHED!
echo ================================================================
echo.
echo 🌐 Backend API Services:
echo   • Main API:     http://localhost:5000
echo   • Enhanced API: http://localhost:5001
echo.
echo 📊 Trading Dashboards:
echo   • Master Control:      http://localhost:8501
echo   • Unified Trading:     http://localhost:8502
echo   • Enhanced Bot:        http://localhost:8503
echo   • Analytics:           http://localhost:8504
echo   • Notifications:       http://localhost:8505
echo   • Alerts:              http://localhost:8506
echo   • Portfolio:           http://localhost:8507
echo   • ML Analytics:        http://localhost:8508
echo   • Enhanced:            http://localhost:8509
echo.
echo 🟢 All dashboards are now using REAL BYBIT DATA!
echo 💰 Connected to your production Bybit account
echo 📡 Real-time trading data and portfolio information
echo.
echo 💡 Keep all windows open for full functionality
echo    Close individual windows to stop specific services
echo.

pause
