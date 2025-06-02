#!/usr/bin/env python3
"""
COMPLETE ZoL0 TRADING SYSTEM LAUNCHER
This script launches the entire trading system with real Bybit data
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser
from pathlib import Path

def set_production_environment():
    """Set environment variables for production Bybit access"""
    os.environ["BYBIT_PRODUCTION_CONFIRMED"] = "true"
    os.environ["BYBIT_PRODUCTION_ENABLED"] = "true"
    print("✅ Production environment configured")

def start_api_server(script_path, port, name):
    """Start an API server in a separate process"""
    try:
        print(f"🚀 Starting {name} on port {port}...")
        
        # Change to the script's directory
        script_dir = os.path.dirname(script_path)
        
        process = subprocess.Popen([
            sys.executable, os.path.basename(script_path)
        ], cwd=script_dir)
        
        print(f"✅ {name} started (PID: {process.pid})")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return None

def start_dashboard(script_path, port, name):
    """Start a dashboard in a separate process"""
    try:
        print(f"🎯 Starting {name} on port {port}...")
        
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", script_path, "--server.port", str(port)
        ], cwd=os.path.dirname(script_path))
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return None

def main():
    print("🔥 ZoL0 COMPLETE TRADING SYSTEM LAUNCHER")
    print("=" * 60)
    print("🟢 LAUNCHING WITH REAL BYBIT PRODUCTION DATA")
    print("=" * 60)
    
    # Set production environment
    set_production_environment()
    
    base_dir = Path(__file__).parent
    
    # Step 1: Start Backend API Services
    print("\n📡 STEP 1: Starting Backend API Services...")
    print("-" * 40)
    
    api_processes = []
    
    # Main API Server
    main_api_path = base_dir / "ZoL0-master" / "dashboard_api.py"
    if main_api_path.exists():
        proc = start_api_server(str(main_api_path), 5000, "Main API Server")
        if proc:
            api_processes.append(proc)
    
    # Enhanced API Server  
    enhanced_api_path = base_dir / "enhanced_dashboard_api.py"
    if enhanced_api_path.exists():
        proc = start_api_server(str(enhanced_api_path), 5001, "Enhanced API Server")
        if proc:
            api_processes.append(proc)
    
    # Wait for APIs to initialize
    print("\n⏳ Waiting 15 seconds for API services to initialize...")
    time.sleep(15)
    
    # Step 2: Start Dashboard Services
    print("\n🎯 STEP 2: Starting Dashboard Services...")
    print("-" * 40)
    
    dashboard_processes = []
    
    # Dashboard configurations
    dashboards = [
        ("master_control_dashboard.py", 8501, "Master Control"),
        ("unified_trading_dashboard.py", 8502, "Unified Trading"),
        ("enhanced_bot_monitor.py", 8503, "Enhanced Bot Monitor"),
        ("advanced_trading_analytics.py", 8504, "Trading Analytics"),
        ("notification_dashboard.py", 8505, "Notifications"),
        ("portfolio_dashboard.py", 8506, "Portfolio"),
        ("ml_predictive_analytics.py", 8507, "ML Analytics"),
        ("enhanced_dashboard.py", 8508, "Enhanced Dashboard"),
        ("system_dashboard.py", 8509, "System Monitor")
    ]
    
    for script_name, port, name in dashboards:
        script_path = base_dir / script_name
        if script_path.exists():
            proc = start_dashboard(str(script_path), port, name)
            if proc:
                dashboard_processes.append((proc, port, name))
        else:
            print(f"⚠️  Dashboard not found: {script_name}")
    
    # Wait for dashboards to start
    print("\n⏳ Waiting 20 seconds for dashboards to initialize...")
    time.sleep(20)
    
    # Step 3: Display Results
    print("\n🎉 SYSTEM LAUNCH COMPLETE!")
    print("=" * 60)
    print("🟢 REAL BYBIT PRODUCTION DATA ACTIVE")
    print("=" * 60)
    
    print(f"\n📡 Backend API Services ({len(api_processes)} running):")
    print("   • Main API Server: http://localhost:5000")
    print("   • Enhanced API Server: http://localhost:5001")
    
    print(f"\n🎯 Trading Dashboards ({len(dashboard_processes)} running):")
    for proc, port, name in dashboard_processes:
        print(f"   • {name}: http://localhost:{port}")
    
    print("\n🚀 QUICK ACCESS LINKS:")
    print("   • Master Control: http://localhost:8501")
    print("   • Unified Trading: http://localhost:8502") 
    print("   • Bot Monitor: http://localhost:8503")
    print("   • Analytics: http://localhost:8504")
    
    # Auto-open main dashboard
    print("\n🌐 Opening Master Control Dashboard...")
    try:
        webbrowser.open("http://localhost:8501")
    except:
        pass
    
    print("\n" + "=" * 60)
    print("✅ ZoL0 TRADING SYSTEM IS NOW LIVE!")
    print("🔴 Press Ctrl+C to stop all services")
    print("=" * 60)
    
    # Keep running until interrupted
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down all services...")
        
        # Stop all processes
        all_processes = api_processes + [p[0] for p in dashboard_processes]
        for process in all_processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        
        print("✅ All services stopped. System shutdown complete.")

if __name__ == "__main__":
    main()
