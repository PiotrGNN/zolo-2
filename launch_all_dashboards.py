#!/usr/bin/env python3
"""
ZoL0 Platform Launcher - Uruchom wszystkie dashboardy z prawdziwymi danymi Bybit
Launch all ZoL0 dashboards with real Bybit data
"""

import subprocess
import time
import sys
import os
from pathlib import Path

# Konfiguracja dashboardów
DASHBOARDS = [
    {"name": "Master Control Dashboard", "file": "master_control_dashboard.py", "port": 8501, "icon": "🎛️"},
    {"name": "Unified Trading Dashboard", "file": "unified_trading_dashboard.py", "port": 8502, "icon": "📊"},
    {"name": "Enhanced Bot Monitor", "file": "enhanced_bot_monitor.py", "port": 8503, "icon": "🤖"},
    {"name": "Advanced Trading Analytics", "file": "advanced_trading_analytics.py", "port": 8504, "icon": "📈"},
    {"name": "Notification Dashboard", "file": "notification_dashboard.py", "port": 8505, "icon": "🔔"},
    {"name": "Advanced Alert Management", "file": "advanced_alert_management.py", "port": 8506, "icon": "🚨"},
    {"name": "Portfolio Optimization", "file": "portfolio_optimization.py", "port": 8507, "icon": "📊"},
    {"name": "ML Predictive Analytics", "file": "ml_predictive_analytics.py", "port": 8508, "icon": "🤖"},
    {"name": "Enhanced Dashboard", "file": "enhanced_dashboard.py", "port": 8509, "icon": "✨"}
]

def check_port_available(port):
    """Sprawdź czy port jest dostępny"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0

def launch_dashboard(dashboard):
    """Uruchom pojedynczy dashboard"""
    try:
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            dashboard["file"], 
            f"--server.port={dashboard['port']}", 
            "--server.headless=true",
            "--server.runOnSave=false",
            "--server.fileWatcherType=none",
            "--browser.gatherUsageStats=false"
        ]
        
        print(f"🚀 Uruchamianie {dashboard['icon']} {dashboard['name']} na porcie {dashboard['port']}...")
        
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
        )
        
        return process
        
    except Exception as e:
        print(f"❌ Błąd uruchamiania {dashboard['name']}: {e}")
        return None

def main():
    print("🚀 ZoL0 PLATFORM LAUNCHER")
    print("=" * 50)
    print("🔗 Uruchamianie wszystkich dashboardów z prawdziwymi danymi Bybit...")
    print()
    
    # Sprawdź czy jesteśmy w odpowiednim katalogu
    if not Path("master_control_dashboard.py").exists():
        print("❌ Nie znaleziono plików dashboardów. Upewnij się, że jesteś w katalogu ZoL0.")
        return
    
    processes = []
    failed_launches = []
    
    # Uruchom każdy dashboard
    for dashboard in DASHBOARDS:
        if not Path(dashboard["file"]).exists():
            print(f"⚠️  Plik {dashboard['file']} nie istnieje, pomijam...")
            continue
            
        if not check_port_available(dashboard["port"]):
            print(f"⚠️  Port {dashboard['port']} jest zajęty, pomijam {dashboard['name']}...")
            continue
            
        process = launch_dashboard(dashboard)
        if process:
            processes.append((dashboard, process))
            time.sleep(2)  # Poczekaj między uruchomieniami
        else:
            failed_launches.append(dashboard)
    
    print()
    print("✅ URUCHOMIONO DASHBOARDY:")
    print("-" * 50)
    
    for dashboard, process in processes:
        print(f"{dashboard['icon']} {dashboard['name']}")
        print(f"   🌐 http://localhost:{dashboard['port']}")
        print()
    
    if failed_launches:
        print("❌ NIEUDANE URUCHOMIENIA:")
        for dashboard in failed_launches:
            print(f"   {dashboard['icon']} {dashboard['name']}")
        print()
    
    print("🎉 PLATFORMA ZoL0 URUCHOMIONA!")
    print("📡 Wszystkie dashboardy używają prawdziwych danych z Bybit Production API")
    print()
    print("💡 GŁÓWNE LINKI:")
    print(f"   🎛️  Master Control: http://localhost:8501")
    print(f"   📊 Trading Dashboard: http://localhost:8502")
    print(f"   🤖 Bot Monitor: http://localhost:8503")
    print()
    print("🔧 Aby zatrzymać wszystkie dashboardy, naciśnij Ctrl+C")
    
    try:
        # Czekaj na signal zatrzymania
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Zatrzymywanie wszystkich dashboardów...")
        
        for dashboard, process in processes:
            try:
                process.terminate()
                print(f"✅ Zatrzymano {dashboard['name']}")
            except:
                pass
        
        print("👋 ZoL0 Platform zatrzymana.")

if __name__ == "__main__":
    main()
