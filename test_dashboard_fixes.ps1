# Test Dashboard Fixes - PowerShell Script
# Run this to start the system and test the applied fixes

Write-Host "🚀 Starting ZoL0 Dashboard System with Fixes" -ForegroundColor Green
Write-Host "=" -Repeat 50 -ForegroundColor Gray

# Check if we're in the right directory
if (!(Test-Path "unified_trading_dashboard.py")) {
    Write-Host "❌ Please run this script from the ZoL0 directory" -ForegroundColor Red
    Write-Host "📁 Expected files: unified_trading_dashboard.py, enhanced_dashboard_api.py" -ForegroundColor Yellow
    exit 1
}

Write-Host "📁 Current directory: $(Get-Location)" -ForegroundColor Cyan

# Start Enhanced Dashboard API in background
Write-Host "`n🔧 Starting Enhanced Dashboard API..." -ForegroundColor Yellow
$apiProcess = Start-Process python -ArgumentList "enhanced_dashboard_api.py" -PassThru -WindowStyle Minimized

# Wait a moment for API to start
Start-Sleep -Seconds 3

# Test API health
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5001/health" -TimeoutSec 5
    Write-Host "✅ Enhanced Dashboard API is running on port 5001" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Enhanced Dashboard API not responding (this is OK, dashboards will use fallback)" -ForegroundColor Yellow
}

Write-Host "`n🎯 Starting Dashboards..." -ForegroundColor Cyan

# Start Unified Dashboard (Port 8501)
Write-Host "`n📊 Starting Unified Dashboard on port 8501..." -ForegroundColor Blue
$unifiedProcess = Start-Process streamlit -ArgumentList "run", "unified_trading_dashboard.py", "--server.port", "8501" -PassThru

# Start Master Control Dashboard (Port 8503)  
Write-Host "📊 Starting Master Control Dashboard on port 8503..." -ForegroundColor Blue
$masterProcess = Start-Process streamlit -ArgumentList "run", "master_control_dashboard.py", "--server.port", "8503" -PassThru

# Start Advanced Trading Analytics (Port 8504)
Write-Host "📊 Starting Advanced Trading Analytics on port 8504..." -ForegroundColor Blue  
$advancedProcess = Start-Process streamlit -ArgumentList "run", "advanced_trading_analytics.py", "--server.port", "8504" -PassThru

# Wait for dashboards to start
Write-Host "`n⏳ Waiting for dashboards to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "`n" + "=" -Repeat 50 -ForegroundColor Gray
Write-Host "🎉 SYSTEM STARTED - Test the Fixes!" -ForegroundColor Green -BackgroundColor DarkGreen
Write-Host "=" -Repeat 50 -ForegroundColor Gray

Write-Host "`n📱 Dashboard URLs:" -ForegroundColor Cyan
Write-Host "  🏠 Unified Dashboard:     http://localhost:8501" -ForegroundColor White
Write-Host "  🎛️  Master Control:       http://localhost:8503" -ForegroundColor White  
Write-Host "  📈 Advanced Analytics:    http://localhost:8504" -ForegroundColor White
Write-Host "  🔧 API Health Check:      http://localhost:5001/health" -ForegroundColor White

Write-Host "`n✅ What to Test:" -ForegroundColor Green
Write-Host "  1. No more 'KeyError: Zysk' errors" -ForegroundColor White
Write-Host "  2. Data source shows 'real data' (green indicators)" -ForegroundColor White
Write-Host "  3. No more 'Unknown' data source status" -ForegroundColor White
Write-Host "  4. All metrics display properly" -ForegroundColor White
Write-Host "  5. Export functionality works" -ForegroundColor White

Write-Host "`n🛑 To Stop System:" -ForegroundColor Red
Write-Host "  Press Ctrl+C in each dashboard window, or run:" -ForegroundColor White
Write-Host "  Get-Process *streamlit* | Stop-Process -Force" -ForegroundColor Gray
Write-Host "  Get-Process *python* | Where {`$_.ProcessName -eq 'python'} | Stop-Process -Force" -ForegroundColor Gray

Write-Host "`n🔍 Process IDs:" -ForegroundColor Cyan
if ($apiProcess) { Write-Host "  API: $($apiProcess.Id)" -ForegroundColor White }
if ($unifiedProcess) { Write-Host "  Unified: $($unifiedProcess.Id)" -ForegroundColor White }
if ($masterProcess) { Write-Host "  Master: $($masterProcess.Id)" -ForegroundColor White }
if ($advancedProcess) { Write-Host "  Advanced: $($advancedProcess.Id)" -ForegroundColor White }

Write-Host "`n🎯 Ready for testing! Open the URLs above in your browser." -ForegroundColor Green
