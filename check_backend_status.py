#!/usr/bin/env python3
"""
ZoL0 Backend Services Status Checker
Verifies that backend API services are running and accessible
"""

import requests
import time
from datetime import datetime

def check_api_endpoint(url, name, timeout=5):
    """Check if an API endpoint is responding"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return True, f"✅ {name} - RUNNING (Status: {response.status_code})"
        else:
            return False, f"❌ {name} - ERROR (Status: {response.status_code})"
    except requests.exceptions.ConnectionError:
        return False, f"❌ {name} - NOT RUNNING (Connection refused)"
    except requests.exceptions.Timeout:
        return False, f"❌ {name} - TIMEOUT (No response in {timeout}s)"
    except Exception as e:
        return False, f"❌ {name} - ERROR ({str(e)})"

def check_api_health(url, name):
    """Check API health endpoints"""
    health_endpoints = [
        "/api/health",
        "/health", 
        "/api/status",
        "/status"
    ]
    
    for endpoint in health_endpoints:
        try:
            response = requests.get(f"{url}{endpoint}", timeout=3)
            if response.status_code == 200:
                data = response.json()
                return True, f"✅ {name} Health Check - OK ({endpoint})"
        except:
            continue
    
    return False, f"🟡 {name} - No health endpoint found"

def main():
    print("🔍 ZoL0 Backend Services Status Check")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Define API endpoints to check
    apis = [
        ("http://localhost:5000", "Main API Server"),
        ("http://localhost:5001", "Enhanced API Server")
    ]
    
    all_running = True
    
    print("📡 Checking Backend API Services...")
    print("-" * 40)
    
    for url, name in apis:
        running, message = check_api_endpoint(url, name)
        print(message)
        
        if running:
            health_ok, health_msg = check_api_health(url, name)
            print(f"   {health_msg}")
        
        all_running = all_running and running
        print()
    
    # Check specific endpoints if APIs are running
    if all_running:
        print("🧪 Testing Specific Endpoints...")
        print("-" * 40)
        
        # Test main API endpoints
        test_endpoints = [
            ("http://localhost:5000/api/portfolio", "Portfolio Data"),
            ("http://localhost:5000/api/trading/status", "Trading Status"),
            ("http://localhost:5001/api/portfolio", "Enhanced Portfolio"),
            ("http://localhost:5001/api/trading/statistics", "Trading Stats")
        ]
        
        for url, name in test_endpoints:
            running, message = check_api_endpoint(url, name)
            print(message)
    
    print()
    print("📊 Dashboard Connectivity Check...")
    print("-" * 40)
    
    if all_running:
        print("✅ Backend APIs are RUNNING - Dashboards will use REAL DATA")
        print("🟢 Data Source: Production Bybit API")
        print()
        print("🚀 You can now start your dashboards:")
        print("   • Run: python launch_all_dashboards.py")
        print("   • Or: launch_all_dashboards.bat")
        print()
        print("📱 Dashboard URLs:")
        for i, port in enumerate(range(8501, 8510), 1):
            print(f"   • Dashboard {i}: http://localhost:{port}")
    else:
        print("❌ Backend APIs are NOT RUNNING - Dashboards will use SYNTHETIC DATA")
        print("🟡 Data Source: Fallback/Demo Data")
        print()
        print("🔧 To fix this:")
        print("   1. Run: START_BACKEND_SERVICES.bat")
        print("   2. Or: powershell -ExecutionPolicy Bypass -File Start-BackendServices.ps1")
        print("   3. Wait 10 seconds, then re-run this check")
    
    print()
    print("=" * 50)

if __name__ == "__main__":
    main()
