/**
 * Application Configuration
 * Centralized configuration for the frontend application
 */

const config = {
    // API Configuration
    API: {
        BASE_URL: 'http://127.0.0.1:8000/api/v1',
        TIMEOUT: 30000,
        RETRY_ATTEMPTS: 3
    },
    
    // Application Info
    APP: {
        NAME: 'DICT Procurement Management System',
        VERSION: '2.0.0',
        ENVIRONMENT: 'development'
    },
    
    // Pagination
    PAGINATION: {
        DEFAULT_PAGE_SIZE: 20,
        PAGE_SIZE_OPTIONS: [10, 20, 50, 100]
    },
    
    // File Upload
    UPLOAD: {
        MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
        ALLOWED_IMAGE_TYPES: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
        ALLOWED_DOCUMENT_TYPES: [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ]
    },
    
    // Date Formats
    DATE_FORMAT: {
        DISPLAY: 'MMM DD, YYYY',
        DISPLAY_WITH_TIME: 'MMM DD, YYYY HH:mm',
        API: 'YYYY-MM-DD'
    },
    
    // Routes
    ROUTES: {
        LOGIN: '/login.html',
        DASHBOARD: '/dashboard.html',
        PURCHASE_REQUESTS: '/purchase-requests.html',
        CREATE_PR: '/create-pr.html',
        USERS: '/users.html',
        SUPPLIERS: '/suppliers.html',
        REPORTS: '/reports.html'
    }
};

// Environment-specific overrides
if (typeof window !== 'undefined') {
    // Check for environment variables or config overrides
    const envConfig = window.APP_CONFIG || {};
    
    if (envConfig.API_BASE_URL) {
        config.API.BASE_URL = envConfig.API_BASE_URL;
    }
    
    if (envConfig.ENVIRONMENT) {
        config.APP.ENVIRONMENT = envConfig.ENVIRONMENT;
    }
}

export default config;
