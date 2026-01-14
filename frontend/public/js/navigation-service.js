/**
 * Navigation Service
 * Handles navigation, menu visibility, and breadcrumbs
 */

(function() {
    'use strict';

    /**
     * Menu configuration with role-based visibility
     */
    const menuItems = [
        {
            id: 'dashboard',
            label: 'Dashboard',
            icon: 'ph ph-squares-four',
            path: '/dashboard.html',
            roles: ['ADMIN', 'PROCUREMENT_OFFICER', 'BAC_CHAIR', 'BAC_MEMBER', 'BAC_SECRETARIAT', 'END_USER', 'CANVASSER']
        },
        {
            id: 'purchase-requests',
            label: 'Purchase Requests',
            icon: 'ph ph-file-text',
            path: '/purchase-requests.html',
            roles: ['ADMIN', 'PROCUREMENT_OFFICER', 'BAC_CHAIR', 'BAC_MEMBER', 'BAC_SECRETARIAT', 'END_USER']
        },
        {
            id: 'create-pr',
            label: 'Create PR',
            icon: 'ph ph-plus-circle',
            path: '/create-pr.html',
            roles: ['ADMIN', 'PROCUREMENT_OFFICER', 'END_USER']
        },
        {
            id: 'rfqs',
            label: 'RFQs',
            icon: 'ph ph-quotes',
            path: '/rfq-list.html',
            roles: ['ADMIN', 'PROCUREMENT_OFFICER', 'BAC_CHAIR', 'BAC_MEMBER', 'BAC_SECRETARIAT']
        },
        {
            id: 'purchase-orders',
            label: 'Purchase Orders',
            icon: 'ph ph-shopping-bag',
            path: '/purchase-orders.html',
            roles: ['ADMIN', 'PROCUREMENT_OFFICER', 'BAC_CHAIR', 'BAC_MEMBER']
        },
        {
            id: 'suppliers',
            label: 'Suppliers',
            icon: 'ph ph-storefront',
            path: '/suppliers.html',
            roles: ['ADMIN', 'PROCUREMENT_OFFICER', 'BAC_CHAIR', 'BAC_MEMBER', 'BAC_SECRETARIAT']
        },
        {
            id: 'bac-documents',
            label: 'BAC Documents',
            icon: 'ph ph-gavel',
            path: '/bac-documents.html',
            roles: ['ADMIN', 'BAC_CHAIR', 'BAC_MEMBER', 'BAC_SECRETARIAT']
        },
        {
            id: 'documents',
            label: 'Documents',
            icon: 'ph ph-files',
            path: '/documents.html',
            roles: ['ADMIN', 'PROCUREMENT_OFFICER', 'BAC_CHAIR', 'BAC_MEMBER', 'BAC_SECRETARIAT', 'END_USER']
        },
        {
            id: 'reports',
            label: 'Reports',
            icon: 'ph ph-chart-bar',
            path: '/reports.html',
            roles: ['ADMIN', 'PROCUREMENT_OFFICER', 'BAC_CHAIR']
        },
        {
            id: 'users',
            label: 'User Management',
            icon: 'ph ph-user-gear',
            path: '/users.html',
            roles: ['ADMIN']
        },
        {
            id: 'audit-trail',
            label: 'Audit Trail',
            icon: 'ph ph-scroll',
            path: '/audit-trail.html',
            roles: ['ADMIN', 'PROCUREMENT_OFFICER', 'BAC_CHAIR']
        }
    ];

    /**
     * Get current page path
     */
    function getCurrentPath() {
        return window.location.pathname;
    }

    /**
     * Get current page ID from path
     */
    function getCurrentPageId() {
        const path = getCurrentPath();
        const item = menuItems.find(item => path.includes(item.path.replace('/', '')));
        return item ? item.id : null;
    }

    /**
     * Check if user has access to menu item
     */
    function hasAccess(menuItem, userRole) {
        if (!menuItem.roles || menuItem.roles.length === 0) {
            return true; // Public access
        }
        if (!userRole) {
            return false;
        }
        return menuItem.roles.includes(userRole);
    }

    /**
     * Get visible menu items for current user
     */
    function getVisibleMenuItems(userRole) {
        if (!userRole) {
            return [];
        }
        return menuItems.filter(item => hasAccess(item, userRole));
    }

    /**
     * Check if menu item is active
     */
    function isActive(menuItem) {
        const currentPath = getCurrentPath();
        return currentPath.includes(menuItem.path.replace('/', ''));
    }

    /**
     * Generate breadcrumbs for current page
     */
    function getBreadcrumbs() {
        const path = getCurrentPath();
        const breadcrumbs = [
            { label: 'Home', path: '/dashboard.html', icon: 'ph ph-house' }
        ];

        // Find current page
        const currentItem = menuItems.find(item => path.includes(item.path.replace('/', '')));
        
        if (currentItem) {
            breadcrumbs.push({
                label: currentItem.label,
                path: currentItem.path,
                icon: currentItem.icon,
                current: true
            });
        } else {
            // Handle special pages
            const pageName = path.split('/').pop().replace('.html', '').replace('-', ' ');
            breadcrumbs.push({
                label: pageName.charAt(0).toUpperCase() + pageName.slice(1),
                path: path,
                current: true
            });
        }

        return breadcrumbs;
    }

    /**
     * Navigate to a page
     */
    function navigateTo(path) {
        window.location.href = path;
    }

    /**
     * Get menu item by ID
     */
    function getMenuItem(id) {
        return menuItems.find(item => item.id === id);
    }

    /**
     * Get page title from path
     */
    function getPageTitle() {
        const path = getCurrentPath();
        const item = menuItems.find(item => path.includes(item.path.replace('/', '')));
        if (item) {
            return item.label;
        }
        
        // Fallback: extract from filename
        const filename = path.split('/').pop().replace('.html', '');
        return filename.split('-').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    }

    // Export navigation service
    window.navigationService = {
        menuItems,
        getCurrentPath,
        getCurrentPageId,
        hasAccess,
        getVisibleMenuItems,
        isActive,
        getBreadcrumbs,
        navigateTo,
        getMenuItem,
        getPageTitle
    };

})();
