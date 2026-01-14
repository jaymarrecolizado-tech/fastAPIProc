@echo off
echo ========================================
echo Restarting DICT Procurement Servers
echo ========================================
echo.

echo Stopping existing servers...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Backend*" 2>nul
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Frontend*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting Backend API Server (Port 8000)...
start "Backend API Server" cmd /k "cd /d %~dp0fastAPI && echo ======================================== && echo Backend API Server ^(Port 8000^) && echo ======================================== && echo. && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 2 /nobreak >nul

echo Starting Frontend Server (Port 3000)...
start "Frontend Server" cmd /k "cd /d %~dp0frontend && echo ======================================== && echo Frontend Server ^(Port 3000^) && echo ======================================== && echo. && python server.py"

echo.
echo ========================================
echo Both servers are restarting in new windows
echo ========================================
echo.
echo Wait 5-10 seconds for servers to start
echo.
echo Backend API: http://localhost:8000/api/docs
echo Frontend:    http://localhost:3000/login.html
echo.
echo Press any key to exit...
pause >nul
