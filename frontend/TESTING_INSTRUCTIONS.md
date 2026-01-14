# Testing Instructions - Authentication

## 🚀 Servers Status

### Frontend Server
- **Status:** ✅ Running
- **URL:** http://localhost:3000
- **Serving from:** `frontend/public/`

### Backend API Server
- **Status:** ⚠️ **YOU NEED TO START THIS**
- **Command:** 
  ```bash
  cd fastAPI
  uvicorn app.main:app --reload
  ```
- **URL:** http://127.0.0.1:8000

---

## 📋 Quick Test Steps

### 1. Start Backend (Required for Authentication)

Open a **NEW terminal** and run:
```bash
cd fastAPI
uvicorn app.main:app --reload
```

Wait for: `Application startup complete`

### 2. Open Frontend

Open browser and go to:
```
http://localhost:3000/login.html
```

### 3. Test Login

1. **Open Browser DevTools** (F12)
2. **Go to Console tab**
3. **Click "Admin" demo account card**
4. **Click "Sign In" button**

**Expected:**
- ✅ Loading spinner appears
- ✅ Success message: "Login successful! Redirecting..."
- ✅ Redirects to dashboard
- ✅ No console errors

### 4. Verify Authentication

In browser console, type:
```javascript
// Check auth state
window.authStore.isAuthenticated
window.authStore.getCurrentUser()

// Check tokens
localStorage.getItem('access_token')
localStorage.getItem('refresh_token')
```

**Expected:**
- `isAuthenticated` = `true`
- `getCurrentUser()` = User object
- Tokens exist in localStorage

### 5. Test Protected Route

In console:
```javascript
// Clear tokens
localStorage.clear()
```

Then navigate to: `http://localhost:3000/dashboard.html`

**Expected:** Redirects to login page

### 6. Test Logout

1. Login again
2. Click "Logout" button on dashboard
3. Confirm logout

**Expected:** Redirects to login, tokens cleared

---

## 🧪 Interactive Test Page

For easier testing, use:
```
http://localhost:3000/test-auth.html
```

This page has:
- ✅ Auth state display
- ✅ Token info
- ✅ Test buttons
- ✅ Console output

---

## 🔍 Debug Commands

If something doesn't work, check in console:

```javascript
// Check if scripts loaded
console.log({
    api: typeof window.api,
    authStore: typeof window.authStore,
    TokenManager: typeof window.TokenManager,
    authGuard: typeof window.authGuard
});

// Check auth state
console.log({
    isAuthenticated: window.authStore?.isAuthenticated,
    user: window.authStore?.getCurrentUser(),
    hasToken: !!window.TokenManager?.getAccessToken(),
    tokenExpired: window.TokenManager?.isTokenExpired()
});
```

---

## ⚠️ Common Issues

### "Network error" or "Failed to fetch"
- **Solution:** Backend server not running
- Start backend: `cd fastAPI && uvicorn app.main:app --reload`

### "api is not defined"
- **Solution:** Scripts not loading
- Check browser Network tab for 404 errors
- Verify you're accessing `http://localhost:3000`

### Login works but dashboard shows errors
- **Solution:** Check console for specific errors
- Verify `auth-guard.js` is loaded
- Check if user data is stored correctly

### CORS errors
- **Solution:** Backend CORS should allow `http://localhost:3000`
- Check backend CORS configuration

---

## ✅ Test Checklist

- [ ] Backend server running (port 8000)
- [ ] Frontend server running (port 3000)
- [ ] Can access login page
- [ ] Scripts load without errors
- [ ] Login works
- [ ] Redirects to dashboard
- [ ] Dashboard shows user name
- [ ] Protected route works (redirects when not logged in)
- [ ] Logout works
- [ ] Tokens cleared after logout

---

## 📝 Test Results

After testing, note:
- ✅ What works
- ❌ What doesn't work
- 🔍 Any console errors
- 📊 Network request status

---

## 🎯 Next Steps

Once authentication is verified:
- ✅ Phase 1 Complete
- ⏭️ Proceed to Phase 2 (Dashboard Integration)
- ⏭️ Or continue with other features
