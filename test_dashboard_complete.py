#!/usr/bin/env python3
"""
Complete Dashboard Control Panel Test
Kompletny test panelu kontrolnego dashboard
"""

import requests
import json
import time
from datetime import datetime

def test_dashboard_api():
    """Test wszystkich funkcji Dashboard API"""
    base_url = "http://localhost:5001"
    results = {}
    
    print("=" * 70)
    print("🎯 ZoL0 Dashboard Control Panel - Complete Test")
    print("=" * 70)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['status']}")
            results["health"] = True
        else:
            print(f"❌ Health Check failed: {response.status_code}")
            results["health"] = False
    except Exception as e:
        print(f"❌ Health Check error: {e}")
        results["health"] = False
    
    # Test 2: Environment Status
    print("\n2️⃣ Testing Environment Management...")
    try:
        response = requests.get(f"{base_url}/api/environment/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Current Environment: {data.get('current_environment', 'unknown')}")
            print(f"📊 Production Ready: {data.get('production_ready', False)}")
            results["environment"] = True
        else:
            print(f"❌ Environment status failed: {response.status_code}")
            results["environment"] = False
    except Exception as e:
        print(f"❌ Environment status error: {e}")
        results["environment"] = False
    
    # Test 3: Trading Engine Status
    print("\n3️⃣ Testing Trading Engine...")
    try:
        response = requests.get(f"{base_url}/api/trading/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Trading Engine Active: {data.get('status', {}).get('active', False)}")
            print(f"📈 Trading Pairs: {data.get('status', {}).get('trading_pairs', [])}")
            results["trading_engine"] = True
        else:
            print(f"❌ Trading engine status failed: {response.status_code}")
            results["trading_engine"] = False
    except Exception as e:
        print(f"❌ Trading engine status error: {e}")
        results["trading_engine"] = False
      # Test 4: Trading Engine Control
    print("\n4️⃣ Testing Trading Engine Control...")
    try:
        # Test start with proper headers
        response = requests.post(f"{base_url}/api/trading/start", 
                               headers={'Content-Type': 'application/json'},
                               json={})
        if response.status_code == 200:
            print("✅ Trading Engine Start command successful")
            
            # Wait a moment
            time.sleep(1)
            
            # Test stop
            response = requests.post(f"{base_url}/api/trading/stop",
                                   headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                print("✅ Trading Engine Stop command successful")
                results["trading_control"] = True
            else:
                print(f"❌ Trading Engine Stop failed: {response.status_code}")
                results["trading_control"] = False
        else:
            print(f"❌ Trading Engine Start failed: {response.status_code}")
            results["trading_control"] = False
    except Exception as e:
        print(f"❌ Trading Engine Control error: {e}")
        results["trading_control"] = False
    
    # Test 5: System Validation
    print("\n5️⃣ Testing System Validation...")
    try:
        response = requests.get(f"{base_url}/api/system/validation")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ System Validation successful")
            print(f"📊 Ready for Production: {data.get('ready_for_production', False)}")
            print(f"🔧 Components: {list(data.get('components', {}).keys())}")
            results["system_validation"] = True
        else:
            print(f"❌ System Validation failed: {response.status_code}")
            results["system_validation"] = False
    except Exception as e:
        print(f"❌ System Validation error: {e}")
        results["system_validation"] = False
    
    # Test 6: Core System APIs
    print("\n6️⃣ Testing Core System APIs...")
    core_endpoints = ["/core/status", "/core/strategies", "/core/ai-models", "/core/system-metrics"]
    core_success = 0
    
    for endpoint in core_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            if response.status_code == 200:
                print(f"✅ {endpoint}")
                core_success += 1
            else:
                print(f"❌ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")
    
    results["core_apis"] = core_success == len(core_endpoints)
    print(f"📊 Core API Success Rate: {(core_success/len(core_endpoints))*100:.1f}%")
    
    # Summary
    print("\n" + "=" * 70)
    print("🎉 TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(results.values())
    total = len(results)
    success_rate = (passed / total) * 100
    
    print(f"📊 Success Rate: {success_rate:.1f}%")
    print(f"✅ Passed Tests: {passed}/{total}")
    
    if success_rate >= 80:
        print("🎯 Overall Status: ✅ EXCELLENT")
        print("🚀 Dashboard Control Panel is fully functional!")
    elif success_rate >= 60:
        print("🎯 Overall Status: ⚠️ GOOD")
        print("🔧 Dashboard Control Panel is mostly functional with minor issues")
    else:
        print("🎯 Overall Status: ❌ NEEDS ATTENTION")
        print("🛠️ Dashboard Control Panel needs fixes")
    
    print("\nDetailed Results:")
    for test, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {test.replace('_', ' ').title()}")
    
    # Save results
    test_report = {
        "timestamp": datetime.now().isoformat(),
        "success_rate": success_rate,
        "results": results,
        "summary": {
            "passed": passed,
            "total": total,
            "status": "excellent" if success_rate >= 80 else "good" if success_rate >= 60 else "needs_attention"
        }
    }
    
    with open("logs/dashboard_complete_test.json", "w") as f:
        json.dump(test_report, f, indent=2)
    
    print(f"\n📄 Test report saved to: logs/dashboard_complete_test.json")
    print(f"🕐 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    test_dashboard_api()
