#!/usr/bin/env python3
"""
Quick logger error test for dashboard files
"""

import sys
import importlib.util
from pathlib import Path

def test_import(file_path):
    """Test if a Python file can be imported without errors"""
    try:
        # Try to compile the file first
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        compile(content, file_path, 'exec')
        print(f"✅ {file_path.name}: Syntax OK")
        return True
    except Exception as e:
        print(f"❌ {file_path.name}: {e}")
        return False

def main():
    """Test key dashboard files"""
    base_path = Path("c:/Users/piotr/Desktop/Zol0")
    
    files_to_test = [
        "advanced_trading_analytics.py",
        "ml_predictive_analytics.py",
        "real_time_market_data_integration.py",
        "enhanced_bot_monitor.py"
    ]
    
    print("🔍 Testing dashboard files for syntax errors...")
    print("-" * 50)
    
    all_good = True
    for file_name in files_to_test:
        file_path = base_path / file_name
        if file_path.exists():
            result = test_import(file_path)
            if not result:
                all_good = False
        else:
            print(f"❌ {file_name}: File not found")
            all_good = False
    
    print("-" * 50)
    if all_good:
        print("🎉 All dashboard files passed syntax check!")
    else:
        print("⚠️  Some files have issues that need fixing")

if __name__ == "__main__":
    main()
