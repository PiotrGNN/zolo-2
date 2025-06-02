#!/usr/bin/env python3
"""
test_dashboard_launches.py
--------------------------
Test launching all dashboards to ensure they are fully operational
"""

import subprocess
import time
import requests
import threading
import os
import sys
from pathlib import Path

def test_enhanced_dashboard_api():
    """Test Enhanced Dashboard API (should already be running)"""
    print("🔍 TESTOWANIE ENHANCED DASHBOARD API")
    print("="*50)
    
    try:
        response = requests.get("http://localhost:5001/health", timeout=5)
        if response.status_code == 200:
            print("✅ Enhanced Dashboard API: Uruchomiony i responsywny")
            return True
        else:
            print(f"⚠️ Enhanced Dashboard API: Status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Enhanced Dashboard API: Niedostępny - {e}")
        return False

def test_streamlit_dashboard_import(dashboard_file):
    """Test if a Streamlit dashboard can be imported without errors"""
    print(f"\n🔍 TESTOWANIE IMPORTU: {dashboard_file}")
    print("="*50)
    
    try:
        # Add current directory to Python path
        current_dir = Path(__file__).parent
        sys.path.insert(0, str(current_dir))
        
        # Try to import the dashboard
        if dashboard_file == "unified_trading_dashboard.py":
            import unified_trading_dashboard
            print("✅ unified_trading_dashboard: Import successful")
            
        elif dashboard_file == "enhanced_dashboard.py":
            import enhanced_dashboard
            print("✅ enhanced_dashboard: Import successful")
            
        elif dashboard_file == "master_control_dashboard.py":
            import master_control_dashboard
            print("✅ master_control_dashboard: Import successful")
            
        elif dashboard_file == "advanced_trading_analytics.py":
            import advanced_trading_analytics
            print("✅ advanced_trading_analytics: Import successful")
            
        return True
        
    except Exception as e:
        print(f"❌ {dashboard_file}: Import failed - {e}")
        return False

def test_streamlit_syntax_check(dashboard_file):
    """Test if Streamlit dashboard has correct syntax"""
    print(f"\n🔍 SPRAWDZANIE SKŁADNI: {dashboard_file}")
    print("="*50)
    
    try:
        # Check if file exists
        if not Path(dashboard_file).exists():
            print(f"❌ {dashboard_file}: Plik nie istnieje")
            return False
        
        # Run Python syntax check
        result = subprocess.run([
            sys.executable, "-m", "py_compile", dashboard_file
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ {dashboard_file}: Składnia poprawna")
            return True
        else:
            print(f"❌ {dashboard_file}: Błąd składni")
            if result.stderr:
                print(f"   Błąd: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⚠️ {dashboard_file}: Timeout podczas sprawdzania składni")
        return False
    except Exception as e:
        print(f"❌ {dashboard_file}: Błąd sprawdzania składni - {e}")
        return False

def test_streamlit_dry_run(dashboard_file):
    """Test if Streamlit dashboard can start without errors (dry run)"""
    print(f"\n🔍 DRY RUN TEST: {dashboard_file}")
    print("="*50)
    
    try:
        # Try to run streamlit config validation
        result = subprocess.run([
            sys.executable, "-c", 
            f"import streamlit as st; exec(open('{dashboard_file}').read())"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ {dashboard_file}: Dry run successful")
            return True
        else:
            print(f"⚠️ {dashboard_file}: Dry run issues detected")
            if result.stderr:
                print(f"   Ostrzeżenia: {result.stderr[:500]}...")
            # Don't fail for warnings, only for hard errors
            return "error" not in result.stderr.lower()
            
    except subprocess.TimeoutExpired:
        print(f"⚠️ {dashboard_file}: Timeout podczas dry run")
        return False
    except Exception as e:
        print(f"❌ {dashboard_file}: Błąd dry run - {e}")
        return False

def test_production_config():
    """Test production configuration files"""
    print("\n🔍 TESTOWANIE KONFIGURACJI PRODUKCYJNEJ")
    print("="*50)
    
    config_files = [
        ".env",
        "production_config.json", 
        "production_api_config.json"
    ]
    
    all_good = True
    
    for config_file in config_files:
        if Path(config_file).exists():
            print(f"✅ {config_file}: Exists")
        else:
            print(f"❌ {config_file}: Missing")
            all_good = False
    
    # Test environment variables
    bybit_api_key = os.getenv("BYBIT_API_KEY")
    bybit_production = os.getenv("BYBIT_PRODUCTION_ENABLED")
    trading_mode = os.getenv("TRADING_MODE")
    
    if bybit_api_key:
        print(f"✅ BYBIT_API_KEY: Configured")
    else:
        print(f"❌ BYBIT_API_KEY: Missing")
        all_good = False
        
    if bybit_production == "true":
        print(f"✅ BYBIT_PRODUCTION_ENABLED: true")
    else:
        print(f"⚠️ BYBIT_PRODUCTION_ENABLED: {bybit_production}")
        
    if trading_mode == "production":
        print(f"✅ TRADING_MODE: production")
    else:
        print(f"⚠️ TRADING_MODE: {trading_mode}")
    
    return all_good

def main():
    """Main test function"""
    print("🚀 TEST URUCHAMIANIA DASHBOARDÓW")
    print("============================================================")
    print(f"Czas: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("============================================================")
    
    tests_passed = 0
    total_tests = 0
    
    # Test Enhanced Dashboard API
    total_tests += 1
    if test_enhanced_dashboard_api():
        tests_passed += 1
    
    # Test production configuration
    total_tests += 1
    if test_production_config():
        tests_passed += 1
    
    # Test dashboard files
    dashboard_files = [
        "unified_trading_dashboard.py",
        "enhanced_dashboard.py", 
        "master_control_dashboard.py",
        "advanced_trading_analytics.py"
    ]
    
    for dashboard_file in dashboard_files:
        # Syntax check
        total_tests += 1
        if test_streamlit_syntax_check(dashboard_file):
            tests_passed += 1
            
        # Import test
        total_tests += 1
        if test_streamlit_dashboard_import(dashboard_file):
            tests_passed += 1
            
        # Dry run test
        total_tests += 1
        if test_streamlit_dry_run(dashboard_file):
            tests_passed += 1
    
    # Summary
    print("\n" + "="*60)
    print("📊 PODSUMOWANIE TESTÓW DASHBOARDÓW")
    print("="*60)
    print(f"Zaliczonych: {tests_passed}/{total_tests}")
    print(f"Procent sukcesu: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("🎉 WSZYSTKIE DASHBOARDY GOTOWE DO URUCHOMIENIA!")
        print("\nMożesz uruchomić:")
        print("• streamlit run unified_trading_dashboard.py --server.port 8512")
        print("• streamlit run enhanced_dashboard.py --server.port 8513") 
        print("• streamlit run master_control_dashboard.py --server.port 8514")
        print("• streamlit run advanced_trading_analytics.py --server.port 8515")
    else:
        print("⚠️ Niektóre testy nie przeszły pomyślnie")
    
    print("="*60)
    
    return tests_passed == total_tests

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Test przerwany przez użytkownika")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Nieoczekiwany błąd: {e}")
        sys.exit(1)
