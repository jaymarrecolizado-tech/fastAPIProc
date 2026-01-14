/**
 * Utility Helper Functions
 * Common functions used across the application
 */

/**
 * Format number with commas (Philippine Peso format)
 */
export function formatNumber(num) {
    if (num === null || num === undefined) return '0';
    return Number(num).toLocaleString('en-PH');
}

/**
 * Format currency (Philippine Peso)
 */
export function formatCurrency(amount) {
    if (amount === null || amount === undefined) return '₱0.00';
    return `₱${formatNumber(Number(amount).toFixed(2))}`;
}

/**
 * Format date to readable string
 */
export function formatDate(date, options = {}) {
    if (!date) return '-';
    
    const defaultOptions = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        ...options
    };
    
    try {
        const dateObj = date instanceof Date ? date : new Date(date);
        return dateObj.toLocaleDateString('en-PH', defaultOptions);
    } catch (error) {
        return '-';
    }
}

/**
 * Format datetime to readable string
 */
export function formatDateTime(date) {
    if (!date) return '-';
    
    try {
        const dateObj = date instanceof Date ? date : new Date(date);
        return dateObj.toLocaleString('en-PH', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (error) {
        return '-';
    }
}

/**
 * Get relative time (e.g., "2 minutes ago")
 */
export function getRelativeTime(date) {
    if (!date) return '-';
    
    try {
        const dateObj = date instanceof Date ? date : new Date(date);
        const now = new Date();
        const diffMs = now - dateObj;
        const diffSecs = Math.floor(diffMs / 1000);
        const diffMins = Math.floor(diffSecs / 60);
        const diffHours = Math.floor(diffMins / 60);
        const diffDays = Math.floor(diffHours / 24);
        
        if (diffSecs < 60) {
            return 'Just now';
        } else if (diffMins < 60) {
            return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
        } else if (diffHours < 24) {
            return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
        } else if (diffDays < 7) {
            return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
        } else {
            return formatDate(date);
        }
    } catch (error) {
        return '-';
    }
}

/**
 * Debounce function
 */
export function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function
 */
export function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * Validate email format
 */
export function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validate phone number (Philippine format)
 */
export function isValidPhone(phone) {
    const phoneRegex = /^(\+63|0)?[9]\d{9}$/;
    return phoneRegex.test(phone.replace(/[\s-]/g, ''));
}

/**
 * Truncate text with ellipsis
 */
export function truncate(text, maxLength = 50) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

/**
 * Capitalize first letter
 */
export function capitalize(text) {
    if (!text) return '';
    return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
}

/**
 * Convert to title case
 */
export function toTitleCase(text) {
    if (!text) return '';
    return text.replace(/\w\S*/g, (txt) => 
        txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
    );
}

/**
 * Generate PR number format (PR-YYYY-####)
 */
export function generatePRNumber() {
    const year = new Date().getFullYear();
    const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0');
    return `PR-${year}-${random}`;
}

/**
 * Get status badge class based on status
 */
export function getStatusBadgeClass(status) {
    const statusMap = {
        // Purchase Request Statuses
        'PR_UNDER_REVIEW': 'badge-info',
        'RFQ_READY': 'badge-info',
        'RFQ_DISSEMINATED': 'badge-info',
        'CANVASS_COMPLETE': 'badge-success',
        'BAC_DOCS_READY': 'badge-info',
        'BAC_APPROVED': 'badge-success',
        'PO_APPROVED': 'badge-success',
        'AWAITING_CONFORME': 'badge-warning',
        'PO_COMPLETE': 'badge-success',
        'COA_STAMPED': 'badge-success',
        'CANCELLED': 'badge-danger',
        
        // General Statuses
        'PENDING': 'badge-warning',
        'APPROVED': 'badge-success',
        'REJECTED': 'badge-danger',
        'COMPLETED': 'badge-success',
        'IN_PROGRESS': 'badge-info',
        'ACTIVE': 'badge-success',
        'INACTIVE': 'badge-danger',
        
        // Urgency Levels
        'LOW': 'badge-info',
        'MEDIUM': 'badge-warning',
        'HIGH': 'badge-danger',
        'URGENT': 'badge-danger'
    };
    
    return statusMap[status] || 'badge-info';
}

/**
 * Get readable status text
 */
export function getStatusText(status) {
    const statusMap = {
        'PR_UNDER_REVIEW': 'Under Review',
        'RFQ_READY': 'RFQ Ready',
        'RFQ_DISSEMINATED': 'RFQ Disseminated',
        'CANVASS_COMPLETE': 'Canvass Complete',
        'BAC_DOCS_READY': 'BAC Docs Ready',
        'BAC_APPROVED': 'BAC Approved',
        'PO_APPROVED': 'PO Approved',
        'AWAITING_CONFORME': 'Awaiting Conforme',
        'PO_COMPLETE': 'PO Complete',
        'COA_STAMPED': 'COA Stamped',
        'CANCELLED': 'Cancelled',
        'PENDING': 'Pending',
        'APPROVED': 'Approved',
        'REJECTED': 'Rejected',
        'COMPLETED': 'Completed',
        'IN_PROGRESS': 'In Progress',
        'ACTIVE': 'Active',
        'INACTIVE': 'Inactive'
    };
    
    return statusMap[status] || status;
}

/**
 * Format file size
 */
export function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Validate file type
 */
export function isValidFileType(file, allowedTypes) {
    if (!file || !allowedTypes) return true;
    return allowedTypes.some(type => file.type.includes(type));
}

/**
 * Validate file size
 */
export function isValidFileSize(file, maxSizeMB) {
    if (!file || !maxSizeMB) return true;
    const maxSizeBytes = maxSizeMB * 1024 * 1024;
    return file.size <= maxSizeBytes;
}

/**
 * Download file from blob
 */
export function downloadBlob(blob, filename) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

/**
 * Copy to clipboard
 */
export async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (error) {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            document.body.removeChild(textArea);
            return true;
        } catch (err) {
            document.body.removeChild(textArea);
            return false;
        }
    }
}

/**
 * Show toast notification (simple implementation)
 */
export function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 animate-fade-in-up`;
    
    const colors = {
        success: 'bg-green-500 text-white',
        error: 'bg-red-500 text-white',
        warning: 'bg-yellow-500 text-white',
        info: 'bg-blue-500 text-white'
    };
    
    toast.className += ` ${colors[type] || colors.info}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

/**
 * Confirm dialog
 */
export function confirmDialog(message) {
    return window.confirm(message);
}

/**
 * Get query parameter from URL
 */
export function getQueryParam(name) {
    const params = new URLSearchParams(window.location.search);
    return params.get(name);
}

/**
 * Set query parameter in URL
 */
export function setQueryParam(name, value) {
    const url = new URL(window.location);
    url.searchParams.set(name, value);
    window.history.pushState({}, '', url);
}

/**
 * Remove query parameter from URL
 */
export function removeQueryParam(name) {
    const url = new URL(window.location);
    url.searchParams.delete(name);
    window.history.pushState({}, '', url);
}
