# Start Both Servers Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting DICT Procurement Servers" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Start Backend Server
Write-Host "Starting Backend API Server (Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir\fastAPI'; Write-Host 'Backend API Server Starting...' -ForegroundColor Green; python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000" -WindowStyle Normal

Start-Sleep -Seconds 2

# Start Frontend Server
Write-Host "Starting Frontend Server (Port 3000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir\frontend'; Write-Host 'Frontend Server Starting...' -ForegroundColor Green; python server.py" -WindowStyle Normal

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Both servers are starting in new windows" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API: http://127.0.0.1:8000/api/docs" -ForegroundColor Green
Write-Host "Frontend:    http://localhost:3000/login.html" -ForegroundColor Green
Write-Host ""
Write-Host "Wait 5-10 seconds for servers to start, then test authentication!" -ForegroundColor Yellow
Write-Host ""
