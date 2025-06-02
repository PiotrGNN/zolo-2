#!/usr/bin/env python3
"""
Test Bybit Authentication and API Connection
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the ZoL0-master directory to the path
zol0_path = os.path.join(os.path.dirname(__file__), 'ZoL0-master')
if zol0_path not in sys.path:
    sys.path.insert(0, zol0_path)

try:
    from data.execution.bybit_connector import BybitConnector
    
    print("🔑 TESTING BYBIT AUTHENTICATION")
    print("=" * 50)
    
    # Check environment variables
    api_key = os.getenv('BYBIT_API_KEY')
    api_secret = os.getenv('BYBIT_API_SECRET')
    testnet = os.getenv('BYBIT_TESTNET', 'false').lower() == 'true'
    
    print(f"API Key: {api_key[:10]}..." if api_key else "API Key: MISSING")
    print(f"API Secret: {'*' * 20}" if api_secret else "API Secret: MISSING")
    print(f"Testnet: {testnet}")
    print(f"Trading Mode: {os.getenv('TRADING_MODE', 'development')}")
    
    if not api_key or not api_secret:
        print("❌ BŁĄD: Brak kluczy API!")
        sys.exit(1)
    
    print("\n🔌 Initializing BybitConnector...")
    connector = BybitConnector()
    
    print("\n⏰ Testing server time...")
    try:
        server_time = connector.get_server_time()
        print(f"✅ Server time: {server_time}")
    except Exception as e:
        print(f"❌ Server time error: {e}")
    
    print("\n💰 Testing account balance...")
    try:
        balance = connector.get_account_balance()
        print(f"✅ Balance response: {balance}")
    except Exception as e:
        print(f"❌ Balance error: {e}")
    
    print("\n📊 Testing market data...")
    try:
        market_data = connector.get_market_data('BTCUSDT')
        print(f"✅ Market data: {market_data}")
    except Exception as e:
        print(f"❌ Market data error: {e}")
        
except Exception as e:
    print(f"❌ CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
