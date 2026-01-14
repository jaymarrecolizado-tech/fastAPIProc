# 🔴 CORS Error - Quick Fix

## Problem
Backend server is running but **didn't reload** the CORS configuration changes.

## ✅ Solution: Restart Backend Server

### Step 1: Stop Backend Server
In the **Backend API Server** window:
- Press `Ctrl+C` to stop the server
- Wait for it to fully stop

### Step 2: Restart Backend Server
In the same window, run:
```bash
cd fastAPI
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Important:** Make sure you see:
```
Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Verify CORS
After restart, the backend should now allow requests from `http://localhost:3000`

### Step 4: Test Login
1. **Hard refresh** login page: `Ctrl+F5`
2. Try login again
3. CORS error should be gone! ✅

---

## Alternative: Use RESTART_SERVERS.bat

Double-click `RESTART_SERVERS.bat` in the project root to restart both servers automatically.

---

## Why This Happens

When you modify `config.py`, the server needs to restart to reload the configuration. The `--reload` flag only watches Python files, not config changes in some cases.

---

## Verify CORS is Working

After restart, check browser console:
- ✅ No CORS errors
- ✅ Successful API calls
- ✅ Login works
