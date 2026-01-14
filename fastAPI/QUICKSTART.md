# 🚀 QUICK START GUIDE

## ⚡ Fast Track to Running the System

This guide gets you from zero to running API in under 10 minutes.

---

## 📋 Prerequisites

Ensure you have installed:
- **Python 3.12+** - [Download here](https://www.python.org/downloads/)
- **MySQL 8.0+** - [Download here](https://dev.mysql.com/downloads/mysql/)
- **Git** - [Download here](https://git-scm.com/downloads)

---

## 🎯 5-Minute Setup

### Step 1: Install Dependencies (1 min)

```bash
# Install Python packages
pip install -r requirements.txt
```

### Step 2: Configure Database (2 min)

```bash
# Open MySQL Command Line
mysql -u root -p

# Run this command in MySQL
CREATE DATABASE dict_procurement CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### Step 3: Configure Environment (1 min)

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` file and update these lines:
```env
DATABASE_PASSWORD=your_mysql_password_here
SECRET_KEY=generate-with-openssl-rand-hex-32
```

**Generate Secret Key:**
```bash
openssl rand -hex 32
```

### Step 4: Run Validation Test (2 min)

```bash
python tests/test_phase1_validation.py
```

Expected output: `🎉 ALL TESTS PASSED! PHASE 1 COMPLETE!`

### Step 5: Start Application (1 min)

```bash
# Option 1: Run directly
python app/main.py

# Option 2: Use uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 6: Access API (instant)

Open browser:
- **API Docs**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **Root**: http://localhost:8000/

---

## ✅ Verify Installation

Run these commands to verify everything works:

```bash
# 1. Check Python version
python --version  # Should be 3.12+

# 2. Check MySQL connection
mysql -u root -p -e "SELECT VERSION();"

# 3. Test database
python tests/test_phase1_validation.py

# 4. Start app (in another terminal)
uvicorn app.main:app --reload

# 5. Test API (in another terminal)
curl http://localhost:8000/api/v1/health
```

**Expected Output:**
```json
{
  "status": "healthy",
  "service": "DICT Procurement Management System",
  "version": "1.0.0",
  "environment": "development"
}
```

---

## 🐳 Docker Setup (Even Faster!)

If you have Docker installed, it's even easier:

```bash
# Start all services (MySQL, Redis, App)
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

Access API at: http://localhost:8000/api/docs

---

## 📁 What Was Created

```
fastAPI/
├── 15 database models       (app/models/*.py)
├── Configuration system     (app/core/config.py)
├── Security utilities       (app/core/security.py)
├── Authentication deps      (app/core/deps.py)
├── FastAPI application      (app/main.py)
├── Validation tests         (tests/test_phase1_validation.py)
├── Docker setup            (docker-compose.yml)
└── Complete documentation   (README.md)
```

---

## 🔑 First Things to Do

After setup, do these in order:

1. **Create First User** (via database or future admin panel)
2. **Initialize Alembic** (for migrations)
   ```bash
   python scripts/init_alembic.py
   ```
3. **Create Initial Migration**
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```
4. **Apply Migration**
   ```bash
   alembic upgrade head
   ```

---

## 📊 Next Phase

**Phase 2: Authentication System**

Coming next:
- Login/logout endpoints
- JWT token management
- Rate limiting
- Password reset
- User registration

---

## 🆘 Troubleshooting

### MySQL Connection Error

**Problem:** `Can't connect to MySQL server`

**Solution:**
```bash
# Check MySQL is running
# Windows:
net start MySQL

# Linux:
sudo systemctl start mysql

# Mac:
brew services start mysql
```

### Module Not Found Error

**Problem:** `ModuleNotFoundError: No module named 'xxx'`

**Solution:**
```bash
pip install -r requirements.txt
```

### Port Already in Use

**Problem:** `Address already in use: port 8000`

**Solution:**
```bash
# Use different port
uvicorn app.main:app --port 8001

# Or kill process on port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

### Database Not Created

**Problem:** `Unknown database 'dict_procurement'`

**Solution:**
```bash
mysql -u root -p
CREATE DATABASE dict_procurement CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

---

## 📞 Need Help?

1. **Check README.md** - Comprehensive documentation
2. **Check PHASE1_COMPLETE.md** - Phase 1 details
3. **Run validation test** - `python tests/test_phase1_validation.py`
4. **Review logs** - `logs/app.log`

---

## 🎉 Success Indicators

You'll know everything is working when:

✅ Terminal shows: `Uvicorn running on http://0.0.0.0:8000`
✅ Browser opens to: http://localhost:8000/api/docs
✅ Health check returns: `{"status": "healthy"}`
✅ Validation test passes: `ALL TESTS PASSED`

---

## 📈 Progress Tracking

- ✅ **Phase 1**: Foundation (COMPLETE)
- ⏳ **Phase 2**: Authentication (NEXT)
- ⏳ **Phase 3-12**: Coming soon

**Current Status**: 8% complete (foundation ready)

---

## 🚀 Ready to Code!

Your development environment is ready. The API is running, database is connected, and all models are created.

**Next Step:** Start building Phase 2 - Authentication endpoints

---

*Last Updated: 2025-01-13*
*Version: 1.0.0*
*Phase: 1 Complete*
