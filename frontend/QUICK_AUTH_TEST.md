# Quick Authentication Test Guide

## Prerequisites

1. **Backend API Server Must Be Running**
   ```bash
   cd fastAPI
   uvicorn app.main:app --reload
   ```
   Should be accessible at: `http://127.0.0.1:8000`

2. **Frontend Server Running**
   - Use any static file server serving from `frontend/public/`
   - Or use Python: `cd frontend && python server.py`
   - Or use VS Code Live Server extension

## Step-by-Step Test

### Test 1: Check Scripts Loading

1. Open browser DevTools (F12)
2. Navigate to: `http://localhost:8000/login.html` (or your frontend URL)
3. Open Console tab
4. Type and check:
   ```javascript
   // Check if scripts loaded
   console.log('API Client:', typeof window.api);
   console.log('TokenManager:', typeof window.TokenManager);
   console.log('AuthStore:', typeof window.authStore);
   ```
   
   **Expected:** All should show "object" or "function"

### Test 2: Login Test

1. On login page, click a demo account (e.g., "Admin")
2. Click "Sign In" button
3. Watch for:
   - Loading spinner appears
   - Success message: "Login successful! Redirecting..."
   - Redirects to dashboard after 1 second

4. **Check Console:**
   - Should see no errors
   - May see successful API call logs

5. **Check localStorage:**
   ```javascript
   // In console
   localStorage.getItem('access_token'); // Should have token
   localStorage.getItem('refresh_token'); // Should have token
   localStorage.getItem('user'); // Should have user JSON
   ```

### Test 3: Dashboard Access Test

1. After login, you should be on dashboard
2. Check if user name appears in header
3. Check console for errors

### Test 4: Protected Route Test

1. **Clear tokens:**
   ```javascript
   localStorage.clear();
   ```

2. **Try to access dashboard:**
   - Navigate to `/dashboard.html`
   - Should redirect to `/login.html`

3. **Login again:**
   - Should redirect back to dashboard

### Test 5: Logout Test

1. On dashboard, click "Logout" button
2. Confirm logout
3. Should redirect to login page
4. Check localStorage:
   ```javascript
   localStorage.getItem('access_token'); // Should be null
   ```

### Test 6: Token Refresh Test

1. Login successfully
2. In console, manually expire token:
   ```javascript
   localStorage.setItem('token_expiry', (Date.now() - 1000).toString());
   ```
3. Make an API call:
   ```javascript
   window.api.get('/auth/me').then(data => console.log('User:', data));
   ```
4. **Expected:** Token should refresh automatically, API call succeeds

## Common Issues & Solutions

### Issue: "api is not defined"
**Solution:** 
- Check that `/js/api.js` is loaded before Vue scripts
- Check browser console for 404 errors on script files
- Verify file paths are correct

### Issue: "Network error"
**Solution:**
- Verify backend is running on `http://127.0.0.1:8000`
- Check CORS settings in backend
- Check browser Network tab for failed requests

### Issue: "401 Unauthorized"
**Solution:**
- Check if tokens are stored correctly
- Verify token format in localStorage
- Check backend authentication endpoint

### Issue: Login works but dashboard shows errors
**Solution:**
- Check if `/js/auth-guard.js` is loaded
- Check console for specific errors
- Verify user data is stored correctly

## Quick Test Page

Use `/test-auth.html` for interactive testing:
- Shows auth state
- Shows token info
- Test buttons for login/logout/API calls
- Console output for debugging

## Expected Behavior

✅ **Login:**
- Form validates
- Shows loading state
- Stores tokens
- Redirects to dashboard

✅ **Dashboard:**
- Checks authentication
- Loads user data
- Shows user name
- Protected from unauthorized access

✅ **Logout:**
- Clears tokens
- Clears user data
- Redirects to login

✅ **Token Refresh:**
- Happens automatically
- Transparent to user
- No interruption

## Debug Commands

```javascript
// Check auth state
window.authStore.isAuthenticated;
window.authStore.getCurrentUser();

// Check tokens
window.TokenManager.getAccessToken();
window.TokenManager.isTokenExpired();

// Test API call
window.api.get('/auth/me').then(console.log).catch(console.error);

// Clear everything
localStorage.clear();
window.authStore.clearAuth();
```

## Next Steps After Testing

If all tests pass:
- ✅ Authentication is working
- ✅ Ready to proceed with Phase 2
- ✅ Can integrate with backend API

If issues found:
- Check browser console for errors
- Verify backend is running
- Check file paths and script loading order
- Review error messages for clues
