/**
 * Centralized API Client
 * Handles all HTTP requests to the backend API with:
 * - Automatic token management
 * - Request/response interceptors
 * - Error handling
 * - Token refresh mechanism
 * - Retry logic
 */

// Configuration
const API_CONFIG = {
    BASE_URL: 'http://127.0.0.1:8000/api/v1',
    TIMEOUT: 30000, // 30 seconds
    RETRY_ATTEMPTS: 3,
    RETRY_DELAY: 1000, // 1 second
    ACCESS_TOKEN_EXPIRE_BUFFER: 5 * 60 * 1000, // Refresh 5 minutes before expiry
};

// Token storage keys
const TOKEN_KEYS = {
    ACCESS_TOKEN: 'access_token',
    REFRESH_TOKEN: 'refresh_token',
    TOKEN_EXPIRY: 'token_expiry',
    USER: 'user',
};

// Request queue for token refresh
let isRefreshing = false;
let refreshSubscribers = [];

/**
 * Token Management Utilities
 */
const TokenManager = {
    /**
     * Get access token from storage
     */
    getAccessToken() {
        return localStorage.getItem(TOKEN_KEYS.ACCESS_TOKEN);
    },

    /**
     * Get refresh token from storage
     */
    getRefreshToken() {
        return localStorage.getItem(TOKEN_KEYS.REFRESH_TOKEN);
    },

    /**
     * Set tokens in storage
     */
    setTokens(accessToken, refreshToken, expiresIn) {
        localStorage.setItem(TOKEN_KEYS.ACCESS_TOKEN, accessToken);
        localStorage.setItem(TOKEN_KEYS.REFRESH_TOKEN, refreshToken);
        
        // Calculate expiry time (expiresIn is in seconds)
        const expiryTime = Date.now() + (expiresIn * 1000);
        localStorage.setItem(TOKEN_KEYS.TOKEN_EXPIRY, expiryTime.toString());
    },

    /**
     * Clear all tokens
     */
    clearTokens() {
        localStorage.removeItem(TOKEN_KEYS.ACCESS_TOKEN);
        localStorage.removeItem(TOKEN_KEYS.REFRESH_TOKEN);
        localStorage.removeItem(TOKEN_KEYS.TOKEN_EXPIRY);
        localStorage.removeItem(TOKEN_KEYS.USER);
    },

    /**
     * Check if token is expired or about to expire
     */
    isTokenExpired() {
        const expiryTime = localStorage.getItem(TOKEN_KEYS.TOKEN_EXPIRY);
        if (!expiryTime) return true;
        
        const now = Date.now();
        const expiry = parseInt(expiryTime, 10);
        const buffer = API_CONFIG.ACCESS_TOKEN_EXPIRE_BUFFER;
        
        return now >= (expiry - buffer);
    },

    /**
     * Check if user is authenticated
     */
    isAuthenticated() {
        return !!this.getAccessToken() && !!this.getRefreshToken();
    }
};

/**
 * Subscribe to token refresh
 */
function subscribeTokenRefresh(callback) {
    refreshSubscribers.push(callback);
}

/**
 * Notify all subscribers when token is refreshed
 */
function onTokenRefreshed(token) {
    refreshSubscribers.forEach(callback => callback(token));
    refreshSubscribers = [];
}

/**
 * Refresh access token
 */
async function refreshAccessToken() {
    const refreshToken = TokenManager.getRefreshToken();
    
    if (!refreshToken) {
        throw new Error('No refresh token available');
    }

    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/auth/refresh`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                refresh_token: refreshToken
            })
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || 'Token refresh failed');
        }

        const data = await response.json();
        
        // Update tokens
        TokenManager.setTokens(
            data.access_token,
            data.refresh_token,
            data.expires_in
        );

        // Update user data if provided
        if (data.user) {
            localStorage.setItem(TOKEN_KEYS.USER, JSON.stringify(data.user));
        }

        onTokenRefreshed(data.access_token);
        return data.access_token;
    } catch (error) {
        // If refresh fails, clear tokens and redirect to login
        TokenManager.clearTokens();
        throw error;
    }
}

/**
 * Handle token refresh with queue management
 */
async function handleTokenRefresh() {
    if (isRefreshing) {
        // Wait for ongoing refresh
        return new Promise((resolve) => {
            subscribeTokenRefresh((token) => {
                resolve(token);
            });
        });
    }

    isRefreshing = true;
    try {
        const newToken = await refreshAccessToken();
        return newToken;
    } finally {
        isRefreshing = false;
    }
}

/**
 * Error handling utilities
 */
const ErrorHandler = {
    /**
     * Parse error response
     */
    async parseError(response) {
        let errorData;
        try {
            errorData = await response.json();
        } catch {
            errorData = {
                detail: response.statusText || 'An error occurred'
            };
        }

        return {
            status: response.status,
            statusText: response.statusText,
            message: errorData.detail || errorData.message || 'An error occurred',
            errors: errorData.errors || errorData.detail || {},
            data: errorData
        };
    },

    /**
     * Handle HTTP errors
     */
    handleError(error, response) {
        // Network error
        if (!response) {
            return {
                message: 'Network error. Please check your connection.',
                type: 'NETWORK_ERROR',
                originalError: error
            };
        }

        // HTTP errors
        switch (response.status) {
            case 401:
                return {
                    message: 'Authentication required. Please login again.',
                    type: 'UNAUTHORIZED',
                    status: 401
                };
            case 403:
                return {
                    message: 'You do not have permission to perform this action.',
                    type: 'FORBIDDEN',
                    status: 403
                };
            case 404:
                return {
                    message: 'The requested resource was not found.',
                    type: 'NOT_FOUND',
                    status: 404
                };
            case 422:
                return {
                    message: 'Validation error. Please check your input.',
                    type: 'VALIDATION_ERROR',
                    status: 422
                };
            case 429:
                return {
                    message: 'Too many requests. Please try again later.',
                    type: 'RATE_LIMIT',
                    status: 429
                };
            case 500:
                return {
                    message: 'Server error. Please try again later.',
                    type: 'SERVER_ERROR',
                    status: 500
                };
            default:
                return {
                    message: `Error ${response.status}: ${response.statusText}`,
                    type: 'HTTP_ERROR',
                    status: response.status
                };
        }
    }
};

/**
 * Retry logic for failed requests
 */
async function retryRequest(requestFn, retries = API_CONFIG.RETRY_ATTEMPTS) {
    let lastError;
    
    for (let i = 0; i < retries; i++) {
        try {
            return await requestFn();
        } catch (error) {
            lastError = error;
            
            // Don't retry on certain errors
            if (error.status === 401 || error.status === 403 || error.status === 404) {
                throw error;
            }
            
            // Wait before retry (exponential backoff)
            if (i < retries - 1) {
                await new Promise(resolve => 
                    setTimeout(resolve, API_CONFIG.RETRY_DELAY * (i + 1))
                );
            }
        }
    }
    
    throw lastError;
}

/**
 * Main API request function
 */
async function apiRequest(endpoint, options = {}) {
    const {
        method = 'GET',
        body = null,
        headers = {},
        requiresAuth = true,
        skipTokenRefresh = false,
        ...fetchOptions
    } = options;

    // Build URL
    const url = endpoint.startsWith('http') 
        ? endpoint 
        : `${API_CONFIG.BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;

    // Prepare headers
    const requestHeaders = {
        'Content-Type': 'application/json',
        ...headers
    };

    // Add authentication token if required
    if (requiresAuth && TokenManager.isAuthenticated()) {
        // Check if token needs refresh
        if (!skipTokenRefresh && TokenManager.isTokenExpired()) {
            try {
                await handleTokenRefresh();
            } catch (error) {
                // Redirect to login if refresh fails
                if (window.location.pathname !== '/login.html') {
                    window.location.href = '/login.html';
                }
                throw new Error('Session expired. Please login again.');
            }
        }

        const accessToken = TokenManager.getAccessToken();
        if (accessToken) {
            requestHeaders['Authorization'] = `Bearer ${accessToken}`;
        }
    }

    // Remove Content-Type for FormData
    if (body instanceof FormData) {
        delete requestHeaders['Content-Type'];
    }

    // Create request function
    const makeRequest = async () => {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.TIMEOUT);

        try {
            const response = await fetch(url, {
                method,
                headers: requestHeaders,
                body: body instanceof FormData ? body : (body ? JSON.stringify(body) : null),
                signal: controller.signal,
                ...fetchOptions
            });

            clearTimeout(timeoutId);

            // Handle 401 - try to refresh token once
            if (response.status === 401 && requiresAuth && !skipTokenRefresh) {
                try {
                    const newToken = await handleTokenRefresh();
                    // Retry request with new token
                    requestHeaders['Authorization'] = `Bearer ${newToken}`;
                    const retryResponse = await fetch(url, {
                        method,
                        headers: requestHeaders,
                        body: body instanceof FormData ? body : (body ? JSON.stringify(body) : null),
                        signal: controller.signal,
                        ...fetchOptions
                    });
                    return retryResponse;
                } catch (refreshError) {
                    // Refresh failed, clear tokens and redirect
                    TokenManager.clearTokens();
                    if (window.location.pathname !== '/login.html') {
                        window.location.href = '/login.html';
                    }
                    throw new Error('Session expired. Please login again.');
                }
            }

            return response;
        } catch (error) {
            clearTimeout(timeoutId);
            
            if (error.name === 'AbortError') {
                throw new Error('Request timeout. Please try again.');
            }
            
            throw error;
        }
    };

    // Execute request with retry logic
    const response = await retryRequest(makeRequest);

    // Handle non-OK responses
    if (!response.ok) {
        const errorInfo = await ErrorHandler.parseError(response);
        const error = ErrorHandler.handleError(errorInfo, response);
        error.response = response;
        error.errorInfo = errorInfo;
        throw error;
    }

    // Parse response
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
        return await response.json();
    }

    return await response.text();
}

/**
 * API Client Methods
 */
const api = {
    /**
     * GET request
     */
    async get(endpoint, options = {}) {
        return apiRequest(endpoint, { ...options, method: 'GET' });
    },

    /**
     * POST request
     */
    async post(endpoint, body, options = {}) {
        return apiRequest(endpoint, { ...options, method: 'POST', body });
    },

    /**
     * PUT request
     */
    async put(endpoint, body, options = {}) {
        return apiRequest(endpoint, { ...options, method: 'PUT', body });
    },

    /**
     * PATCH request
     */
    async patch(endpoint, body, options = {}) {
        return apiRequest(endpoint, { ...options, method: 'PATCH', body });
    },

    /**
     * DELETE request
     */
    async delete(endpoint, options = {}) {
        return apiRequest(endpoint, { ...options, method: 'DELETE' });
    },

    /**
     * Upload file
     */
    async upload(endpoint, formData, options = {}) {
        return apiRequest(endpoint, {
            ...options,
            method: 'POST',
            body: formData,
            headers: {
                // Don't set Content-Type, let browser set it with boundary
                ...options.headers
            }
        });
    },

    /**
     * Download file
     */
    async download(endpoint, filename, options = {}) {
        const response = await fetch(`${API_CONFIG.BASE_URL}${endpoint}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${TokenManager.getAccessToken()}`
            },
            ...options
        });

        if (!response.ok) {
            throw new Error('Download failed');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    },

    /**
     * Set base URL (for environment switching)
     */
    setBaseURL(url) {
        API_CONFIG.BASE_URL = url;
    },

    /**
     * Get current base URL
     */
    getBaseURL() {
        return API_CONFIG.BASE_URL;
    },

    /**
     * Token management (exposed for auth operations)
     */
    tokenManager: TokenManager
};

// Export for use in Vue components
if (typeof window !== 'undefined') {
    window.api = api;
}

// Export for ES modules (if using build tools)
export default api;
export { TokenManager, ErrorHandler };
