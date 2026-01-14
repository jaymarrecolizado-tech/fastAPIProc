/**
 * Utility Loader
 * Loads all utility modules and makes them available globally
 * This file should be included in HTML pages before Vue scripts
 */

// Load API client
import api, { TokenManager, ErrorHandler } from './api.js';

// Load helpers
import * as helpers from './helpers.js';

// Load config
import config from './config.js';

// Load auth store
import authStore, { useAuth } from '../stores/auth.js';

// Make available globally
if (typeof window !== 'undefined') {
    window.api = api;
    window.TokenManager = TokenManager;
    window.ErrorHandler = ErrorHandler;
    window.helpers = helpers;
    window.config = config;
    window.authStore = authStore;
    window.useAuth = useAuth;
}

// Export for ES modules
export { api, TokenManager, ErrorHandler, helpers, config, authStore, useAuth };
