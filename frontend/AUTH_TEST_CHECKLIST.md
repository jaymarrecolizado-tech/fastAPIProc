# Authentication Test Checklist ✅

## Pre-Test Setup

- [ ] Backend API server is running (`http://127.0.0.1:8000`)
- [ ] Frontend server is running (serving from `frontend/public/`)
- [ ] Browser DevTools open (F12) with Console tab visible

---

## Test 1: Script Loading ✅

**Action:** Navigate to `/login.html`

**Check Console:**
```javascript
typeof window.api          // Should be "object"
typeof window.TokenManager // Should be "object"  
typeof window.authStore    // Should be "object"
```

**Expected:** All scripts loaded, no 404 errors

**Status:** ⬜ Pass / ⬜ Fail

---

## Test 2: Login Functionality ✅

**Action:** 
1. Click "Admin" demo account card
2. Click "Sign In" button

**Expected:**
- ✅ Email and password auto-filled
- ✅ Loading spinner appears
- ✅ Success message: "Login successful! Redirecting..."
- ✅ Redirects to dashboard after ~1 second
- ✅ No console errors

**Check localStorage:**
```javascript
localStorage.getItem('access_token')  // Should have token
localStorage.getItem('refresh_token') // Should have token
localStorage.getItem('user')         // Should have user JSON
```

**Status:** ⬜ Pass / ⬜ Fail

---

## Test 3: Dashboard Access ✅

**Action:** After login, verify dashboard loads

**Expected:**
- ✅ Dashboard page loads
- ✅ User name appears in header
- ✅ No console errors
- ✅ Dashboard data starts loading

**Check:**
```javascript
window.authStore.isAuthenticated  // Should be true
window.authStore.getCurrentUser() // Should show user object
```

**Status:** ⬜ Pass / ⬜ Fail

---

## Test 4: Protected Route ✅

**Action:**
1. Clear tokens: `localStorage.clear()`
2. Navigate to `/dashboard.html`

**Expected:**
- ✅ Redirects to `/login.html`
- ✅ Cannot access dashboard without login

**Status:** ⬜ Pass / ⬜ Fail

---

## Test 5: Auto-Redirect (Already Logged In) ✅

**Action:**
1. Login successfully
2. Navigate to `/login.html` again

**Expected:**
- ✅ Automatically redirects to dashboard
- ✅ Does not show login form

**Status:** ⬜ Pass / ⬜ Fail

---

## Test 6: Logout ✅

**Action:** Click "Logout" button on dashboard

**Expected:**
- ✅ Confirmation dialog appears
- ✅ After confirm, redirects to login
- ✅ Tokens cleared from localStorage
- ✅ Cannot access dashboard without re-login

**Check:**
```javascript
localStorage.getItem('access_token')  // Should be null
window.authStore.isAuthenticated      // Should be false
```

**Status:** ⬜ Pass / ⬜ Fail

---

## Test 7: Token Refresh ✅

**Action:**
1. Login successfully
2. In console, expire token:
   ```javascript
   localStorage.setItem('token_expiry', (Date.now() - 1000).toString());
   ```
3. Make API call:
   ```javascript
   window.api.get('/auth/me').then(console.log);
   ```

**Expected:**
- ✅ Token automatically refreshes
- ✅ API call succeeds
- ✅ New token stored
- ✅ No redirect to login

**Status:** ⬜ Pass / ⬜ Fail

---

## Test 8: Error Handling ✅

**Test Invalid Credentials:**
- Enter wrong email/password
- Click "Sign In"

**Expected:**
- ✅ Error message displayed
- ✅ No redirect
- ✅ Tokens not stored

**Test Network Error:**
- Stop backend server
- Try to login

**Expected:**
- ✅ Error message: "Network error..."
- ✅ No redirect

**Status:** ⬜ Pass / ⬜ Fail

---

## Test 9: Session Persistence ✅

**Action:**
1. Login successfully
2. Close browser tab
3. Reopen browser
4. Navigate to `/dashboard.html`

**Expected:**
- ✅ Still authenticated
- ✅ Dashboard loads without login
- ✅ User data persists

**Status:** ⬜ Pass / ⬜ Fail

---

## Quick Debug Commands

```javascript
// Check everything
console.log('API:', window.api);
console.log('Auth:', window.authStore.isAuthenticated);
console.log('User:', window.authStore.getCurrentUser());
console.log('Token:', window.TokenManager.getAccessToken() ? 'Exists' : 'Missing');
console.log('Expired:', window.TokenManager.isTokenExpired());

// Clear everything
localStorage.clear();
window.authStore.clearAuth();
location.reload();
```

---

## Common Issues

### Scripts Not Loading
- Check file paths: `/js/api.js`, `/js/auth-store.js`
- Check browser Network tab for 404 errors
- Verify server is serving files correctly

### API Errors
- Verify backend is running on `http://127.0.0.1:8000`
- Check CORS settings
- Check Network tab for failed requests

### Redirect Issues
- Check `auth-guard.js` is loaded on dashboard
- Verify script loading order
- Check console for errors

---

## Test Results Summary

- Total Tests: 9
- Passed: ___
- Failed: ___

**Overall Status:** ⬜ Ready / ⬜ Needs Fixes

---

## Next Steps

If all tests pass:
- ✅ Authentication is working correctly
- ✅ Ready to proceed with Phase 2
- ✅ Can integrate with backend API

If tests fail:
- Note which tests failed
- Check console for errors
- Review error messages
- Fix issues before proceeding
