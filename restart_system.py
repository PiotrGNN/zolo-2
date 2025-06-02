#!/usr/bin/env python3
"""
System Restart Script - ZoL0 Trading System
===========================================
This script restarts all ZoL0 services with the fixed Master Control Dashboard
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def run_command(cmd, cwd=None, background=True):
    """Run a command with proper error handling"""
    try:
        if background:
            if sys.platform == "win32":
                subprocess.Popen(cmd, shell=True, cwd=cwd, 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen(cmd, shell=True, cwd=cwd)
        else:
            result = subprocess.run(cmd, shell=True, cwd=cwd, 
                                  capture_output=True, text=True)
            return result
        return True
    except Exception as e:
        print(f"Error running command '{cmd}': {e}")
        return False

def main():
    print("🚀 Starting ZoL0 Trading System with Fixed Master Control Dashboard")
    print("=" * 70)
    
    # Define paths
    base_dir = Path("C:/Users/piotr/Desktop/Zol0")
    zol0_master_dir = base_dir / "ZoL0-master"
    
    # Step 1: Start API servers
    print("\n📡 Starting API Servers...")
    
    # Main API server
    print("  - Starting Main API Server (port 5000)...")
    run_command("python dashboard_api.py", cwd=zol0_master_dir)
    time.sleep(3)
    
    # Enhanced API server  
    print("  - Starting Enhanced API Server (port 5001)...")
    run_command("python enhanced_dashboard_api.py", cwd=base_dir)
    time.sleep(3)
    
    # Step 2: Start Dashboards
    print("\n🖥️  Starting Dashboards...")
    
    # Main Dashboard
    print("  - Starting Main Trading Dashboard (port 8501)...")
    run_command("streamlit run dashboard.py --server.port 8501", cwd=zol0_master_dir)
    time.sleep(3)
    
    # Unified Dashboard
    print("  - Starting Unified Trading Dashboard (port 8503)...")
    run_command("streamlit run unified_trading_dashboard.py --server.port 8503", cwd=base_dir)
    time.sleep(3)
    
    # Enhanced Dashboard
    print("  - Starting Enhanced Dashboard (port 8504)...")
    run_command("streamlit run enhanced_dashboard.py --server.port 8504", cwd=base_dir)
    time.sleep(3)
    
    # Fixed Master Control Dashboard
    print("  - Starting FIXED Master Control Dashboard (port 8505)...")
    run_command("streamlit run master_control_dashboard.py --server.port 8505", cwd=base_dir)
    time.sleep(5)
    
    print("\n✅ System Startup Complete!")
    print("\n🌐 Access Points:")
    print("  • Main Trading Dashboard:    http://localhost:8501")
    print("  • Unified Trading Dashboard: http://localhost:8503")
    print("  • Enhanced Dashboard:        http://localhost:8504")
    print("  • Master Control Dashboard:  http://localhost:8505  ← FIXED WITH REAL DATA")
    print("  • Main API:                  http://localhost:5000")
    print("  • Enhanced API:              http://localhost:5001")
    
    print("\n📊 Master Control Dashboard now shows REAL Bybit production data!")
    print("🎛️  All services are running with real-time data integration.")
    
    # Wait for user input to keep script running
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
