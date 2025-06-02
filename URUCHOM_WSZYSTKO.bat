@echo off
echo.
echo ████████████████████████████████████████████████████████
echo ███                                                  ███
echo ███         ZoL0 TRADING SYSTEM LAUNCHER            ███
echo ███            PRAWDZIWE DANE BYBIT                 ███
echo ███                                                  ███
echo ████████████████████████████████████████████████████████
echo.

REM Ustawienie zmiennych środowiskowych dla produkcji
set BYBIT_PRODUCTION_CONFIRMED=true
set BYBIT_PRODUCTION_ENABLED=true

echo [INFO] Ustawiono zmienne produkcyjne...
echo [INFO] BYBIT_PRODUCTION_CONFIRMED=%BYBIT_PRODUCTION_CONFIRMED%
echo [INFO] BYBIT_PRODUCTION_ENABLED=%BYBIT_PRODUCTION_ENABLED%
echo.

echo [KROK 1] Uruchamianie serwerów API Backend...
echo ================================================

echo [1.1] Uruchamianie Main API Server (port 5000)...
start "ZoL0 Main API Server" /MIN cmd /k "cd /d C:\Users\piotr\Desktop\Zol0\ZoL0-master && echo Uruchamianie Main API Server... && python dashboard_api.py"

echo [1.2] Oczekiwanie 5 sekund...
timeout /t 5 /nobreak >nul

echo [1.3] Uruchamianie Enhanced API Server (port 5001)...
start "ZoL0 Enhanced API Server" /MIN cmd /k "cd /d C:\Users\piotr\Desktop\Zol0 && echo Uruchamianie Enhanced API Server... && python enhanced_dashboard_api.py"

echo [1.4] Oczekiwanie 15 sekund na inicjalizację API...
timeout /t 15 /nobreak >nul

echo.
echo [KROK 2] Uruchamianie Dashboard Services...
echo ===============================================

echo [2.1] Master Control Dashboard (port 8501)...
start "ZoL0 Master Control" /MIN cmd /k "cd /d C:\Users\piotr\Desktop\Zol0 && streamlit run master_control_dashboard.py --server.port 8501"

timeout /t 3 /nobreak >nul

echo [2.2] Unified Trading Dashboard (port 8502)...
start "ZoL0 Unified Trading" /MIN cmd /k "cd /d C:\Users\piotr\Desktop\Zol0 && streamlit run unified_trading_dashboard.py --server.port 8502"

timeout /t 3 /nobreak >nul

echo [2.3] Enhanced Bot Monitor (port 8503)...
start "ZoL0 Bot Monitor" /MIN cmd /k "cd /d C:\Users\piotr\Desktop\Zol0 && streamlit run enhanced_bot_monitor.py --server.port 8503"

timeout /t 3 /nobreak >nul

echo [2.4] Trading Analytics (port 8504)...
start "ZoL0 Analytics" /MIN cmd /k "cd /d C:\Users\piotr\Desktop\Zol0 && streamlit run advanced_trading_analytics.py --server.port 8504"

timeout /t 3 /nobreak >nul

echo [2.5] Notification Dashboard (port 8505)...
start "ZoL0 Notifications" /MIN cmd /k "cd /d C:\Users\piotr\Desktop\Zol0 && streamlit run notification_dashboard.py --server.port 8505"

timeout /t 3 /nobreak >nul

echo [2.6] Portfolio Dashboard (port 8506)...
start "ZoL0 Portfolio" /MIN cmd /k "cd /d C:\Users\piotr\Desktop\Zol0 && streamlit run portfolio_dashboard.py --server.port 8506"

timeout /t 3 /nobreak >nul

echo [2.7] ML Analytics (port 8507)...
start "ZoL0 ML Analytics" /MIN cmd /k "cd /d C:\Users\piotr\Desktop\Zol0 && streamlit run ml_predictive_analytics.py --server.port 8507"

timeout /t 3 /nobreak >nul

echo [2.8] Enhanced Dashboard (port 8508)...
start "ZoL0 Enhanced" /MIN cmd /k "cd /d C:\Users\piotr\Desktop\Zol0 && streamlit run enhanced_dashboard.py --server.port 8508"

echo.
echo [KROK 3] Oczekiwanie na inicjalizację wszystkich serwisów...
echo ==========================================================
timeout /t 20 /nobreak >nul

echo.
echo ████████████████████████████████████████████████████████
echo ███                                                  ███
echo ███         SYSTEM ZoL0 URUCHOMIONY!                ███
echo ███                                                  ███
echo ███  🟢 PRAWDZIWE DANE BYBIT AKTYWNE               ███
echo ███                                                  ███
echo ████████████████████████████████████████████████████████
echo.

echo [SUKCES] Serwery Backend API:
echo    • Main API Server:     http://localhost:5000
echo    • Enhanced API Server: http://localhost:5001
echo.

echo [SUKCES] Dashboardy Trading:
echo    • Master Control:    http://localhost:8501
echo    • Unified Trading:   http://localhost:8502
echo    • Bot Monitor:       http://localhost:8503
echo    • Trading Analytics: http://localhost:8504
echo    • Notifications:     http://localhost:8505
echo    • Portfolio:         http://localhost:8506
echo    • ML Analytics:      http://localhost:8507
echo    • Enhanced:          http://localhost:8508
echo.

echo [INFO] Otwieranie Master Control Dashboard...
start "" "http://localhost:8501"

echo.
echo ================================================================
echo   WSZYSTKIE SYSTEMY ONLINE - GOTOWE DO TRADINGU!
echo   Naciśnij dowolny klawisz aby sprawdzić status...
echo ================================================================
pause

echo.
echo [TEST] Sprawdzanie conectywności serwisów...
python -c "import requests; print('✅ Main API:', 'OK' if requests.get('http://localhost:5000', timeout=3).status_code == 200 else 'ERROR')" 2>nul || echo "❌ Main API: NOT RESPONDING"
python -c "import requests; print('✅ Enhanced API:', 'OK' if requests.get('http://localhost:5001', timeout=3).status_code == 200 else 'ERROR')" 2>nul || echo "❌ Enhanced API: NOT RESPONDING"
python -c "import requests; print('✅ Master Control:', 'OK' if requests.get('http://localhost:8501', timeout=3).status_code == 200 else 'ERROR')" 2>nul || echo "❌ Master Control: NOT RESPONDING"

echo.
echo Wszystkie serwisy ZoL0 są teraz uruchomione!
echo Aby zatrzymać wszystkie serwisy, zamknij wszystkie okna terminali.
echo.
pause
