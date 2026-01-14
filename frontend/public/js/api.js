/**
 * Centralized API Client - Browser Compatible Version
 * Works directly in HTML pages without build tools
 */

(function() {
    'use strict';

    // Configuration
    const API_CONFIG = {
        BASE_URL: 'http://localhost:8000/api/v1',
        TIMEOUT: 30000,
        RETRY_ATTEMPTS: 3,
        RETRY_DELAY: 1000,
        ACCESS_TOKEN_EXPIRE_BUFFER: 5 * 60 * 1000, // 5 minutes
    };

    const TOKEN_KEYS = {
        ACCESS_TOKEN: 'access_token',
        REFRESH_TOKEN: 'refresh_token',
        TOKEN_EXPIRY: 'token_expiry',
        USER: 'user',
    };

    // Token refresh state
    let isRefreshing = false;
    let refreshSubscribers = [];

    /**
     * Token Manager
     */
    const TokenManager = {
        getAccessToken() {
            return localStorage.getItem(TOKEN_KEYS.ACCESS_TOKEN);
        },

        getRefreshToken() {
            return localStorage.getItem(TOKEN_KEYS.REFRESH_TOKEN);
        },

        setTokens(accessToken, refreshToken, expiresIn) {
            localStorage.setItem(TOKEN_KEYS.ACCESS_TOKEN, accessToken);
            localStorage.setItem(TOKEN_KEYS.REFRESH_TOKEN, refreshToken);
            const expiryTime = Date.now() + (expiresIn * 1000);
            localStorage.setItem(TOKEN_KEYS.TOKEN_EXPIRY, expiryTime.toString());
        },

        clearTokens() {
            localStorage.removeItem(TOKEN_KEYS.ACCESS_TOKEN);
            localStorage.removeItem(TOKEN_KEYS.REFRESH_TOKEN);
            localStorage.removeItem(TOKEN_KEYS.TOKEN_EXPIRY);
            localStorage.removeItem(TOKEN_KEYS.USER);
        },

        isTokenExpired() {
            const expiryTime = localStorage.getItem(TOKEN_KEYS.TOKEN_EXPIRY);
            if (!expiryTime) return true;
            const now = Date.now();
            const expiry = parseInt(expiryTime, 10);
            const buffer = API_CONFIG.ACCESS_TOKEN_EXPIRE_BUFFER;
            return now >= (expiry - buffer);
        },

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
     * Notify subscribers
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
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh_token: refreshToken })
            });

            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.detail || 'Token refresh failed');
            }

            const data = await response.json();
            TokenManager.setTokens(data.access_token, data.refresh_token, data.expires_in);
            
            if (data.user) {
                localStorage.setItem(TOKEN_KEYS.USER, JSON.stringify(data.user));
            }

            onTokenRefreshed(data.access_token);
            return data.access_token;
        } catch (error) {
            TokenManager.clearTokens();
            throw error;
        }
    }

    /**
     * Handle token refresh with queue
     */
    async function handleTokenRefresh() {
        if (isRefreshing) {
            return new Promise((resolve) => {
                subscribeTokenRefresh((token) => resolve(token));
            });
        }

        isRefreshing = true;
        try {
            return await refreshAccessToken();
        } finally {
            isRefreshing = false;
        }
    }

    /**
     * Error Handler
     */
    const ErrorHandler = {
        async parseError(response) {
            let errorData;
            try {
                errorData = await response.json();
            } catch {
                errorData = { detail: response.statusText || 'An error occurred' };
            }

            return {
                status: response.status,
                statusText: response.statusText,
                message: errorData.detail || errorData.message || 'An error occurred',
                errors: errorData.errors || errorData.detail || {},
                data: errorData
            };
        },

        handleError(error, response) {
            if (!response) {
                return {
                    message: 'Network error. Please check your connection.',
                    type: 'NETWORK_ERROR',
                    originalError: error
                };
            }

            const errorMap = {
                401: { message: 'Authentication required. Please login again.', type: 'UNAUTHORIZED' },
                403: { message: 'You do not have permission to perform this action.', type: 'FORBIDDEN' },
                404: { message: 'The requested resource was not found.', type: 'NOT_FOUND' },
                422: { message: 'Validation error. Please check your input.', type: 'VALIDATION_ERROR' },
                429: { message: 'Too many requests. Please try again later.', type: 'RATE_LIMIT' },
                500: { message: 'Server error. Please try again later.', type: 'SERVER_ERROR' }
            };

            const errorInfo = errorMap[response.status] || {
                message: `Error ${response.status}: ${response.statusText}`,
                type: 'HTTP_ERROR'
            };

            return { ...errorInfo, status: response.status };
        }
    };

    /**
     * Retry logic
     */
    async function retryRequest(requestFn, retries = API_CONFIG.RETRY_ATTEMPTS) {
        let lastError;
        for (let i = 0; i < retries; i++) {
            try {
                return await requestFn();
            } catch (error) {
                lastError = error;
                if (error.status === 401 || error.status === 403 || error.status === 404) {
                    throw error;
                }
                if (i < retries - 1) {
                    await new Promise(resolve => setTimeout(resolve, API_CONFIG.RETRY_DELAY * (i + 1)));
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

        const url = endpoint.startsWith('http') 
            ? endpoint 
            : `${API_CONFIG.BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;

        const requestHeaders = {
            'Content-Type': 'application/json',
            ...headers
        };

        if (requiresAuth && TokenManager.isAuthenticated()) {
            if (!skipTokenRefresh && TokenManager.isTokenExpired()) {
                try {
                    await handleTokenRefresh();
                } catch (error) {
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

        if (body instanceof FormData) {
            delete requestHeaders['Content-Type'];
        }

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

                if (response.status === 401 && requiresAuth && !skipTokenRefresh) {
                    try {
                        const newToken = await handleTokenRefresh();
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
                    const timeoutError = new Error('Request timeout. Please try again.');
                    timeoutError.type = 'TIMEOUT_ERROR';
                    throw timeoutError;
                }
                // Preserve original error for network issues
                if (!error.type) {
                    error.type = 'NETWORK_ERROR';
                }
                throw error;
            }
        };

        const response = await retryRequest(makeRequest);

        if (!response.ok) {
            let errorInfo;
            try {
                errorInfo = await ErrorHandler.parseError(response);
            } catch (parseError) {
                // If we can't parse the error, create a basic one
                errorInfo = {
                    status: response.status,
                    statusText: response.statusText,
                    message: `HTTP ${response.status}: ${response.statusText}`,
                    errors: {},
                    data: {}
                };
            }
            const error = ErrorHandler.handleError(errorInfo, response);
            error.response = response;
            error.errorInfo = errorInfo;
            error.status = response.status;
            throw error;
        }

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
        async get(endpoint, options = {}) {
            return apiRequest(endpoint, { ...options, method: 'GET' });
        },

        async post(endpoint, body, options = {}) {
            return apiRequest(endpoint, { ...options, method: 'POST', body });
        },

        async put(endpoint, body, options = {}) {
            return apiRequest(endpoint, { ...options, method: 'PUT', body });
        },

        async patch(endpoint, body, options = {}) {
            return apiRequest(endpoint, { ...options, method: 'PATCH', body });
        },

        async delete(endpoint, options = {}) {
            return apiRequest(endpoint, { ...options, method: 'DELETE' });
        },

        async upload(endpoint, formData, options = {}) {
            return apiRequest(endpoint, {
                ...options,
                method: 'POST',
                body: formData,
                headers: { ...options.headers }
            });
        },

        setBaseURL(url) {
            API_CONFIG.BASE_URL = url;
        },

        getBaseURL() {
            return API_CONFIG.BASE_URL;
        },

        tokenManager: TokenManager
    };

    // Make available globally
    window.api = api;
    window.TokenManager = TokenManager;
    window.ErrorHandler = ErrorHandler;

})();
