/**
 * Authentication Guard
 * Protects routes and checks authentication status
 */

(function() {
    'use strict';

    /**
     * Check if user is authenticated
     */
    function requireAuth() {
        if (!window.TokenManager || !window.TokenManager.isAuthenticated()) {
            return false;
        }
        return true;
    }

    /**
     * Check if user has required role
     */
    function requireRole(role) {
        if (!requireAuth()) {
            return false;
        }
        
        const user = window.authStore?.getCurrentUser();
        if (!user) {
            return false;
        }
        
        return user.role === role;
    }

    /**
     * Check if user has any of the required roles
     */
    function requireAnyRole(roles) {
        if (!requireAuth()) {
            return false;
        }
        
        const user = window.authStore?.getCurrentUser();
        if (!user) {
            return false;
        }
        
        return roles.includes(user.role);
    }

    /**
     * Protect a route - redirect to login if not authenticated
     */
    function protectRoute() {
        if (!requireAuth()) {
            // Store intended destination
            const currentPath = window.location.pathname;
            sessionStorage.setItem('redirect_after_login', currentPath);
            
            // Redirect to login
            window.location.href = '/login.html';
            return false;
        }
        return true;
    }

    /**
     * Protect route with role requirement
     */
    function protectRouteWithRole(role) {
        if (!protectRoute()) {
            return false;
        }
        
        if (!requireRole(role)) {
            // User doesn't have required role
            alert('You do not have permission to access this page.');
            window.location.href = '/dashboard.html';
            return false;
        }
        
        return true;
    }

    /**
     * Protect route with any of the roles
     */
    function protectRouteWithAnyRole(roles) {
        if (!protectRoute()) {
            return false;
        }
        
        if (!requireAnyRole(roles)) {
            // User doesn't have any of the required roles
            alert('You do not have permission to access this page.');
            window.location.href = '/dashboard.html';
            return false;
        }
        
        return true;
    }

    /**
     * Initialize auth guard on page load
     * Call this in onMounted or at the end of script
     */
    function initAuthGuard(options = {}) {
        const {
            requireAuth: needsAuth = true,
            requiredRole = null,
            requiredRoles = null,
            redirectTo = '/login.html'
        } = options;

        // Wait for API client and auth store to load
        if (!window.api || !window.TokenManager || !window.authStore) {
            console.error('API client or auth store not loaded. Make sure to include api.js and auth-store.js before auth-guard.js');
            return false;
        }

        // Check authentication
        if (needsAuth && !requireAuth()) {
            sessionStorage.setItem('redirect_after_login', window.location.pathname);
            window.location.href = redirectTo;
            return false;
        }

        // Check role requirements
        if (requiredRole && !requireRole(requiredRole)) {
            alert('You do not have permission to access this page.');
            window.location.href = '/dashboard.html';
            return false;
        }

        if (requiredRoles && !requireAnyRole(requiredRoles)) {
            alert('You do not have permission to access this page.');
            window.location.href = '/dashboard.html';
            return false;
        }

        // Fetch current user if authenticated but user data not loaded
        if (needsAuth && window.TokenManager.isAuthenticated() && !window.authStore.getCurrentUser()) {
            window.authStore.fetchCurrentUser().catch(err => {
                console.error('Failed to fetch user:', err);
                window.authStore.clearAuth();
                window.location.href = redirectTo;
            });
        }

        return true;
    }

    /**
     * Get redirect URL after login
     */
    function getRedirectAfterLogin() {
        const redirect = sessionStorage.getItem('redirect_after_login');
        sessionStorage.removeItem('redirect_after_login');
        return redirect || '/dashboard.html';
    }

    // Export auth guard
    window.authGuard = {
        requireAuth,
        requireRole,
        requireAnyRole,
        protectRoute,
        protectRouteWithRole,
        protectRouteWithAnyRole,
        initAuthGuard,
        getRedirectAfterLogin
    };

})();
