# Testing Guide - Phase 1: Authentication & API Client

## Prerequisites

1. **Backend API Server Running**
   ```bash
   cd fastAPI
   uvicorn app.main:app --reload
   ```
   Server should be running at `http://127.0.0.1:8000`

2. **Frontend Server Running**
   ```bash
   cd frontend
   python server.py
   ```
   Or use any static file server serving from `frontend/public/`

3. **Test Users Available**
   - Admin: `admin@dict.gov.ph` / `AdminPass123!`
   - Procurement: `procurement@dict.gov.ph` / `ProcurePass123!`
   - BAC: `bac@dict.gov.ph` / `BacPass123!`
   - End User: `user@dict.gov.ph` / `UserPass123!`

## Test 1: API Client Loading

### Steps:
1. Open browser console (F12)
2. Navigate to `http://localhost:8000/login.html` (or your frontend URL)
3. Check console for errors

### Expected Result:
- No errors in console
- `window.api` object available
- `window.TokenManager` object available
- `window.authStore` object available
- `window.authGuard` object available (after loading dashboard)

### Test Commands:
```javascript
// In browser console
console.log(window.api);
console.log(window.TokenManager);
console.log(window.authStore);
```

## Test 2: Login Functionality

### Steps:
1. Navigate to login page
2. Enter credentials: `admin@dict.gov.ph` / `AdminPass123!`
3. Click "Sign In" button
4. Observe behavior

### Expected Result:
- Loading spinner appears
- Success message: "Login successful! Redirecting..."
- Redirects to dashboard after 1 second
- Tokens stored in localStorage
- User data stored in localStorage

### Verify in Console:
```javascript
// Check tokens
localStorage.getItem('access_token');
localStorage.getItem('refresh_token');
localStorage.getItem('user');

// Check auth state
window.TokenManager.isAuthenticated(); // Should return true
window.authStore.isAuthenticated; // Should return true
window.authStore.user; // Should show user object
```

## Test 3: Auto-Redirect (Already Authenticated)

### Steps:
1. Login successfully
2. Navigate to `/login.html` again
3. Observe behavior

### Expected Result:
- Automatically redirects to dashboard
- No login form shown

## Test 4: Protected Route Guard

### Steps:
1. **Without Login:**
   - Clear localStorage: `localStorage.clear()`
   - Navigate to `/dashboard.html`
   - Observe behavior

2. **With Login:**
   - Login successfully
   - Navigate to `/dashboard.html`
   - Observe behavior

### Expected Result:
- **Without Login:** Redirects to `/login.html`
- **With Login:** Dashboard loads successfully
- User data displayed in header

## Test 5: Token Refresh

### Steps:
1. Login successfully
2. In console, manually expire token:
   ```javascript
   localStorage.setItem('token_expiry', (Date.now() - 1000).toString());
   ```
3. Make an API call:
   ```javascript
   window.api.get('/auth/me');
   ```

### Expected Result:
- Token automatically refreshed
- API call succeeds
- New token stored

## Test 6: Logout Functionality

### Steps:
1. Login successfully
2. Navigate to dashboard
3. Click "Logout" button
4. Confirm logout

### Expected Result:
- Confirmation dialog appears
- After confirmation:
  - Tokens cleared from localStorage
  - User data cleared
  - Redirects to login page
  - Cannot access dashboard without login

### Verify:
```javascript
// After logout
localStorage.getItem('access_token'); // Should be null
window.TokenManager.isAuthenticated(); // Should return false
window.authStore.isAuthenticated; // Should return false
```

## Test 7: Error Handling

### Test Invalid Credentials:
1. Enter wrong email/password
2. Click "Sign In"

### Expected Result:
- Error message displayed
- No redirect
- Tokens not stored

### Test Network Error:
1. Stop backend server
2. Try to login

### Expected Result:
- Error message: "Network error. Please check your connection."
- No redirect

### Test API Error:
1. Login with invalid format email
2. Click "Sign In"

### Expected Result:
- Validation error message displayed
- User-friendly error message

## Test 8: Demo Account Quick Login

### Steps:
1. Click on any demo account card (Admin, Procurement, BAC, End User)
2. Observe form fields

### Expected Result:
- Email and password auto-filled
- Selected card highlighted
- Can click "Sign In" immediately

## Test 9: Session Persistence

### Steps:
1. Login successfully
2. Close browser tab
3. Reopen browser
4. Navigate to `/dashboard.html`

### Expected Result:
- Still authenticated
- Dashboard loads without login
- User data persists

## Test 10: Token Expiry Handling

### Steps:
1. Login successfully
2. Wait for token to expire (or manually expire)
3. Try to access dashboard

### Expected Result:
- Token automatically refreshed
- Dashboard loads successfully
- No redirect to login

## Test 11: Multiple Tabs

### Steps:
1. Login in Tab 1
2. Open Tab 2, navigate to dashboard
3. Logout in Tab 1
4. Try to use Tab 2

### Expected Result:
- Tab 2 still works (tokens in localStorage)
- On next API call, will detect expired session
- Will redirect to login

## Test 12: API Client Methods

### Test GET Request:
```javascript
// In browser console (after login)
window.api.get('/auth/me').then(data => console.log(data));
```

### Test POST Request:
```javascript
// Test with invalid data to see error handling
window.api.post('/purchase-requests', {}).catch(err => console.log(err));
```

### Expected Result:
- GET request succeeds (if authenticated)
- POST request shows appropriate error

## Common Issues & Solutions

### Issue: "api is not defined"
**Solution:** Make sure `/js/api.js` is loaded before Vue scripts

### Issue: "TokenManager is not defined"
**Solution:** Check that API client script is loaded correctly

### Issue: Login redirects but dashboard shows errors
**Solution:** Check browser console for API errors, verify backend is running

### Issue: Tokens not persisting
**Solution:** Check localStorage is enabled, check for browser privacy settings

### Issue: CORS errors
**Solution:** Make sure backend CORS is configured correctly

## Browser Compatibility

Tested browsers:
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari

## Performance Checks

1. **Page Load Time:** Should be < 2 seconds
2. **Login Response:** Should be < 1 second
3. **Token Refresh:** Should be transparent (< 500ms)

## Security Checks

1. ✅ Tokens stored in localStorage (not cookies)
2. ✅ Tokens automatically cleared on logout
3. ✅ Protected routes redirect to login
4. ✅ Token refresh happens automatically
5. ✅ No tokens exposed in URLs

## Next Steps After Testing

Once all tests pass:
1. ✅ Phase 1.1 Complete - API Client
2. ✅ Phase 1.2 Complete - Auth State Management
3. ✅ Phase 1.3 Complete - Auth Integration
4. ⏭️ Move to Phase 2: Dashboard Integration

## Reporting Issues

If you encounter issues:
1. Check browser console for errors
2. Check network tab for failed requests
3. Verify backend API is running
4. Check localStorage for token storage
5. Verify CORS configuration
