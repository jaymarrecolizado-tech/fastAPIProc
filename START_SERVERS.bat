@echo off
echo ========================================
echo Starting DICT Procurement Servers
echo ========================================
echo.

echo Starting Backend API Server (Port 8000)...
start "Backend API Server" cmd /k "cd /d %~dp0fastAPI && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

timeout /t 2 /nobreak >nul

echo Starting Frontend Server (Port 3000)...
start "Frontend Server" cmd /k "cd /d %~dp0frontend && python server.py"

echo.
echo ========================================
echo Both servers are starting in new windows
echo ========================================
echo.
echo Backend API: http://127.0.0.1:8000/api/docs
echo Frontend:    http://localhost:3000/login.html
echo.
echo Press any key to exit this window...
pause >nul
