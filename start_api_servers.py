#!/usr/bin/env python3
"""
Start API Servers for ZoL0 Trading System
This script starts both API servers needed for real data access
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def start_api_server(script_path, port, name):
    """Start an API server in a new process"""
    try:
        print(f"🚀 Starting {name} on port {port}...")
        
        # Create new process for the API server
        process = subprocess.Popen(
            [sys.executable, script_path],
            cwd=Path(script_path).parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"✅ {name} started with PID: {process.pid}")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return None

def main():
    print("🔧 ZoL0 API Server Startup Script")
    print("=" * 50)
    
    # Define paths
    base_dir = Path("C:/Users/piotr/Desktop/Zol0")
    main_api_path = base_dir / "ZoL0-master" / "dashboard_api.py"
    enhanced_api_path = base_dir / "enhanced_dashboard_api.py"
    
    # Check if files exist
    if not main_api_path.exists():
        print(f"❌ Main API file not found: {main_api_path}")
        return
        
    if not enhanced_api_path.exists():
        print(f"❌ Enhanced API file not found: {enhanced_api_path}")
        return
    
    # Start API servers
    main_process = start_api_server(str(main_api_path), 5000, "Main API Server")
    time.sleep(2)
    
    enhanced_process = start_api_server(str(enhanced_api_path), 5001, "Enhanced API Server")
    time.sleep(2)
    
    print("\n🎯 API Server Status:")
    print(f"  • Main API (port 5000): {'✅ Running' if main_process and main_process.poll() is None else '❌ Failed'}")
    print(f"  • Enhanced API (port 5001): {'✅ Running' if enhanced_process and enhanced_process.poll() is None else '❌ Failed'}")
    
    print("\n🌐 API Endpoints:")
    print("  • Main API:     http://localhost:5000")
    print("  • Enhanced API: http://localhost:5001")
    
    print("\n📊 Dashboard URLs:")
    print("  • Master Control: http://localhost:8501 (or use launch_all_dashboards.py)")
    print("  • All Dashboards: Run 'python launch_all_dashboards.py' to start all")
    
    print("\n💡 To stop servers, close this window or use Ctrl+C")
    
    # Keep script running to monitor servers
    try:
        while True:
            time.sleep(10)
            
            # Check if processes are still running
            if main_process and main_process.poll() is not None:
                print("⚠️  Main API server stopped unexpectedly")
                break
                
            if enhanced_process and enhanced_process.poll() is not None:
                print("⚠️  Enhanced API server stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping API servers...")
        
        if main_process and main_process.poll() is None:
            main_process.terminate()
            print("✅ Main API server stopped")
            
        if enhanced_process and enhanced_process.poll() is None:
            enhanced_process.terminate()
            print("✅ Enhanced API server stopped")

if __name__ == "__main__":
    main()
