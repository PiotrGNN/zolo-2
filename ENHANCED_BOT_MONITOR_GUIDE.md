# ZoL0 Enhanced Bot Monitor - Przewodnik Użytkownika

## 🎯 Cel
Enhanced Bot Monitor został stworzony, aby zapewnić kompleksowy podgląd działania bota tradingowego ZoL0 w czasie rzeczywistym.

## 🚀 Dostęp
- **Enhanced Bot Monitor**: http://localhost:8502
- **Podstawowy Dashboard**: http://localhost:8501  
- **API Backend**: http://localhost:5001

## 📊 Główne Funkcje

### 1. **Bot Current Activity** (Aktualna Aktywność Bota)
Pokazuje aktualny status bota:
- ✅ **Trading Status**: Czy bot aktywnie prowadzi transakcje
- 💰 **Portfolio**: Aktualny stan portfela i dostępne środki
- 📊 **Positions**: Liczba aktywnych pozycji
- 📋 **Orders**: Liczba oczekujących zleceń

### 2. **Detailed Bot Operations** (Szczegółowe Operacje)
Zawiera tabele z:
- **Active Positions**: Wszystkie otwarte pozycje z detalami
- **Pending Orders**: Zlecenia oczekujące na realizację

### 3. **Strategy Performance** (Wydajność Strategii)
Wyświetla:
- Win Rate dla każdej strategii
- Całkowity zysk/stratę
- Wykres porównawczy wydajności strategii

### 4. **Component Health Status** (Status Komponentów)
Monitoruje stan:
- System Components (API, Environment Manager, Trading Engine, etc.)
- AI Models Status
- Ogólną gotowość systemu

### 5. **Live System Logs** (Logi Systemowe na Żywo)
- Ostatnie 10-20 logów systemowych
- Kolorowe kodowanie według poziomu (ERROR, WARNING, INFO)
- Statystyki poziomów logów

### 6. **Alerts & Quick Actions** (Alerty i Szybkie Akcje)
- Automatyczne wykrywanie problemów systemowych
- Szybkie przyciski do uruchamiania/zatrzymywania tradingu
- Alerty o wysokim użyciu zasobów

## 🎛️ Kontrolki
- **Auto Refresh**: Automatyczne odświeżanie co 10 sekund
- **Refresh Interval**: Możliwość zmiany częstotliwości odświeżania (5s-60s)
- **Refresh Now**: Ręczne odświeżenie danych

## 🔄 Auto-Refresh
Monitor automatycznie odświeża dane, aby zapewnić:
- Aktualne informacje o statusie bota
- Najnowsze logi systemowe
- Bieżące alerty i ostrzeżenia

## 🚨 Interpretacja Alertów

### Poziomy Alertów:
- 🔴 **ERROR**: Krytyczne problemy wymagające natychmiastowej uwagi
- 🟡 **WARNING**: Ostrzeżenia o potencjalnych problemach
- 🟢 **SUCCESS**: Wszystko działa prawidłowo
- 🔵 **INFO**: Informacje o normalnym działaniu systemu

### Typowe Alerty:
- **High CPU/Memory Usage**: Wysokie użycie zasobów systemowych
- **Trading Engine Not Initialized**: Trading engine nie jest zainicjalizowany
- **System Not Ready for Production**: System nie jest gotowy do trybu produkcyjnego
- **Error Logs Detected**: Wykryto błędy w logach

## 📋 Endpointy API

Monitor wykorzystuje następujące endpointy API:

```
GET /api/bot/activity        - Aktualna aktywność bota
GET /api/bot/performance     - Metryki wydajności
GET /api/bot/logs           - Ostatnie logi systemowe  
GET /api/bot/alerts         - Aktualne alerty systemowe
GET /api/system/validation  - Walidacja komponentów
GET /api/environment/status - Status środowiska
GET /api/portfolio          - Status portfela
GET /core/strategies        - Status strategii
POST /api/trading/start     - Uruchom trading
POST /api/trading/stop      - Zatrzymaj trading
```

## ⚡ Szybkie Akcje

### Uruchomienie Tradingu:
1. Sprawdź status w sekcji "Bot Current Activity"
2. Upewnij się, że wszystkie komponenty są aktywne
3. Kliknij przycisk "🚀 Start Trading"

### Zatrzymanie Tradingu:
1. Kliknij przycisk "🛑 Stop Trading"
2. Sprawdź czy pozycje zostały poprawnie zamknięte

## 🔧 Rozwiązywanie Problemów

### Bot nie traduje:
1. Sprawdź "Component Health Status"
2. Upewnij się, że "Trading Status" pokazuje "ACTIVE"
3. Sprawdź alerty w sekcji "Alerts & Quick Actions"

### Błędy w logach:
1. Przejrzyj "Live System Logs"
2. Zwróć uwagę na logi z poziomem ERROR
3. Sprawdź szczegóły w logach systemowych

### Wysokie użycie zasobów:
1. Monitoruj alerty o CPU/Memory
2. Sprawdź liczbę aktywnych pozycji
3. Rozważ zmniejszenie częstotliwości operacji

## 📱 Responsywność
Monitor jest zoptymalizowany dla:
- Przeglądarek desktopowych (Chrome, Firefox, Edge)
- Szerokich ekranów (monitor desktop)
- Rozdzielczości Full HD i wyższych

## 🔄 Aktualizacje w Czasie Rzeczywistym
Dane są odświeżane automatycznie co 10 sekund (domyślnie), zapewniając:
- Aktualne statusy wszystkich komponentów
- Najnowsze logi i alerty
- Bieżące dane o portfelu i pozycjach

---

**Uwaga**: Ten monitor jest narzędziem diagnostycznym i nie zastępuje profesjonalnego monitorowania w środowisku produkcyjnym. Zawsze śledź również logi systemowe i alerty bezpieczeństwa.
