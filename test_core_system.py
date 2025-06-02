#!/usr/bin/env python3
"""
Core System Analysis and Dashboard Update
Test wszystkich komponentów folderu core i aktualizacja dashboard
"""

import sys
import os
import json
import logging
from datetime import datetime
from pathlib import Path

# Dodaj ścieżki do Pythona
project_root = Path(__file__).parent / "ZoL0-master"
sys.path.insert(0, str(project_root))

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

class CoreSystemAnalyzer:
    """Analizator systemu core - sprawdza wszystkie komponenty"""
    
    def __init__(self):
        self.core_path = project_root / "core"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "core_components": {},
            "strategies": {},
            "ai_models": {},
            "trading_engine": {},
            "portfolio": {},
            "risk_management": {},
            "monitoring": {},
            "issues": [],
            "recommendations": []
        }
    
    def analyze_core_structure(self):
        """Analizuje strukturę folderu core"""
        logger.info("Analizuję strukturę core...")
        
        components = {}
        for item in self.core_path.iterdir():
            if item.is_dir() and not item.name.startswith('__'):
                components[item.name] = {
                    "path": str(item),
                    "files": [f.name for f in item.glob("*.py")],
                    "submodules": [d.name for d in item.iterdir() if d.is_dir() and not d.name.startswith('__')]
                }
        
        self.results["core_components"] = components
        logger.info(f"Znaleziono {len(components)} głównych komponentów core")
        
    def test_strategies(self):
        """Testuje strategie tradingowe"""
        logger.info("Testuję strategie tradingowe...")
        
        try:
            from core.strategies.manager import StrategyManager
            
            manager = StrategyManager()
            strategies = manager.strategies
            
            self.results["strategies"] = {
                "total_count": len(strategies),
                "strategy_list": list(strategies.keys()),
                "loaded_successfully": True
            }
            
            # Test każdej strategii
            test_prices = [100.0, 101.0, 102.0, 100.5, 99.0]
            test_volume = [1000, 1100, 1200, 900, 800]
            
            strategy_results = {}
            for name, strategy in strategies.items():
                try:
                    # Test podstawowej funkcjonalności
                    if hasattr(strategy, 'analyze'):
                        result = strategy.analyze(test_prices, test_volume)
                        strategy_results[name] = {
                            "status": "working",
                            "result_type": type(result).__name__
                        }
                    else:
                        strategy_results[name] = {
                            "status": "missing_analyze_method"
                        }
                except Exception as e:
                    strategy_results[name] = {
                        "status": "error",
                        "error": str(e)
                    }
            
            self.results["strategies"]["individual_tests"] = strategy_results
            logger.info(f"Przetestowano {len(strategies)} strategii")
            
        except Exception as e:
            self.results["strategies"] = {
                "loaded_successfully": False,
                "error": str(e)
            }
            self.results["issues"].append(f"Strategy Manager error: {e}")
    
    def test_trading_engine(self):
        """Testuje silnik tradingowy"""
        logger.info("Testuję silnik tradingowy...")
        
        try:
            # Test importu głównych komponentów
            from core.trading.engine import TradingEngine
            from core.trading.executor import TradeExecutor
            
            self.results["trading_engine"] = {
                "engine_available": True,
                "executor_available": True,
                "components": ["engine", "executor", "handler"]
            }
            
            # Test podstawowej funkcjonalności
            engine = TradingEngine()
            if hasattr(engine, 'start'):
                self.results["trading_engine"]["start_method"] = True
            
        except ImportError as e:
            self.results["trading_engine"] = {
                "available": False,
                "import_error": str(e)
            }
            self.results["issues"].append(f"Trading engine import error: {e}")
        except Exception as e:
            self.results["trading_engine"]["error"] = str(e)
    
    def test_ai_integration(self):
        """Testuje integrację AI"""
        logger.info("Testuję integrację AI...")
        
        try:
            from core.ai.rl_trader import RLTrader
            from core.ai.model_exchange import ModelExchange
            
            self.results["ai_models"] = {
                "rl_trader_available": True,
                "model_exchange_available": True
            }
            
        except ImportError as e:
            self.results["ai_models"] = {
                "available": False,
                "import_error": str(e)
            }
    
    def test_portfolio_management(self):
        """Testuje zarządzanie portfelem"""
        logger.info("Testuję zarządzanie portfelem...")
        
        try:
            from core.portfolio.manager import PortfolioManager
            
            self.results["portfolio"] = {
                "manager_available": True
            }
            
        except ImportError as e:
            self.results["portfolio"] = {
                "available": False,
                "import_error": str(e)
            }
    
    def test_risk_management(self):
        """Testuje zarządzanie ryzykiem"""
        logger.info("Testuję zarządzanie ryzykiem...")
        
        try:
            from core.risk.manager import RiskManager
            
            self.results["risk_management"] = {
                "manager_available": True
            }
            
        except ImportError as e:
            self.results["risk_management"] = {
                "available": False,
                "import_error": str(e)
            }
    
    def test_monitoring(self):
        """Testuje system monitorowania"""
        logger.info("Testuję system monitorowania...")
        
        try:
            from core.monitoring.metrics import SystemMetrics
            from core.monitoring.autoswitch import AutoSwitch
            
            self.results["monitoring"] = {
                "metrics_available": True,
                "autoswitch_available": True
            }
            
        except ImportError as e:
            self.results["monitoring"] = {
                "available": False,
                "import_error": str(e)
            }
    
    def test_api_endpoints(self):
        """Testuje główne API endpoints"""
        logger.info("Testuję API endpoints...")
        
        try:
            from core.main import app
            
            # Test konfiguracji FastAPI
            self.results["api"] = {
                "fastapi_configured": True,
                "routes": [route.path for route in app.routes]
            }
            
        except Exception as e:
            self.results["api"] = {
                "error": str(e)
            }
    
    def generate_recommendations(self):
        """Generuje rekomendacje na podstawie analizy"""
        
        recommendations = []
        
        # Sprawdź czy wszystkie główne komponenty działają
        if not self.results.get("strategies", {}).get("loaded_successfully", False):
            recommendations.append("Fix strategy loading issues")
        
        if not self.results.get("trading_engine", {}).get("engine_available", False):
            recommendations.append("Fix trading engine imports")
        
        if not self.results.get("ai_models", {}).get("rl_trader_available", False):
            recommendations.append("Fix AI model integration")
        
        # Sprawdź liczba strategii
        strategy_count = self.results.get("strategies", {}).get("total_count", 0)
        if strategy_count < 3:
            recommendations.append("Add more trading strategies")
        
        # Dodaj rekomendacje dla dashboard
        recommendations.extend([
            "Add real-time core system monitoring to dashboard",
            "Integrate strategy performance metrics",
            "Add AI model status monitoring",
            "Create core system health dashboard section"
        ])
        
        self.results["recommendations"] = recommendations
    
    def run_analysis(self):
        """Uruchamia pełną analizę systemu core"""
        logger.info("=== ROZPOCZYNAM ANALIZĘ SYSTEMU CORE ===")
        
        self.analyze_core_structure()
        self.test_strategies()
        self.test_trading_engine()
        self.test_ai_integration()
        self.test_portfolio_management()
        self.test_risk_management()
        self.test_monitoring()
        self.test_api_endpoints()
        self.generate_recommendations()
        
        logger.info("=== ANALIZA ZAKOŃCZONA ===")
        return self.results

def main():
    """Główna funkcja"""
    analyzer = CoreSystemAnalyzer()
    results = analyzer.run_analysis()
    
    # Zapisz wyniki
    output_file = "CORE_SYSTEM_ANALYSIS.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Wyświetl podsumowanie
    print("\n" + "="*60)
    print("🔍 ANALIZA SYSTEMU CORE - PODSUMOWANIE")
    print("="*60)
    
    print(f"\n📁 KOMPONENTY CORE ({len(results['core_components'])} found):")
    for name in results['core_components'].keys():
        print(f"  ✅ {name}")
    
    print(f"\n🎯 STRATEGIE TRADINGOWE:")
    if results['strategies'].get('loaded_successfully'):
        count = results['strategies']['total_count']
        print(f"  ✅ Załadowano {count} strategii")
        for strategy in results['strategies']['strategy_list']:
            print(f"    - {strategy}")
    else:
        print(f"  ❌ Błąd ładowania strategii: {results['strategies'].get('error', 'Unknown')}")
    
    print(f"\n🚀 SILNIK TRADINGOWY:")
    if results['trading_engine'].get('engine_available'):
        print("  ✅ Trading Engine dostępny")
    else:
        print("  ❌ Trading Engine niedostępny")
    
    print(f"\n🤖 INTEGRACJA AI:")
    if results['ai_models'].get('rl_trader_available'):
        print("  ✅ RL Trader dostępny")
    else:
        print("  ❌ RL Trader niedostępny")
    
    print(f"\n📊 MONITOROWANIE:")
    if results['monitoring'].get('metrics_available'):
        print("  ✅ System metryk dostępny")
    else:
        print("  ❌ System metryk niedostępny")
    
    print(f"\n⚠️  PROBLEMY ZNALEZIONE ({len(results['issues'])}):")
    for issue in results['issues']:
        print(f"  - {issue}")
    
    print(f"\n💡 REKOMENDACJE ({len(results['recommendations'])}):")
    for rec in results['recommendations']:
        print(f"  - {rec}")
    
    print(f"\n📄 Szczegółowy raport zapisany w: {output_file}")
    
    return results

if __name__ == "__main__":
    main()
