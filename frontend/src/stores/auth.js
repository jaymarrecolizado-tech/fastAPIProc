/**
 * Authentication Store
 * Manages authentication state and user session
 * Uses Vue 3 Composition API reactive system
 */

import { ref, reactive, computed } from 'vue';

// Import API client
import api, { TokenManager } from '../utils/api.js';

// Reactive state
const user = ref(null);
const isAuthenticated = ref(false);
const isLoading = ref(false);
const error = ref(null);

/**
 * Initialize auth state from localStorage
 */
function initAuth() {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
        try {
            user.value = JSON.parse(storedUser);
            isAuthenticated.value = TokenManager.isAuthenticated();
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
    isLoading.value = true;
    error.value = null;
    
    try {
        const response = await api.post('/auth/login', {
            email,
            password
        }, {
            requiresAuth: false
        });
        
        // Store tokens
        TokenManager.setTokens(
            response.access_token,
            response.refresh_token,
            response.expires_in
        );
        
        // Store user data
        user.value = response.user;
        localStorage.setItem('user', JSON.stringify(response.user));
        isAuthenticated.value = true;
        
        return {
            success: true,
            user: response.user
        };
    } catch (err) {
        error.value = err.message || 'Login failed. Please try again.';
        return {
            success: false,
            error: error.value
        };
    } finally {
        isLoading.value = false;
    }
}

/**
 * Logout function
 */
async function logout() {
    isLoading.value = true;
    error.value = null;
    
    try {
        // Call logout endpoint if authenticated
        if (isAuthenticated.value) {
            try {
                await api.post('/auth/logout', {}, {
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
        error.value = err.message || 'Logout failed';
        return {
            success: false,
            error: error.value
        };
    } finally {
        isLoading.value = false;
    }
}

/**
 * Clear authentication state
 */
function clearAuth() {
    TokenManager.clearTokens();
    user.value = null;
    isAuthenticated.value = false;
    error.value = null;
}

/**
 * Get current user info from API
 */
async function fetchCurrentUser() {
    isLoading.value = true;
    error.value = null;
    
    try {
        const userData = await api.get('/auth/me');
        user.value = userData;
        localStorage.setItem('user', JSON.stringify(userData));
        return userData;
    } catch (err) {
        error.value = err.message || 'Failed to fetch user data';
        // If unauthorized, clear auth
        if (err.status === 401) {
            clearAuth();
        }
        throw err;
    } finally {
        isLoading.value = false;
    }
}

/**
 * Change password
 */
async function changePassword(currentPassword, newPassword) {
    isLoading.value = true;
    error.value = null;
    
    try {
        await api.post('/auth/change-password', {
            current_password: currentPassword,
            new_password: newPassword
        });
        
        return { success: true };
    } catch (err) {
        error.value = err.message || 'Failed to change password';
        return {
            success: false,
            error: error.value
        };
    } finally {
        isLoading.value = false;
    }
}

/**
 * Check if user has specific role
 */
function hasRole(role) {
    return user.value?.role === role;
}

/**
 * Check if user has any of the specified roles
 */
function hasAnyRole(roles) {
    if (!user.value) return false;
    return roles.includes(user.value.role);
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

// Initialize auth on load
initAuth();

// Export auth store
export default {
    // State
    user: computed(() => user.value),
    isAuthenticated: computed(() => isAuthenticated.value),
    isLoading: computed(() => isLoading.value),
    error: computed(() => error.value),
    
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
    initAuth
};

// For Vue 3 Composition API usage
export function useAuth() {
    return {
        user: computed(() => user.value),
        isAuthenticated: computed(() => isAuthenticated.value),
        isLoading: computed(() => isLoading.value),
        error: computed(() => error.value),
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
        isEndUser
    };
}
