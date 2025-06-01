#!/usr/bin/env python3
"""
ZoL0 Quick Start - Unified Dashboard
===================================
Szybkie uruchomienie zunifikowanego dashboardu z minimalną konfiguracją.
Uruchamia tylko niezbędne serwisy.
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path
import threading

def check_requirements():
    """Sprawdź wymagania systemowe"""
    try:
        import streamlit
        import requests
        import pandas
        import numpy
        import plotly
        return True
    except ImportError as e:
        print(f"❌ Brakuje wymaganego pakietu: {e}")
        print("💡 Uruchom: pip install streamlit requests pandas numpy plotly")
        return False

def start_enhanced_api():
    """Uruchom Enhanced Dashboard API w tle"""
    api_path = Path(__file__).parent / "enhanced_dashboard_api.py"
    if not api_path.exists():
        print("⚠️  Enhanced Dashboard API nie znaleziony")
        return None
    
    print("🔧 Uruchamianie Enhanced Dashboard API...")
    try:
        process = subprocess.Popen([
            sys.executable, str(api_path)
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Poczekaj chwilę na uruchomienie
        time.sleep(3)
        
        # Sprawdź czy API odpowiada
        import requests
        try:
            response = requests.get("http://localhost:5001/health", timeout=5)
            if response.status_code == 200:
                print("✅ Enhanced Dashboard API uruchomiony (port 5001)")
                return process
            else:
                print("⚠️  API uruchomiony ale nie odpowiada poprawnie")
                return process
        except:
            print("⚠️  Nie można połączyć się z API")
            return process
    except Exception as e:
        print(f"❌ Błąd uruchamiania API: {e}")
        return None

def start_unified_dashboard():
    """Uruchom zunifikowany dashboard"""
    dashboard_path = Path(__file__).parent / "unified_trading_dashboard.py"
    if not dashboard_path.exists():
        print("❌ unified_trading_dashboard.py nie znaleziony")
        return False
      print("🚀 Uruchamianie Unified Trading Dashboard...")
    print("📱 URL: http://localhost:8512")
    print("⏹️  Zatrzymanie: Ctrl+C")
    
    # Otwórz przeglądarkę po 3 sekundach
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open("http://localhost:8512")
        except:
            pass
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:        # Uruchom Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            str(dashboard_path),
            "--server.port", "8512",
            "--theme.base", "dark",
            "--theme.primaryColor", "#667eea",
            "--browser.gatherUsageStats", "false"
        ]
        
        subprocess.run(cmd)
        return True
    except KeyboardInterrupt:
        print("\n👋 Dashboard zatrzymany")
        return True
    except Exception as e:
        print(f"❌ Błąd uruchamiania dashboardu: {e}")
        return False

def main():
    """Główna funkcja"""
    print("🚀 ZoL0 Unified Trading Dashboard - Quick Start")
    print("=" * 60)
    print("✨ Ten skrypt uruchomi JEDEN dashboard z wszystkimi funkcjami")
    print("💡 Nie potrzebujesz uruchamiać osobnych serwisów")
    print()
    
    # Sprawdź wymagania
    if not check_requirements():
        input("Naciśnij Enter aby zakończyć...")
        return
    
    # Uruchom API w tle
    api_process = start_enhanced_api()
    
    try:
        # Uruchom dashboard
        success = start_unified_dashboard()
        
    finally:
        # Wyczyść procesy
        if api_process:
            try:
                api_process.terminate()
                print("🔧 Enhanced Dashboard API zatrzymany")
            except:
                pass

if __name__ == "__main__":
    main()
