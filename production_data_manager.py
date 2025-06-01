#!/usr/bin/env python3
"""
production_data_manager.py
--------------------------
Centralized manager for production Bybit API data across all dashboards.

This module provides a unified interface for all dashboards to access real
Bybit production data, with fallback mechanisms and error handling.
"""

import os
import json
import logging
import asyncio
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
import pandas as pd
import requests
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    logger.warning("python-dotenv not available, using system environment variables")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductionDataManager:
    """Centralized manager for production API data"""
    def __init__(self):
        self.config_file = Path("production_api_config.json")
        self.config = self._load_config()
        
        # Load environment variables from .env file
        try:
            env_path = Path(__file__).parent / "ZoL0-master" / ".env"
            if env_path.exists():
                from dotenv import load_dotenv
                load_dotenv(env_path)
        except ImportError:
            pass
        
        # Connection state - use specific values from .env
        self.is_production = os.getenv("BYBIT_PRODUCTION_ENABLED", "true").lower() == "true"
        self.api_key = os.getenv("BYBIT_API_KEY", "lAXnmPeMMVecqcW8oT")
        self.api_secret = os.getenv("BYBIT_API_SECRET", "RAQcrNjFSVBGWeRBjQGL8fTRzbtbKHmAArGz")
        
        # Data cache
        self.data_cache = {}
        self.cache_timestamps = {}
        self.cache_ttl = 30  # seconds
        
        # Connection status
        self.connection_status = {
            "bybit": {"connected": False, "last_check": None, "error": None},
            "last_update": datetime.now()
        }
        
        # Rate limiting
        self.request_count = 0
        self.last_reset = time.time()
        self.rate_limit = self.config.get("dashboard_configuration", {}).get("rate_limits", {}).get("requests_per_minute", 600)
        
        # Initialize connector
        self.bybit_connector = None
        self._initialize_connector()
        
        # Start background health monitoring
        self._start_health_monitor()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            
        # Default configuration
        return {
            "api_configuration": {
                "bybit": {
                    "production": {
                        "base_url": "https://api.bybit.com",
                        "ws_url": "wss://stream.bybit.com/v5/public"
                    },
                    "testnet": {
                        "base_url": "https://api-testnet.bybit.com",
                        "ws_url": "wss://stream-testnet.bybit.com/v5/public"
                    }
                }
            },
            "symbols": {
                "crypto": ["BTCUSDT", "ETHUSDT", "ADAUSDT", "DOTUSDT", "SOLUSDT"]
            }        }
        
    def _initialize_connector(self):
        """Initialize Bybit connector"""
        try:
            # Import the existing connector
            import sys
            sys.path.append(str(Path(__file__).parent / "ZoL0-master"))
            from data.execution.bybit_connector import BybitConnector
            
            self.bybit_connector = BybitConnector(
                api_key=self.api_key,
                api_secret=self.api_secret,
                use_testnet=not self.is_production            )
            
            # Test connection
            if self._test_connection():
                self.connection_status["bybit"]["connected"] = True
                logger.info(f"Connected to Bybit {'Production' if self.is_production else 'Testnet'} API")
            else:
                logger.error("Failed to connect to Bybit API")
                
        except Exception as e:
            logger.error(f"Failed to initialize Bybit connector: {e}")
            
    def _test_connection(self) -> bool:
        """Test API connection"""
        try:
            if self.bybit_connector:
                result = self.bybit_connector.get_server_time()
                # Bybit API returns retCode: 0 for success
                return result.get("retCode") == 0
        except Exception as e:
            self.connection_status["bybit"]["error"] = str(e)
            logger.error(f"Connection test failed: {e}")
            
        return False
        
    def _start_health_monitor(self):
        """Start background health monitoring"""
        def health_check():
            while True:
                try:
                    self.connection_status["bybit"]["connected"] = self._test_connection()
                    self.connection_status["bybit"]["last_check"] = datetime.now()
                    self.connection_status["last_update"] = datetime.now()
                    
                    # Clean old cache entries
                    self._cleanup_cache()
                    
                    # Reset rate limiting counter
                    if time.time() - self.last_reset > 60:
                        self.request_count = 0
                        self.last_reset = time.time()
                        
                except Exception as e:
                    logger.error(f"Health check failed: {e}")
                    
                time.sleep(30)  # Check every 30 seconds
                
        health_thread = threading.Thread(target=health_check, daemon=True)
        health_thread.start()
    
    def _cleanup_cache(self):
        """Remove expired cache entries"""
        current_time = time.time()
        expired_keys = [
            key for key, timestamp in self.cache_timestamps.items()
            if current_time - timestamp > self.cache_ttl
        ]
        for key in expired_keys:
            self.data_cache.pop(key, None)
            self.cache_timestamps.pop(key, None)
            
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cache entry is still valid"""
        if cache_key not in self.cache_timestamps:
            return False
            
        return time.time() - self.cache_timestamps[cache_key] < self.cache_ttl
    
    def _is_portfolio_cache_valid(self, cache_key: str, extended_ttl: int = 120) -> bool:
        """Check if portfolio cache entry is still valid with extended TTL"""
        if cache_key not in self.cache_timestamps:
            return False
            
        # Use extended TTL for portfolio data to reduce API calls
        return time.time() - self.cache_timestamps[cache_key] < extended_ttl
    
    def _get_portfolio_cache_key(self, method_name: str) -> str:
        """Generate cache key for portfolio methods"""
        return f"portfolio_{method_name}_{self.is_production}"
    
    def _cache_data(self, cache_key: str, data: Any):
        """Cache data with timestamp"""
        self.data_cache[cache_key] = data
        self.cache_timestamps[cache_key] = time.time()
        
    def _check_rate_limit(self) -> bool:
        """Check if request is within rate limits"""
        if self.request_count >= self.rate_limit:
            logger.warning("Rate limit exceeded, request denied")
            return False
        
        self.request_count += 1
        return True
    
    def get_account_balance(self, use_cache: bool = True) -> Dict[str, Any]:
        """Get account balance from production API"""
        # Use enhanced portfolio cache for balance data
        balance_cache_key = self._get_portfolio_cache_key("account_balance")
        
        # Check enhanced cache first (60 second cache for balance)
        if use_cache and self._is_portfolio_cache_valid(balance_cache_key, 60):
            logger.info("Using cached account balance")
            return self.data_cache[balance_cache_key]
            
        # Check rate limit
        if not self._check_rate_limit():
            logger.warning("Rate limit exceeded for account balance")
            return {"error": "Rate limit exceeded", "success": False}
        
        try:
            if self.bybit_connector:                # Set timeout for this specific call
                import signal
                import threading
                
                result_container = {"result": None, "error": None}
                
                def get_balance():
                    try:
                        result_container["result"] = self.bybit_connector.get_account_balance()
                    except Exception as e:
                        result_container["error"] = str(e)
                  # Run with timeout
                thread = threading.Thread(target=get_balance)
                thread.daemon = True
                thread.start()
                thread.join(timeout=10)  # 10 second timeout for balance (reduced for faster API response)
                
                if thread.is_alive():
                    logger.warning("Account balance call timed out after 10 seconds, using cache/fallback")
                    return self._get_fallback_balance()
                
                if result_container["error"]:
                    logger.error(f"Account balance error: {result_container['error']}")
                    return self._get_fallback_balance()
                
                result = result_container["result"]
                if result and result.get("retCode") == 0:
                    # Transform Bybit API response to dashboard-compatible format
                    transformed_result = self._transform_bybit_balance_response(result)
                    transformed_result["data_source"] = "production_api" if self.is_production else "testnet_api"
                    transformed_result["timestamp"] = datetime.now().isoformat()
                    
                    # Cache with enhanced TTL
                    self._cache_data(balance_cache_key, transformed_result)
                    logger.info("Successfully retrieved and cached account balance")
                    
                    return transformed_result
                else:
                    logger.error(f"Account balance API call failed: {result}")
                    
        except Exception as e:
            logger.error(f"Failed to get account balance: {e}")
            
        # Return fallback data
        logger.warning("Using fallback account balance data")
        return self._get_fallback_balance()
        
    def get_portfolio_balance(self, use_cache: bool = True) -> Dict[str, Any]:
        """Get portfolio balance - alias for get_account_balance for compatibility"""
        return self.get_account_balance(use_cache)
    
    def get_market_data(self, symbol: str = "BTCUSDT", use_cache: bool = True) -> Dict[str, Any]:
        """Get market data for a symbol"""
        cache_key = f"market_data_{symbol}"
        
        # Check cache first
        if use_cache and self._is_cache_valid(cache_key):
            return self.data_cache[cache_key]
              # Check rate limit
        if not self._check_rate_limit():
            return {"error": "Rate limit exceeded", "success": False}
            
        try:
            if self.bybit_connector:
                result = self.bybit_connector.get_ticker(symbol)
                
                # Bybit API returns retCode: 0 for success
                if result.get("retCode") == 0:
                    result["data_source"] = "production_api" if self.is_production else "testnet_api"
                    result["timestamp"] = datetime.now().isoformat()
                    
                    # Cache the result
                    self._cache_data(cache_key, result)
                    
                    return result
                else:
                    logger.error(f"Market data API call failed for {symbol}: {result}")
                    
        except Exception as e:
            logger.error(f"Failed to get market data for {symbol}: {e}")
            
        # Return fallback data
        return self._get_fallback_market_data(symbol)
        
    def get_historical_data(self, symbol: str = "BTCUSDT", interval: str = "1h", 
                          limit: int = 100, use_cache: bool = True) -> pd.DataFrame:
        """Get historical OHLCV data"""
        cache_key = f"historical_{symbol}_{interval}_{limit}"
        
        # Check cache first
        if use_cache and self._is_cache_valid(cache_key):
            return self.data_cache[cache_key]
            
        # Check rate limit
        if not self._check_rate_limit():
            logger.warning("Rate limit exceeded for historical data")
            return pd.DataFrame()
            
        try:
            # Use market data fetcher
            import sys
            sys.path.append(str(Path(__file__).parent / "ZoL0-master"))
            from data.data.market_data_fetcher import MarketDataFetcher
            
            fetcher = MarketDataFetcher(
                api_key=self.api_key,
                api_secret=self.api_secret,
                use_testnet=not self.is_production
            )
            
            df = fetcher.fetch_data(symbol=symbol, interval=interval, limit=limit)
            
            if df is not None and not df.empty:
                # Add metadata
                df.attrs["data_source"] = "production_api" if self.is_production else "testnet_api"
                df.attrs["timestamp"] = datetime.now().isoformat()
                df.attrs["symbol"] = symbol
                
                # Cache the result
                self._cache_data(cache_key, df)
                
                return df
                
        except Exception as e:
            logger.error(f"Failed to get historical data for {symbol}: {e}")
              # Return fallback data
        return self._get_fallback_historical_data(symbol, interval, limit)
        
    def get_positions(self, use_cache: bool = True) -> Dict[str, Any]:
        """Get current positions"""
        cache_key = "positions"
        
        # Check cache first
        if use_cache and self._is_cache_valid(cache_key):
            return self.data_cache[cache_key]
            
        # Check rate limit
        if not self._check_rate_limit():
            return {"error": "Rate limit exceeded", "success": False}
        
        try:
            if self.bybit_connector:
                result = self.bybit_connector.get_positions()
                
                # Bybit API returns retCode: 0 for success
                if result.get("retCode") == 0:
                    result["data_source"] = "production_api" if self.is_production else "testnet_api"
                    result["timestamp"] = datetime.now().isoformat()
                    
                    # Cache the result
                    self._cache_data(cache_key, result)
                    
                    return result
                    
        except Exception as e:
            logger.error(f"Failed to get positions: {e}")
            
        # Return fallback data
        return self._get_fallback_positions()
        
    def get_trading_stats(self, use_cache: bool = True) -> Dict[str, Any]:
        """Get comprehensive trading statistics"""
        try:
            balance = self.get_account_balance(use_cache)
            positions = self.get_positions(use_cache)
            market_data = self.get_market_data("BTCUSDT", use_cache)
            
            stats = {
                "account": balance,
                "positions": positions,
                "market": market_data,
                "environment": "production" if self.is_production else "testnet",
                "api_status": self.connection_status,
                "timestamp": datetime.now().isoformat(),
                "data_source": "live_api"
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get trading stats: {e}")
            return self._get_fallback_trading_stats()
            
    def get_multiple_symbols_data(self, symbols: List[str], use_cache: bool = True) -> Dict[str, Any]:
        """Get market data for multiple symbols"""
        results = {}
        
        for symbol in symbols:
            try:
                results[symbol] = self.get_market_data(symbol, use_cache)
            except Exception as e:
                logger.error(f"Failed to get data for {symbol}: {e}")
                results[symbol] = {"error": str(e), "success": False}
                
        return {
            "symbols": results,
            "timestamp": datetime.now().isoformat(),
            "environment": "production" if self.is_production else "testnet"        }
        
    def get_enhanced_portfolio_details(self, use_cache: bool = True) -> Dict[str, Any]:
        """Get enhanced portfolio details with comprehensive information"""
        try:
            import concurrent.futures
            import threading            # Set adequate timeout for each API call (reduced for faster fallback to cache)
            api_timeout = 10  # seconds per API call (reduced from 25 for faster API response)
            
            def get_data_with_timeout(func, *args, **kwargs):
                """Get data with timeout"""
                result = {"data": None, "error": None}
                
                def run():
                    try:
                        result["data"] = func(*args, **kwargs)
                    except Exception as e:
                        result["error"] = str(e)
                
                thread = threading.Thread(target=run)
                thread.daemon = True
                thread.start()
                thread.join(timeout=api_timeout)
                
                if thread.is_alive():
                    logger.warning(f"API call {func.__name__} timed out after {api_timeout}s")
                    return None
                
                if result["error"]:
                    logger.warning(f"API call {func.__name__} failed: {result['error']}")
                    return None
                    
                return result["data"]
              # Get basic account balance with timeout
            balance_data = get_data_with_timeout(self.get_account_balance, use_cache)
            if balance_data is None:
                # Try to get cached balance data directly before falling back to demo
                balance_cache_key = self._get_portfolio_cache_key("account_balance")
                if balance_cache_key in self.data_cache:
                    logger.info("API timed out, using cached balance data")
                    balance_data = self.data_cache[balance_cache_key]
                else:
                    logger.warning("Balance data timed out and no cache available, using fallback")
                    return self._get_fallback_enhanced_portfolio()
            
            # Track if we're using real data (even if cached)
            using_real_data = balance_data is not None and balance_data.get("success")
            
            # Get positions data with timeout (optional, can fail)
            positions_data = get_data_with_timeout(self.get_positions, use_cache)
            if positions_data is None:
                logger.warning("Positions data timed out, using empty positions")
                positions_data = {"success": False, "result": {"list": []}}
            
            # Get market data with timeout (optional, can fail)
            btc_data = get_data_with_timeout(self.get_market_data, "BTCUSDT", use_cache)
            eth_data = get_data_with_timeout(self.get_market_data, "ETHUSDT", use_cache)
            
            # Use fallback prices if market data failed
            if btc_data is None:
                btc_data = {"last_price": "45000.0"}
                logger.warning("BTC market data timed out, using fallback price")
            if eth_data is None:
                eth_data = {"last_price": "2800.0"}
                logger.warning("ETH market data timed out, using fallback price")
            
            # Calculate portfolio metrics
            total_equity = 0
            total_available = 0
            total_wallet = 0
            coin_details = {}
            
            if balance_data.get("success") and balance_data.get("balances"):
                for coin, balance_info in balance_data["balances"].items():
                    equity = float(balance_info.get("equity", 0))
                    available = float(balance_info.get("available_balance", 0))
                    wallet = float(balance_info.get("wallet_balance", 0))
                    
                    total_equity += equity
                    total_available += available
                    total_wallet += wallet
                    
                    # Enhanced coin details
                    coin_details[coin] = {
                        "symbol": coin,
                        "equity": equity,
                        "available_balance": available,
                        "wallet_balance": wallet,
                        "locked_balance": wallet - available,
                        "percentage_of_portfolio": 0  # Will calculate below
                    }
            
            # Calculate percentages
            for coin in coin_details:
                if total_equity > 0:
                    coin_details[coin]["percentage_of_portfolio"] = (coin_details[coin]["equity"] / total_equity) * 100
            
            # Get current positions summary
            active_positions = 0
            total_unrealized_pnl = 0
            
            if positions_data.get("success") and positions_data.get("result"):
                positions_list = positions_data["result"].get("list", [])
                active_positions = len(positions_list)
                
                for pos in positions_list:
                    pnl = float(pos.get("unrealisedPnl", 0))
                    total_unrealized_pnl += pnl
              # Build enhanced portfolio response with correct data source indicators
            enhanced_details = {
                "success": True,
                "data_source": "production_api" if (using_real_data and self.is_production) else "fallback",
                "timestamp": datetime.now().isoformat(),
                "environment": "production" if (using_real_data and self.is_production) else "demo",
                
                # Summary metrics
                "portfolio_summary": {
                    "total_equity": round(total_equity, 4),
                    "total_available": round(total_available, 4),
                    "total_wallet_balance": round(total_wallet, 4),
                    "locked_balance": round(total_wallet - total_available, 4),
                    "unrealized_pnl": round(total_unrealized_pnl, 4),
                    "active_positions": active_positions,
                    "total_coins": len(coin_details)
                },
                
                # Detailed coin breakdown
                "coin_details": coin_details,
                
                # Position information
                "positions_summary": {
                    "active_count": active_positions,
                    "total_unrealized_pnl": round(total_unrealized_pnl, 4),
                    "positions": positions_data.get("result", {}).get("list", [])[:5]  # First 5 positions
                },
                
                # Market context
                "market_context": {
                    "btc_price": self._extract_price(btc_data),
                    "eth_price": self._extract_price(eth_data),
                    "last_updated": datetime.now().isoformat()
                },
                
                # API status
                "connection_status": self.connection_status,
                
                # Raw data for compatibility
                "balances": balance_data.get("balances", {}),                "raw_balance_data": balance_data,
                "raw_positions_data": positions_data
            }
            
            return enhanced_details
            
        except Exception as e:
            logger.error(f"Failed to get enhanced portfolio details: {e}")
            return self._get_fallback_enhanced_portfolio()
    
    def _extract_price(self, market_data: Dict[str, Any]) -> float:
        """Extract price from market data response"""
        try:
            if market_data.get("success"):
                data = market_data.get("data", {})
                if "list" in data and data["list"]:
                    return float(data["list"][0].get("lastPrice", 0))
                elif "lastPrice" in data:
                    return float(data.get("lastPrice", 0))
        except (ValueError, TypeError, KeyError):
            pass
        return 0.0
    
    def _transform_bybit_balance_response(self, bybit_response: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Bybit API response to dashboard-compatible format"""
        try:
            # Extract data from Bybit V5 API response
            balances = {}
            result_data = bybit_response.get("result", {})
            
            if "list" in result_data:
                for account in result_data["list"]:
                    if "coin" in account and isinstance(account["coin"], list):
                        for coin_data in account["coin"]:
                            symbol = coin_data.get("coin")
                            if symbol:
                                balances[symbol] = {
                                    "equity": float(coin_data.get("equity", 0) or 0),
                                    "available_balance": float(coin_data.get("availableToWithdraw", 0) or coin_data.get("walletBalance", 0) or 0),
                                    "wallet_balance": float(coin_data.get("walletBalance", 0) or 0)
                                }
            
            # Return in dashboard-expected format
            return {
                "success": True,
                "retCode": bybit_response.get("retCode", 0),
                "retMsg": bybit_response.get("retMsg", "OK"),
                "balances": balances,
                "raw_bybit_response": bybit_response  # Keep original for debugging
            }
            
        except Exception as e:
            logger.error(f"Failed to transform Bybit balance response: {e}")
            return {
                "success": False,                "error": f"Transformation failed: {e}",
                "raw_bybit_response": bybit_response
            }
    
    def _get_fallback_enhanced_portfolio(self) -> Dict[str, Any]:
        """Fallback enhanced portfolio data - TRUE demo data only when no real data available"""
        return {
            "success": True,
            "data_source": "fallback",
            "timestamp": datetime.now().isoformat(),
            "environment": "demo",
            
            "portfolio_summary": {
                "total_equity": 10000.0,  # True demo values
                "total_available": 8500.0,
                "total_wallet_balance": 10000.0,
                "locked_balance": 1500.0,
                "unrealized_pnl": 0.0,
                "active_positions": 0,
                "total_coins": 1
            },
            
            "coin_details": {
                "USDT": {
                    "symbol": "USDT",
                    "equity": 10000.0,  # True demo values
                    "available_balance": 8500.0,
                    "wallet_balance": 10000.0,
                    "locked_balance": 1500.0,
                    "percentage_of_portfolio": 100.0
                }
            },
            
            "positions_summary": {
                "active_count": 0,
                "total_unrealized_pnl": 0.0,
                "positions": []
            },
            
            "market_context": {
                "btc_price": 45000.0,
                "eth_price": 2800.0,
                "last_updated": datetime.now().isoformat()
            },
              "connection_status": {"status": "fallback", "message": "Using demo data - no real API data available"},
            "balances": {"USDT": {"equity": 10000.0, "available_balance": 8500.0, "wallet_balance": 10000.0}}
        }

    # ...existing code...
        
    def _get_fallback_balance(self) -> Dict[str, Any]:
        """Fallback account balance data"""
        return {
            "success": True,
            "data_source": "fallback",
            "balances": {
                "USDT": {"equity": 10000.0, "available_balance": 8500.0, "wallet_balance": 10000.0}
            },
            "timestamp": datetime.now().isoformat()
        }
        
    def _get_fallback_market_data(self, symbol: str) -> Dict[str, Any]:
        """Fallback market data"""
        base_prices = {
            "BTCUSDT": 45000,
            "ETHUSDT": 2800,
            "ADAUSDT": 0.45,
            "DOTUSDT": 6.5,
            "SOLUSDT": 95
        }
        
        base_price = base_prices.get(symbol, 1000)
        
        return {
            "success": True,
            "data_source": "fallback",
            "data": {
                "list": [{
                    "symbol": symbol,
                    "lastPrice": str(base_price),
                    "bid1Price": str(base_price * 0.999),
                    "ask1Price": str(base_price * 1.001),
                    "volume24h": "1000000"
                }]
            },
            "timestamp": datetime.now().isoformat()
        }
        
    def _get_fallback_historical_data(self, symbol: str, interval: str, limit: int) -> pd.DataFrame:
        """Fallback historical data"""
        import numpy as np
        
        # Generate synthetic OHLCV data
        dates = pd.date_range(end=datetime.now(), periods=limit, freq='1H')
        base_price = 45000 if 'BTC' in symbol else 2800
        
        # Generate realistic price movements
        returns = np.random.normal(0, 0.02, limit)
        prices = base_price * np.exp(np.cumsum(returns))
        
        df = pd.DataFrame({
            'timestamp': [int(date.timestamp()) for date in dates],
            'open': prices,
            'high': prices * (1 + np.random.uniform(0, 0.03, limit)),
            'low': prices * (1 - np.random.uniform(0, 0.03, limit)),
            'close': prices,
            'volume': np.random.uniform(100, 1000, limit)
        })
        
        # Ensure high >= open,close and low <= open,close
        df['high'] = np.maximum(df['high'], np.maximum(df['open'], df['close']))
        df['low'] = np.minimum(df['low'], np.minimum(df['open'], df['close']))
        
        df.attrs = {
            "data_source": "fallback",
            "timestamp": datetime.now().isoformat(),
            "symbol": symbol
        }
        
        return df
        
    def _get_fallback_positions(self) -> Dict[str, Any]:
        """Fallback positions data"""
        return {
            "success": True,
            "data_source": "fallback",
            "result": {
                "list": []  # No positions
            },
            "timestamp": datetime.now().isoformat()
        }
        
    def _get_fallback_trading_stats(self) -> Dict[str, Any]:
        """Fallback trading statistics"""
        return {
            "account": self._get_fallback_balance(),
            "positions": self._get_fallback_positions(),
            "market": self._get_fallback_market_data("BTCUSDT"),
            "environment": "fallback",
            "api_status": {"error": "API unavailable"},
            "timestamp": datetime.now().isoformat(),
            "data_source": "fallback"
        }
        
    def get_status(self) -> Dict[str, Any]:
        """Get manager status"""
        return {
            "environment": "production" if self.is_production else "testnet",
            "connection_status": self.connection_status,
            "cache_size": len(self.data_cache),
            "rate_limit": {
                "requests_this_minute": self.request_count,
                "limit": self.rate_limit        },
            "timestamp": datetime.now().isoformat()
        }
    
    def get_portfolio_data(self, use_cache: bool = True) -> Dict[str, Any]:
        """Get portfolio data in dashboard-compatible format (for /api/portfolio endpoint)"""
        # Check enhanced portfolio cache first with extended TTL
        portfolio_cache_key = self._get_portfolio_cache_key("portfolio_data")
        
        if use_cache and self._is_portfolio_cache_valid(portfolio_cache_key, 300):  # 5 minute cache for API calls
            logger.info("Using cached portfolio data (extended TTL)")
            return self.data_cache[portfolio_cache_key]
        
        try:
            # Use enhanced details for richer dashboard data with aggressive caching
            details = self.get_enhanced_portfolio_details(use_cache=True)  # Always use cache for API calls
            
            # Flatten for legacy compatibility
            portfolio_data = {
                "success": details.get("success", False),
                "timestamp": details.get("timestamp"),
                "total_value": details.get("portfolio_summary", {}).get("total_equity"),
                "available_balance": details.get("portfolio_summary", {}).get("total_available"),
                "balances": details.get("balances", {}),
                "positions": details.get("positions_summary", {}).get("positions", []),
                "performance": {
                    "daily_pnl": details.get("portfolio_summary", {}).get("unrealized_pnl", 0),
                    "total_pnl": details.get("portfolio_summary", {}).get("unrealized_pnl", 0),
                    "win_rate": 0.68,  # Placeholder, real value if available
                    "sharpe_ratio": 1.45  # Placeholder, real value if available
                },
                "data_source": details.get("data_source"),
                "environment": details.get("environment"),
                "connection_status": details.get("connection_status"),
            }
            
            # Cache the result with extended TTL
            self._cache_data(portfolio_cache_key, portfolio_data)
            
            return portfolio_data
        except Exception as e:
            logger.error(f"get_portfolio_data error: {e}")
            return self._get_fallback_enhanced_portfolio()

    def get_trading_status(self, use_cache: bool = True) -> Dict[str, Any]:
        """Get trading status for dashboard/API"""
        try:
            stats = self.get_trading_stats(use_cache)
            return {
                "success": True,
                "timestamp": stats.get("timestamp"),
                "account": stats.get("account"),
                "positions": stats.get("positions"),
                "market": stats.get("market"),
                "environment": stats.get("environment"),
                "api_status": stats.get("api_status"),
                "data_source": stats.get("data_source"),
            }
        except Exception as e:
            logger.error(f"get_trading_status error: {e}")
            return self._get_fallback_trading_stats()

# Global instance
production_data_manager = ProductionDataManager()

def get_production_data() -> ProductionDataManager:
    """Get the global production data manager instance"""
    return production_data_manager
