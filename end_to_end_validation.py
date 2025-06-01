#!/usr/bin/env python3
"""
End-to-End Validation Script for Real Data Integration
Tests the complete data flow from APIs to dashboard display
"""

import json
import requests
import time
from datetime import datetime

def test_enhanced_dashboard_api():
    """Test Enhanced Dashboard API endpoints"""
    print("🔍 Testing Enhanced Dashboard API...")
    
    base_url = "http://localhost:5001"
    endpoints = [
        "/health",
        "/api/portfolio", 
        "/core/status"
    ]
    
    results = {}
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            results[endpoint] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response_size": len(response.content)
            }
            if response.status_code == 200:
                print(f"  ✅ {endpoint} - OK")
            else:
                print(f"  ❌ {endpoint} - HTTP {response.status_code}")
        except Exception as e:
            results[endpoint] = {
                "success": False,
                "error": str(e)
            }
            print(f"  ❌ {endpoint} - Error: {e}")
    
    return results

def test_unified_dashboard_accessibility():
    """Test Unified Dashboard accessibility"""
    print("🔍 Testing Unified Trading Dashboard accessibility...")
    
    try:
        response = requests.get("http://localhost:8512", timeout=5)
        if response.status_code == 200:
            print("  ✅ Unified Dashboard accessible")
            return {"accessible": True, "status_code": 200}
        else:
            print(f"  ❌ Unified Dashboard HTTP {response.status_code}")
            return {"accessible": False, "status_code": response.status_code}
    except Exception as e:
        print(f"  ❌ Unified Dashboard connection error: {e}")
        return {"accessible": False, "error": str(e)}

def test_production_data_manager():
    """Test Production Data Manager"""
    print("🔍 Testing Production Data Manager...")
    
    try:
        from production_data_manager import get_production_data
        
        manager = get_production_data()
        print("  ✅ Production Data Manager initialized")
        
        # Test account balance
        balance_result = manager.get_account_balance()
        data_source = balance_result.get("data_source", "unknown")
        success = balance_result.get("success", False)
        
        print(f"  📊 Account Balance - Source: {data_source}, Success: {success}")
        
        # Test market data
        market_result = manager.get_market_data("BTCUSDT")
        market_source = market_result.get("data_source", "unknown")
        market_success = market_result.get("success", False)
        
        print(f"  📈 Market Data - Source: {market_source}, Success: {market_success}")
        
        return {
            "initialized": True,
            "account_balance": {
                "source": data_source,
                "success": success
            },
            "market_data": {
                "source": market_source,
                "success": market_success
            }
        }
        
    except Exception as e:
        print(f"  ❌ Production Data Manager error: {e}")
        return {"initialized": False, "error": str(e)}

def test_unified_dashboard_integration():
    """Test Unified Dashboard Real Data Integration"""
    print("🔍 Testing Unified Dashboard Real Data Integration...")
    
    try:
        from unified_trading_dashboard import UnifiedDashboard
        
        dashboard = UnifiedDashboard()
        print("  ✅ Unified Dashboard initialized")
        
        # Test performance data method
        perf_data = dashboard.get_unified_performance_data()
        data_source = perf_data.get("data_source", "unknown")
        
        print(f"  📊 Performance Data - Source: {data_source}")
        
        # Check if production manager is available
        has_production_manager = hasattr(dashboard, 'production_manager')
        print(f"  🔧 Production Manager Available: {has_production_manager}")
        
        return {
            "initialized": True,
            "performance_data_source": data_source,
            "has_production_manager": has_production_manager,
            "data_sample": perf_data
        }
        
    except Exception as e:
        print(f"  ❌ Unified Dashboard integration error: {e}")
        return {"initialized": False, "error": str(e)}

def generate_report(test_results):
    """Generate comprehensive validation report"""
    
    report = {
        "validation_timestamp": datetime.now().isoformat(),
        "test_results": test_results,
        "summary": {
            "enhanced_dashboard_api": test_results["enhanced_dashboard_api"].get("health", {}).get("success", False),
            "unified_dashboard_accessible": test_results["unified_dashboard"].get("accessible", False),
            "production_data_manager": test_results["production_data_manager"].get("initialized", False),
            "unified_integration": test_results["unified_integration"].get("initialized", False)
        }
    }
    
    # Determine overall data integration status
    data_sources = []
    if test_results["production_data_manager"].get("account_balance", {}).get("source"):
        data_sources.append(test_results["production_data_manager"]["account_balance"]["source"])
    if test_results["unified_integration"].get("performance_data_source"):
        data_sources.append(test_results["unified_integration"]["performance_data_source"])
    
    real_data_active = any(source in ["production_api", "api_endpoint"] for source in data_sources)
    
    report["summary"]["real_data_integration"] = real_data_active
    report["summary"]["data_sources_detected"] = list(set(data_sources))
    
    return report

def main():
    """Run complete end-to-end validation"""
    print("🚀 Starting End-to-End Validation of Real Data Integration")
    print("=" * 60)
    
    test_results = {}
    
    # Test Enhanced Dashboard API
    test_results["enhanced_dashboard_api"] = test_enhanced_dashboard_api()
    print()
    
    # Test Unified Dashboard accessibility
    test_results["unified_dashboard"] = test_unified_dashboard_accessibility()
    print()
    
    # Test Production Data Manager
    test_results["production_data_manager"] = test_production_data_manager()
    print()
    
    # Test Unified Dashboard Integration
    test_results["unified_integration"] = test_unified_dashboard_integration()
    print()
    
    # Generate final report
    print("📋 Generating Validation Report...")
    report = generate_report(test_results)
    
    # Save report
    with open("END_TO_END_VALIDATION_REPORT.json", "w") as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print("=" * 60)
    print("🎯 VALIDATION SUMMARY")
    print("=" * 60)
    
    summary = report["summary"]
    
    print(f"Enhanced Dashboard API: {'✅ OK' if summary['enhanced_dashboard_api'] else '❌ FAIL'}")
    print(f"Unified Dashboard Accessible: {'✅ OK' if summary['unified_dashboard_accessible'] else '❌ FAIL'}")
    print(f"Production Data Manager: {'✅ OK' if summary['production_data_manager'] else '❌ FAIL'}")
    print(f"Unified Integration: {'✅ OK' if summary['unified_integration'] else '❌ FAIL'}")
    print(f"Real Data Integration: {'✅ ACTIVE' if summary['real_data_integration'] else '⚠️  FALLBACK'}")
    
    if summary["data_sources_detected"]:
        print(f"Data Sources: {', '.join(summary['data_sources_detected'])}")
    
    print("\n📄 Full report saved to: END_TO_END_VALIDATION_REPORT.json")
    
    if summary["real_data_integration"]:
        print("\n🎉 SUCCESS: Real data integration is working!")
    else:
        print("\n⚠️  WARNING: System is using fallback/demo data")

if __name__ == "__main__":
    main()
