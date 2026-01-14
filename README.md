# DICT Procurement Management System

A comprehensive Government Procurement Management System for the Department of Information and Communications Technology (DICT), Philippines. Fully compliant with RA 9184 - Government Procurement Reform Act and COA regulations.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL/MariaDB
- Node.js (optional, for future build tools)

### Start Servers

#### Option 1: Use Batch Scripts (Windows)
```bash
# Start both servers
START_SERVERS.bat

# Or restart both
RESTART_SERVERS.bat
```

#### Option 2: Manual Start

**Backend API Server:**
```bash
cd fastAPI
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend Server:**
```bash
cd frontend
python server.py
```

### Access URLs
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/docs
- **Login Page:** http://localhost:3000/login.html

## 📋 Demo Accounts

- **Admin:** `admin@dict.gov.ph` / `AdminPass123!`
- **Procurement:** `procurement@dict.gov.ph` / `ProcurePass123!`
- **BAC Chair:** `bac@dict.gov.ph` / `BacPass123!`
- **End User:** `user@dict.gov.ph` / `UserPass123!`

## 🏗️ Project Structure

```
procurement/
├── fastAPI/              # Backend API (FastAPI)
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Core configuration
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic
│   └── requirements.txt
│
├── frontend/            # Frontend (Vue 3 + Tailwind)
│   ├── public/          # HTML pages
│   │   ├── js/         # JavaScript modules
│   │   └── *.html      # UI pages
│   └── src/            # Source files (for future build)
│
└── README.md
```

## ✅ Completed Features

### Phase 1: Authentication & API Client ✅
- ✅ Centralized API client with token management
- ✅ Authentication state management
- ✅ Protected route guards
- ✅ Login/logout functionality
- ✅ Token refresh mechanism
- ✅ Error handling

### Phase 2: Dashboard Integration (In Progress)
- ✅ Dashboard service with mock data
- ✅ Loading states and error handling
- ✅ Chart integration ready
- ⏭️ Real API integration pending

## 📚 Documentation

- **Implementation Plan:** `frontend/IMPLEMENTATION_PLAN.md`
- **API Client Docs:** `frontend/README_API_CLIENT.md`
- **Testing Guide:** `frontend/TESTING_GUIDE.md`
- **Backend Docs:** `fastAPI/README.md`

## 🔧 Technology Stack

### Backend
- **Framework:** FastAPI
- **ORM:** SQLAlchemy (async)
- **Database:** MySQL/MariaDB
- **Authentication:** JWT tokens
- **Validation:** Pydantic

### Frontend
- **Framework:** Vue 3 (CDN)
- **Styling:** Tailwind CSS
- **Icons:** Phosphor Icons
- **Charts:** Chart.js

## 📝 Development Status

- ✅ Phase 1: Core Infrastructure & Authentication
- 🔄 Phase 2: Dashboard & Navigation (In Progress)
- ⏭️ Phase 3: Purchase Request Management
- ⏭️ Phase 4-12: Additional features (see IMPLEMENTATION_PLAN.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Commit and push
5. Create a pull request

## 📄 License

This project is for the Department of Information and Communications Technology (DICT), Philippines.

## 🔗 Repository

GitHub: https://github.com/jaymarrecolizado-tech/fastAPIProc

---

**Status:** Development in Progress 🚀
