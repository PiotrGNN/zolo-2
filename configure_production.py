#!/usr/bin/env python3
"""
configure_production.py
-----------------------
Script to configure ZoL0 system for production environment.

This script helps set up the necessary environment variables and 
configurations for production trading.
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Any

def print_banner():
    """Print configuration banner"""
    print("=" * 60)
    print("🚀 ZoL0 Production Configuration Setup")
    print("=" * 60)
    print()

def check_current_environment():
    """Check current environment configuration"""
    print("📊 Current Environment Status:")
    print("-" * 40)
    
    # Check environment variables
    env_vars = {
        "BYBIT_PRODUCTION_CONFIRMED": os.getenv("BYBIT_PRODUCTION_CONFIRMED", "Not set"),
        "BYBIT_PRODUCTION_ENABLED": os.getenv("BYBIT_PRODUCTION_ENABLED", "Not set"),
        "BYBIT_TESTNET": os.getenv("BYBIT_TESTNET", "Not set"),
        "BYBIT_API_KEY": "***HIDDEN***" if os.getenv("BYBIT_API_KEY") else "Not set",
        "BYBIT_SECRET": "***HIDDEN***" if os.getenv("BYBIT_SECRET") else "Not set",
        "BYBIT_PRODUCTION_API_KEY": "***HIDDEN***" if os.getenv("BYBIT_PRODUCTION_API_KEY") else "Not set",
        "BYBIT_PRODUCTION_SECRET": "***HIDDEN***" if os.getenv("BYBIT_PRODUCTION_SECRET") else "Not set"
    }
    
    for key, value in env_vars.items():
        status = "✅" if value != "Not set" else "❌"
        print(f"{status} {key}: {value}")
    
    print()
    return env_vars

def configure_testnet():
    """Configure for testnet trading"""
    print("🔧 Configuring for Testnet Environment...")
    print("-" * 40)
    
    # Set testnet environment variables
    os.environ["BYBIT_TESTNET"] = "true"
    os.environ["BYBIT_PRODUCTION_CONFIRMED"] = "false" 
    os.environ["BYBIT_PRODUCTION_ENABLED"] = "false"
    
    print("✅ Testnet configuration set:")
    print("   - BYBIT_TESTNET = true")
    print("   - BYBIT_PRODUCTION_CONFIRMED = false")
    print("   - BYBIT_PRODUCTION_ENABLED = false")
    print()

def configure_production_preparation():
    """Prepare for production (confirmation step)"""
    print("⚠️  Production Preparation Mode")
    print("-" * 40)
    print("This will prepare the system for production but NOT enable it yet.")
    print()
    
    confirm = input("Are you sure you want to prepare for production? (yes/no): ").lower()
    if confirm != "yes":
        print("❌ Production preparation cancelled.")
        return False
    
    # Set preparation variables
    os.environ["BYBIT_PRODUCTION_CONFIRMED"] = "true"
    os.environ["BYBIT_PRODUCTION_ENABLED"] = "false"  # Still disabled
    
    print("✅ Production preparation set:")
    print("   - BYBIT_PRODUCTION_CONFIRMED = true")
    print("   - BYBIT_PRODUCTION_ENABLED = false (still disabled)")
    print()
    print("⚠️  IMPORTANT: You still need to:")
    print("   1. Set BYBIT_PRODUCTION_API_KEY")
    print("   2. Set BYBIT_PRODUCTION_SECRET") 
    print("   3. Set BYBIT_PRODUCTION_ENABLED = true")
    print()
    return True

def configure_production_full():
    """Full production configuration (DANGEROUS)"""
    print("🚨 DANGER: Full Production Configuration")
    print("-" * 40)
    print("⚠️  WARNING: This will enable REAL trading with REAL money!")
    print("⚠️  Make sure you have:")
    print("   - Valid production API credentials")
    print("   - Sufficient account balance") 
    print("   - Tested strategies thoroughly")
    print("   - Risk management configured")
    print()
    
    confirm1 = input("I understand this will trade with REAL money (yes/no): ").lower()
    if confirm1 != "yes":
        print("❌ Production configuration cancelled.")
        return False
        
    confirm2 = input("I have tested the system thoroughly (yes/no): ").lower()
    if confirm2 != "yes":
        print("❌ Production configuration cancelled.")
        return False
        
    confirm3 = input("Type 'ENABLE PRODUCTION' to proceed: ")
    if confirm3 != "ENABLE PRODUCTION":
        print("❌ Production configuration cancelled.")
        return False
    
    # Set production variables
    os.environ["BYBIT_PRODUCTION_CONFIRMED"] = "true"
    os.environ["BYBIT_PRODUCTION_ENABLED"] = "true"
    
    if "BYBIT_TESTNET" in os.environ:
        del os.environ["BYBIT_TESTNET"]
    
    print("🚨 Production configuration enabled:")
    print("   - BYBIT_PRODUCTION_CONFIRMED = true")
    print("   - BYBIT_PRODUCTION_ENABLED = true")
    print("   - BYBIT_TESTNET = removed")
    print()
    print("⚠️  SYSTEM IS NOW IN PRODUCTION MODE!")
    return True

def save_configuration():
    """Save current configuration to file"""
    config = {
        "timestamp": datetime.now().isoformat(),
        "environment_variables": {
            key: os.getenv(key, "Not set")
            for key in [
                "BYBIT_PRODUCTION_CONFIRMED",
                "BYBIT_PRODUCTION_ENABLED", 
                "BYBIT_TESTNET"
            ]
        },
        "api_keys_configured": {
            "testnet": bool(os.getenv("BYBIT_API_KEY")),
            "production": bool(os.getenv("BYBIT_PRODUCTION_API_KEY"))
        }
    }
    
    with open("logs/environment_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"📁 Configuration saved to logs/environment_config.json")

def main():
    """Main configuration menu"""
    print_banner()
    
    while True:
        check_current_environment()
        
        print("🔧 Configuration Options:")
        print("-" * 40)
        print("1. Configure for Testnet (Safe)")
        print("2. Prepare for Production (Confirmation only)")
        print("3. Enable Full Production (DANGEROUS)")
        print("4. Check Environment Status")
        print("5. Save Current Configuration")
        print("6. Exit")
        print()
        
        choice = input("Select option (1-6): ").strip()
        
        if choice == "1":
            configure_testnet()
        elif choice == "2":
            configure_production_preparation()
        elif choice == "3":
            configure_production_full()
        elif choice == "4":
            continue  # Will show status at top of loop
        elif choice == "5":
            save_configuration()
        elif choice == "6":
            print("👋 Configuration complete!")
            break
        else:
            print("❌ Invalid option. Please select 1-6.")
        
        print()
        input("Press Enter to continue...")
        print("\n" * 2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Configuration cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
