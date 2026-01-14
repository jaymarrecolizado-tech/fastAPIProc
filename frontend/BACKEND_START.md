# Backend Server - Quick Start Guide

## ⚠️ Error: "Network error. Please check if the API server is running."

This error means the **backend API server is not running**. 

## 🚀 Start Backend Server

### Option 1: Using Terminal (Recommended)

1. **Open a NEW terminal window** (keep frontend server running)
2. Navigate to fastAPI directory:
   ```bash
   cd fastAPI
   ```
3. Start the server:
   ```bash
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

4. **Wait for this message:**
   ```
   Application startup complete.
   INFO:     Uvicorn running on http://127.0.0.1:8000
   ```

### Option 2: Using Python Directly

```bash
cd fastAPI
python -m uvicorn app.main:app --reload
```

## ✅ Verify Backend is Running

Open browser and go to:
- **API Docs:** http://127.0.0.1:8000/api/docs
- **Health Check:** http://127.0.0.1:8000/api/v1/health

You should see:
- API documentation (Swagger UI)
- Or JSON response: `{"status": "healthy", ...}`

## 🔧 Troubleshooting

### Port 8000 Already in Use
If you get "port already in use" error:
```bash
# Find what's using port 8000
netstat -ano | findstr :8000

# Or use a different port
python -m uvicorn app.main:app --reload --port 8001
```

Then update frontend API URL in `/public/js/api.js`:
```javascript
BASE_URL: 'http://127.0.0.1:8001/api/v1'
```

### Database Connection Error
If you see database errors:
1. Make sure MySQL/MariaDB is running
2. Check database credentials in `.env` file
3. Run migrations: `alembic upgrade head`

### Module Not Found
If you see import errors:
```bash
cd fastAPI
pip install -r requirements.txt
```

## 📋 Quick Checklist

- [ ] Backend server started
- [ ] See "Application startup complete" message
- [ ] Can access http://127.0.0.1:8000/api/docs
- [ ] Frontend server still running on port 3000
- [ ] Try login again - should work now!

## 🎯 After Backend Starts

1. **Go back to login page:** http://localhost:3000/login.html
2. **Click "Admin" demo account**
3. **Click "Sign In"**
4. **Should work now!** ✅

---

## Current Status

- ✅ Frontend: Running on http://localhost:3000
- ⚠️ Backend: **YOU NEED TO START THIS**
- ✅ CORS: Configured for localhost:3000
