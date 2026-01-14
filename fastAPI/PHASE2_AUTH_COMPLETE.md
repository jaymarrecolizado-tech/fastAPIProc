# Phase 2: Authentication System - COMPLETE

## Overview

This phase implements the complete authentication system for the DICT Procurement Management System, including:

- ✅ Backend authentication API endpoints (6 endpoints)
- ✅ Rate limiting for security (5 attempts/min, 15-min lockout)
- ✅ JWT token-based authentication (access + refresh tokens)
- ✅ Modern Vue.js 3 login UI with Tailwind CSS
- ✅ Dashboard page with user information
- ✅ Complete authentication flow

---

## Backend API Endpoints

### Authentication Endpoints

All authentication endpoints are available at: `http://127.0.0.1:8000/api/v1/auth`

#### 1. Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 7200,
  "user": {
    "id": 1,
    "name": "Juan Dela Cruz",
    "email": "juan.delacruz@dict.gov.ph",
    "role": "ADMIN",
    "department": "Information Technology Service",
    "is_active": true,
    "last_login_at": "2026-01-13T18:00:00",
    "created_at": "2026-01-13T10:00:00"
  }
}
```

#### 2. Get Current User
```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

#### 3. Refresh Token
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 4. Logout
```http
POST /api/v1/auth/logout
Authorization: Bearer <access_token>
```

#### 5. Change Password
```http
POST /api/v1/auth/change-password
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "old_password": "oldpass123",
  "new_password": "newpass456"
}
```

#### 6. OAuth2 Login (for Swagger UI)
```http
POST /api/v1/auth/login/oauth2
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=password123
```

---

## Rate Limiting

The authentication system implements rate limiting to prevent brute force attacks:

- **Max Attempts**: 5 failed attempts per minute
- **Lockout Duration**: 15 minutes (900 seconds)
- **Algorithm**: Sliding window
- **Identifier**: Client IP address

**Rate Limit Exceeded Response (429 Too Many Requests):**
```json
{
  "detail": {
    "error": "Too many failed attempts. Account locked temporarily.",
    "lockout_remaining_seconds": 875,
    "lockout_remaining_minutes": 14
  }
}
```

---

## Frontend UI

### Login Page

**Location**: `frontend/public/login.html`
**Access**: http://localhost:3000/login.html

**Features:**
- Modern glassmorphism design with gradient background
- Email and password fields with icons
- Password visibility toggle
- Remember me checkbox
- Forgot password link
- Demo account buttons for quick testing
- Real-time error/success messages
- Loading spinner during authentication
- Responsive design (mobile-friendly)

**Demo Accounts:**
| Role | Email | Password |
|------|-------|----------|
| Admin | admin@dict.gov.ph | AdminPass123! |
| Procurement | procurement@dict.gov.ph | ProcurePass123! |
| BAC Chair | bac@dict.gov.ph | BacPass123! |
| End User | user@dict.gov.ph | UserPass123! |

### Dashboard Page

**Location**: `frontend/public/dashboard.html`
**Access**: http://localhost:3000/dashboard.html

**Features:**
- User welcome message with role display
- Statistics cards (PRs, Approved, Pending)
- User information table
- Logout button
- Token verification on load
- Auto-redirect to login if not authenticated

---

## How to Test

### Prerequisites

1. **Backend API Running:**
   ```bash
   cd C:/wamp64/www/procurement/fastAPI
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

2. **Database Setup** (if not already done):
   ```bash
   # Create database
   mysql -u root -p
   CREATE DATABASE dict_procurement CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   
   # Run migrations
   cd C:/wamp64/www/procurement/fastAPI
   alembic upgrade head
   ```

### Step 1: Start Backend Server

```bash
cd C:/wamp64/www/procurement/fastAPI
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Verify it's running:**
- Visit: http://127.0.0.1:8000/api/v1/health
- Should see: `{"status":"healthy",...}`

### Step 2: Start Frontend Server

Open a new terminal and run:

```bash
cd C:/wamp64/www/procurement/frontend
python server.py
```

**Output:**
```
🚀 Frontend server running at http://localhost:3000
📁 Serving files from: public/
🔐 Login page: http://localhost:3000/login.html
📊 Dashboard:  http://localhost:3000/dashboard.html
⚙️  Backend API: http://127.0.0.1:8000/api/v1
```

### Step 3: Test Login UI

1. Open browser: http://localhost:3000/login.html
2. Click any demo account button (e.g., "Admin")
3. Click "Sign In"
4. You should see:
   - Success message: "Login successful! Redirecting..."
   - Redirect to dashboard after 1 second

### Step 4: Verify Dashboard

After login, you should see:
- Welcome message with your name
- Your role displayed
- Statistics cards
- User information table
- Logout button

---

## Testing with cURL

### 1. Test Login

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@dict.gov.ph","password":"AdminPass123!"}'
```

**Expected Response:**
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer",
  "expires_in": 7200,
  "user": {...}
}
```

### 2. Test Get Current User

```bash
# Replace YOUR_ACCESS_TOKEN with the token from login
curl -X GET http://127.0.0.1:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. Test Rate Limiting

```bash
# Attempt 6 failed logins to trigger rate limit
for i in {1..6}; do
  curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"test@test.com","password":"wrongpass"}'
  echo ""
done
```

**Expected Response on 6th attempt:**
```json
{
  "detail": {
    "error": "Too many failed attempts. Account locked temporarily.",
    "lockout_remaining_seconds": 900,
    "lockout_remaining_minutes": 15
  }
}
```

---

## Files Created/Modified

### Backend Files (8 new files)

```
app/
├── core/
│   └── rate_limiter.py          # Rate limiting implementation
├── services/
│   ├── __init__.py
│   └── auth_service.py          # Authentication business logic
├── schemas/
│   └── auth.py                  # Authentication schemas
├── api/v1/endpoints/
│   └── auth.py                  # Authentication endpoints (6 endpoints)
└── main.py                      # Updated to include API router
```

### Frontend Files (3 new files)

```
frontend/
├── server.py                    # Simple HTTP server
└── public/
    ├── login.html               # Login page (Vue.js + Tailwind)
    └── dashboard.html           # Dashboard page (Vue.js + Tailwind)
```

---

## Security Features

### 1. Password Hashing
- Algorithm: bcrypt
- Cost Factor: 12
- Format: 60-character hash

### 2. JWT Tokens
- **Access Token**: Expires in 2 hours (7200 seconds)
- **Refresh Token**: Expires in 30 days
- Signing Algorithm: HS256
- Payload includes: user_id, email, role

### 3. Rate Limiting
- Sliding window algorithm
- 5 attempts per minute
- 15-minute lockout on violation
- Per-IP tracking

### 4. CORS Configuration
- Allowed origins: http://localhost:3000, http://localhost:5173
- Credentials: Enabled
- Methods: All
- Headers: All

---

## API Documentation

### Swagger UI

Interactive API documentation available at:
- **Swagger UI**: http://127.0.0.1:8000/api/docs
- **ReDoc**: http://127.0.0.1:8000/api/redoc
- **OpenAPI JSON**: http://127.0.0.1:8000/api/openapi.json

### Using Swagger UI for Authentication

1. Visit: http://127.0.0.1:8000/api/docs
2. Click "Authorize" button (lock icon)
3. Use OAuth2 password flow:
   - **client_id**: (leave empty)
   - **username**: `admin@dict.gov.ph`
   - **password**: `AdminPass123!`
4. Click "Authorize" then "Close"
5. Now you can test protected endpoints

---

## Troubleshooting

### Issue: "Network error" in login UI

**Cause**: Backend API not running

**Solution**:
```bash
cd C:/wamp64/www/procurement/fastAPI
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Issue: "Incorrect email or password"

**Cause**: User doesn't exist in database or wrong password

**Solution**: Create a test user:
```python
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash

async def create_test_user():
    async with AsyncSessionLocal() as db:
        user = User(
            name="Admin User",
            email="admin@dict.gov.ph",
            password_hash=get_password_hash("AdminPass123!"),
            role="ADMIN",
            department="ICT",
            is_active=True
        )
        db.add(user)
        await db.commit()
        print("User created!")
```

### Issue: "Too many failed attempts"

**Cause**: Rate limit triggered

**Solution**: Wait 15 minutes for lockout to expire, or restart the server

### Issue: CORS errors

**Cause**: Frontend trying to access backend from different port

**Solution**: Ensure CORS is configured in `app/core/config.py`:
```python
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

---

## Next Steps

### Phase 3: User Management
- [ ] Create user CRUD endpoints
- [ ] Admin user creation interface
- [ ] User list and search
- [ ] User activation/deactivation

### Phase 4: Purchase Request Workflow
- [ ] Create PR endpoint
- [ ] PR list and filtering
- [ ] PR detail view
- [ ] PR approval workflow

---

## Summary

✅ **Complete Authentication System Implemented**

**Backend:**
- 6 authentication endpoints
- JWT token-based auth
- Rate limiting for security
- Refresh token support
- Password change functionality

**Frontend:**
- Modern Vue.js 3 login UI
- Tailwind CSS styling
- Dashboard page
- Token management
- Error handling

**Testing:**
- Demo accounts included
- cURL examples provided
- Swagger UI available
- Complete authentication flow tested

**Status**: ✅ PHASE 2 COMPLETE  
**Servers**: 
- Backend: http://127.0.0.1:8000
- Frontend: http://localhost:3000

**Confidence**: HIGH (endpoints tested, UI functional)
