# API Client Documentation

## Overview

The centralized API client (`/public/js/api.js`) provides a robust, feature-rich HTTP client for communicating with the backend API. It handles authentication, token management, error handling, and request retries automatically.

## Features

✅ **Automatic Token Management**
- Stores access and refresh tokens
- Automatically refreshes tokens before expiry
- Handles token expiration gracefully

✅ **Request/Response Interceptors**
- Automatically adds Authorization headers
- Handles 401 errors with token refresh
- Parses JSON responses automatically

✅ **Error Handling**
- Comprehensive error parsing
- User-friendly error messages
- Network error detection

✅ **Retry Logic**
- Automatic retry on network failures
- Exponential backoff
- Configurable retry attempts

✅ **Request Timeout**
- 30-second default timeout
- Prevents hanging requests

## Usage

### Basic Setup

Include the API client script in your HTML before Vue:

```html
<!-- API Client -->
<script src="/js/api.js"></script>

<!-- Vue 3 -->
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
```

### Making API Calls

#### GET Request

```javascript
try {
    const data = await window.api.get('/purchase-requests');
    console.log(data);
} catch (error) {
    console.error('Error:', error.message);
}
```

#### POST Request

```javascript
try {
    const result = await window.api.post('/purchase-requests', {
        project_title: 'Office Supplies',
        estimated_budget: 50000
    });
    console.log('Created:', result);
} catch (error) {
    console.error('Error:', error.message);
}
```

#### PUT Request

```javascript
try {
    const updated = await window.api.put(`/purchase-requests/${id}`, {
        status: 'APPROVED'
    });
} catch (error) {
    console.error('Error:', error.message);
}
```

#### DELETE Request

```javascript
try {
    await window.api.delete(`/purchase-requests/${id}`);
    console.log('Deleted successfully');
} catch (error) {
    console.error('Error:', error.message);
}
```

#### File Upload

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('category', 'PR_DOCUMENT');

try {
    const result = await window.api.upload('/documents', formData);
    console.log('Uploaded:', result);
} catch (error) {
    console.error('Upload error:', error.message);
}
```

### Authentication

#### Login

```javascript
try {
    const data = await window.api.post('/auth/login', {
        email: 'user@dict.gov.ph',
        password: 'password123'
    }, {
        requiresAuth: false  // Don't require auth for login
    });
    
    // Tokens are automatically stored
    window.TokenManager.setTokens(
        data.access_token,
        data.refresh_token,
        data.expires_in
    );
    
    // Store user data
    localStorage.setItem('user', JSON.stringify(data.user));
} catch (error) {
    console.error('Login failed:', error.message);
}
```

#### Logout

```javascript
try {
    await window.api.post('/auth/logout');
    window.TokenManager.clearTokens();
    window.location.href = '/login.html';
} catch (error) {
    console.error('Logout error:', error.message);
}
```

### Token Management

```javascript
// Check if authenticated
if (window.TokenManager.isAuthenticated()) {
    console.log('User is authenticated');
}

// Get access token
const token = window.TokenManager.getAccessToken();

// Clear all tokens
window.TokenManager.clearTokens();

// Check if token is expired
if (window.TokenManager.isTokenExpired()) {
    console.log('Token needs refresh');
}
```

### Error Handling

```javascript
try {
    const data = await window.api.get('/purchase-requests');
} catch (error) {
    // Error object contains:
    // - message: User-friendly error message
    // - type: Error type (NETWORK_ERROR, UNAUTHORIZED, etc.)
    // - status: HTTP status code
    // - errorInfo: Detailed error information
    
    console.error('Error type:', error.type);
    console.error('Error message:', error.message);
    console.error('Status code:', error.status);
    
    // Handle specific error types
    if (error.type === 'UNAUTHORIZED') {
        // Redirect to login
        window.location.href = '/login.html';
    } else if (error.type === 'VALIDATION_ERROR') {
        // Show validation errors
        console.error('Validation errors:', error.errorInfo.errors);
    }
}
```

### Request Options

```javascript
// Custom headers
await window.api.get('/endpoint', {
    headers: {
        'Custom-Header': 'value'
    }
});

// Skip authentication
await window.api.get('/public-endpoint', {
    requiresAuth: false
});

// Skip token refresh check
await window.api.get('/endpoint', {
    skipTokenRefresh: true
});
```

## Configuration

You can modify the API configuration by editing `/public/js/api.js`:

```javascript
const API_CONFIG = {
    BASE_URL: 'http://127.0.0.1:8000/api/v1',  // Change API base URL
    TIMEOUT: 30000,                            // Request timeout (ms)
    RETRY_ATTEMPTS: 3,                         // Number of retries
    RETRY_DELAY: 1000,                         // Delay between retries (ms)
    ACCESS_TOKEN_EXPIRE_BUFFER: 5 * 60 * 1000  // Refresh 5 min before expiry
};
```

Or change it at runtime:

```javascript
window.api.setBaseURL('https://api.example.com/api/v1');
```

## Vue 3 Integration Example

```javascript
const { createApp, ref } = Vue;

createApp({
    setup() {
        const data = ref(null);
        const loading = ref(false);
        const error = ref(null);
        
        const fetchData = async () => {
            loading.value = true;
            error.value = null;
            
            try {
                data.value = await window.api.get('/purchase-requests');
            } catch (err) {
                error.value = err.message;
            } finally {
                loading.value = false;
            }
        };
        
        return {
            data,
            loading,
            error,
            fetchData
        };
    }
}).mount('#app');
```

## Error Types

- `NETWORK_ERROR`: Network connection failed
- `UNAUTHORIZED`: Authentication required (401)
- `FORBIDDEN`: Insufficient permissions (403)
- `NOT_FOUND`: Resource not found (404)
- `VALIDATION_ERROR`: Input validation failed (422)
- `RATE_LIMIT`: Too many requests (429)
- `SERVER_ERROR`: Server error (500)
- `HTTP_ERROR`: Other HTTP errors

## Best Practices

1. **Always use try-catch** when making API calls
2. **Handle errors appropriately** based on error type
3. **Check authentication** before making authenticated requests
4. **Use requiresAuth: false** for public endpoints
5. **Clear tokens on logout** to prevent unauthorized access

## Troubleshooting

### Token refresh fails
- Check if refresh token is valid
- Verify API endpoint is correct
- Check network connectivity

### Requests timeout
- Increase `TIMEOUT` in config
- Check server response time
- Verify network connection

### 401 errors persist
- Verify tokens are stored correctly
- Check token expiry
- Ensure API endpoint is correct

## Next Steps

- ✅ API Client created
- ⏭️ Update login page to use API client (Done)
- ⏭️ Create auth store for Vue components
- ⏭️ Add protected route guards
- ⏭️ Implement token refresh on page load
