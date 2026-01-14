/**
 * Authentication Store - Browser Compatible Version
 * Manages authentication state and user session
 */

(function() {
    'use strict';

    // State
    let user = null;
    let isAuthenticated = false;
    let isLoading = false;
    let error = null;

    // Initialize auth state from localStorage
    function initAuth() {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            try {
                user = JSON.parse(storedUser);
                isAuthenticated = window.TokenManager && window.TokenManager.isAuthenticated();
            } catch (e) {
                console.error('Failed to parse user data:', e);
                clearAuth();
            }
        }
    }

    /**
     * Login function
     */
    async function login(email, password) {
        isLoading = true;
        error = null;
        
        try {
            const response = await window.api.post('/auth/login', {
                email,
                password
            }, {
                requiresAuth: false
            });
            
            // Store tokens
            window.TokenManager.setTokens(
                response.access_token,
                response.refresh_token,
                response.expires_in
            );
            
            // Store user data
            user = response.user;
            localStorage.setItem('user', JSON.stringify(response.user));
            isAuthenticated = true;
            
            return {
                success: true,
                user: response.user
            };
        } catch (err) {
            error = err.message || 'Login failed. Please try again.';
            return {
                success: false,
                error: error
            };
        } finally {
            isLoading = false;
        }
    }

    /**
     * Logout function
     */
    async function logout() {
        isLoading = true;
        error = null;
        
        try {
            // Call logout endpoint if authenticated
            if (isAuthenticated) {
                try {
                    await window.api.post('/auth/logout', {}, {
                        requiresAuth: true
                    });
                } catch (err) {
                    // Continue with logout even if API call fails
                    console.warn('Logout API call failed:', err);
                }
            }
            
            // Clear local state
            clearAuth();
            
            return { success: true };
        } catch (err) {
            error = err.message || 'Logout failed';
            return {
                success: false,
                error: error
            };
        } finally {
            isLoading = false;
        }
    }

    /**
     * Clear authentication state
     */
    function clearAuth() {
        if (window.TokenManager) {
            window.TokenManager.clearTokens();
        }
        user = null;
        isAuthenticated = false;
        error = null;
        localStorage.removeItem('user');
    }

    /**
     * Get current user info from API
     */
    async function fetchCurrentUser() {
        isLoading = true;
        error = null;
        
        try {
            const userData = await window.api.get('/auth/me');
            user = userData;
            localStorage.setItem('user', JSON.stringify(userData));
            isAuthenticated = true;
            return userData;
        } catch (err) {
            error = err.message || 'Failed to fetch user data';
            // If unauthorized, clear auth
            if (err.status === 401) {
                clearAuth();
            }
            throw err;
        } finally {
            isLoading = false;
        }
    }

    /**
     * Change password
     */
    async function changePassword(currentPassword, newPassword) {
        isLoading = true;
        error = null;
        
        try {
            await window.api.post('/auth/change-password', {
                current_password: currentPassword,
                new_password: newPassword
            });
            
            return { success: true };
        } catch (err) {
            error = err.message || 'Failed to change password';
            return {
                success: false,
                error: error
            };
        } finally {
            isLoading = false;
        }
    }

    /**
     * Check if user has specific role
     */
    function hasRole(role) {
        return user?.role === role;
    }

    /**
     * Check if user has any of the specified roles
     */
    function hasAnyRole(roles) {
        if (!user) return false;
        return roles.includes(user.role);
    }

    /**
     * Check if user is admin
     */
    function isAdmin() {
        return hasRole('ADMIN');
    }

    /**
     * Check if user is procurement officer
     */
    function isProcurementOfficer() {
        return hasRole('PROCUREMENT_OFFICER');
    }

    /**
     * Check if user is BAC member
     */
    function isBACMember() {
        return hasAnyRole(['BAC_CHAIR', 'BAC_MEMBER']);
    }

    /**
     * Check if user is end user
     */
    function isEndUser() {
        return hasRole('END_USER');
    }

    /**
     * Get current user
     */
    function getCurrentUser() {
        return user;
    }

    /**
     * Get auth state
     */
    function getAuthState() {
        return {
            user: user,
            isAuthenticated: isAuthenticated,
            isLoading: isLoading,
            error: error
        };
    }

    // Initialize on load
    initAuth();

    // Export auth store
    window.authStore = {
        // State getters
        get user() { return user; },
        get isAuthenticated() { return isAuthenticated; },
        get isLoading() { return isLoading; },
        get error() { return error; },
        
        // Methods
        login,
        logout,
        clearAuth,
        fetchCurrentUser,
        changePassword,
        hasRole,
        hasAnyRole,
        isAdmin,
        isProcurementOfficer,
        isBACMember,
        isEndUser,
        getCurrentUser,
        getAuthState,
        initAuth
    };

})();
