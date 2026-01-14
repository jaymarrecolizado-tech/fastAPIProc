/**
 * Dashboard Service
 * Handles dashboard data fetching and processing
 * Currently uses mock data, will switch to API when endpoints are ready
 */

(function() {
    'use strict';

    /**
     * Fetch dashboard statistics
     * TODO: Replace with real API call when endpoint is available
     * Expected endpoint: GET /api/v1/dashboard/stats
     */
    async function fetchDashboardStats() {
        // For now, return mock data
        // When API is ready, replace with:
        // return await window.api.get('/dashboard/stats');
        
        return {
            totalPRs: 1247,
            approved: 856,
            pending: 234,
            rejected: 45,
            inProgress: 112,
            budgetUtilized: 15700000,
            budgetAllocated: 20000000,
            budgetUtilizationPercent: 78.5,
            totalSuppliers: 156,
            activeRFQs: 23,
            completedPOs: 342
        };
    }

    /**
     * Fetch recent activities
     * TODO: Replace with real API call when endpoint is available
     * Expected endpoint: GET /api/v1/activity-logs?limit=10
     */
    async function fetchRecentActivities(limit = 10) {
        // For now, return mock data
        // When API is ready, replace with:
        // return await window.api.get(`/activity-logs?limit=${limit}`);
        
        const mockActivities = [
            {
                id: 1,
                action: 'APPROVED',
                entity_type: 'PurchaseRequest',
                entity_id: 156,
                description: 'PR-2025-0156 Approved',
                details: 'Office supplies request from IT Department',
                user_name: 'Maria Santos',
                user_role: 'PROCUREMENT_OFFICER',
                created_at: new Date(Date.now() - 2 * 60 * 1000).toISOString(),
                status: 'Approved',
                icon: 'ph ph-check text-white',
                colorClass: 'gradient-success',
                badgeClass: 'badge-success'
            },
            {
                id: 2,
                action: 'CREATE',
                entity_type: 'PurchaseRequest',
                entity_id: 157,
                description: 'New PR Created',
                details: 'Computer equipment request from HR Department',
                user_name: 'Carlos Reyes',
                user_role: 'END_USER',
                created_at: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
                status: 'Pending',
                icon: 'ph ph-plus text-white',
                colorClass: 'gradient-primary',
                badgeClass: 'badge-warning'
            },
            {
                id: 3,
                action: 'REJECTED',
                entity_type: 'PurchaseRequest',
                entity_id: 154,
                description: 'PR-2025-0154 Rejected',
                details: 'Furniture request exceeded budget allocation',
                user_name: 'Ana Cruz',
                user_role: 'PROCUREMENT_OFFICER',
                created_at: new Date(Date.now() - 60 * 60 * 1000).toISOString(),
                status: 'Rejected',
                icon: 'ph ph-x text-white',
                colorClass: 'gradient-danger',
                badgeClass: 'badge-danger'
            },
            {
                id: 4,
                action: 'CREATE',
                entity_type: 'Supplier',
                entity_id: 45,
                description: 'Supplier Accredited',
                details: 'Tech Solutions Inc. added to supplier list',
                user_name: 'Juan Dela Cruz',
                user_role: 'PROCUREMENT_OFFICER',
                created_at: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
                status: 'Completed',
                icon: 'ph ph-storefront text-white',
                colorClass: 'gradient-info',
                badgeClass: 'badge-info'
            }
        ];

        return mockActivities.slice(0, limit);
    }

    /**
     * Fetch pending approvals for current user
     * TODO: Replace with real API call when endpoint is available
     * Expected endpoint: GET /api/v1/approvals/pending
     */
    async function fetchPendingApprovals(limit = 10) {
        // For now, return mock data
        // When API is ready, replace with:
        // return await window.api.get('/approvals/pending');
        
        const mockPRs = [
            {
                id: 1,
                pr_number: 'PR-2025-0158',
                project_title: 'IT Equipment',
                requester: 'Maria Santos',
                department: 'IT',
                amount: 450000,
                date: 'Jan 14, 2025',
                status: 'PR_UNDER_REVIEW',
                badgeClass: 'badge-warning',
                created_at: new Date().toISOString()
            },
            {
                id: 2,
                pr_number: 'PR-2025-0157',
                project_title: 'Office Supplies',
                requester: 'Carlos Reyes',
                department: 'HR',
                amount: 125000,
                date: 'Jan 14, 2025',
                status: 'PR_UNDER_REVIEW',
                badgeClass: 'badge-warning',
                created_at: new Date().toISOString()
            },
            {
                id: 3,
                pr_number: 'PR-2025-0156',
                project_title: 'Furniture',
                requester: 'Ana Cruz',
                department: 'Finance',
                amount: 78000,
                date: 'Jan 13, 2025',
                status: 'BAC_APPROVED',
                badgeClass: 'badge-success',
                created_at: new Date().toISOString()
            },
            {
                id: 4,
                pr_number: 'PR-2025-0155',
                project_title: 'Office Equipment',
                requester: 'Jose Garcia',
                department: 'Operations',
                amount: 320000,
                date: 'Jan 13, 2025',
                status: 'RFQ_READY',
                badgeClass: 'badge-info',
                created_at: new Date().toISOString()
            }
        ];

        return mockPRs.slice(0, limit);
    }

    /**
     * Fetch procurement trends data for charts
     * TODO: Replace with real API call when endpoint is available
     * Expected endpoint: GET /api/v1/dashboard/trends?period=6months
     */
    async function fetchProcurementTrends(period = '6months') {
        // For now, return mock data
        // When API is ready, replace with:
        // return await window.api.get(`/dashboard/trends?period=${period}`);
        
        const periods = {
            '6months': {
                labels: ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan'],
                procurementValue: [12.5, 15.2, 18.7, 22.1, 19.8, 24.5],
                budgetAllocated: [15, 18, 20, 22, 25, 28]
            },
            'year': {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                procurementValue: [10, 12, 15, 18, 20, 22, 19, 12.5, 15.2, 18.7, 22.1, 24.5],
                budgetAllocated: [12, 14, 16, 18, 20, 22, 25, 15, 18, 20, 22, 28]
            }
        };

        return periods[period] || periods['6months'];
    }

    /**
     * Fetch budget by department data
     * TODO: Replace with real API call when endpoint is available
     * Expected endpoint: GET /api/v1/dashboard/budget-by-department
     */
    async function fetchBudgetByDepartment() {
        // For now, return mock data
        // When API is ready, replace with:
        // return await window.api.get('/dashboard/budget-by-department');
        
        return {
            labels: ['IT', 'HR', 'Finance', 'Operations', 'Admin'],
            data: [4.5, 3.2, 5.8, 2.9, 4.1]
        };
    }

    /**
     * Fetch PR status distribution
     * TODO: Replace with real API call when endpoint is available
     * Expected endpoint: GET /api/v1/dashboard/pr-status-distribution
     */
    async function fetchPRStatusDistribution() {
        // For now, return mock data
        // When API is ready, replace with:
        // return await window.api.get('/dashboard/pr-status-distribution');
        
        return {
            labels: ['Approved', 'Pending', 'Rejected', 'In Progress'],
            data: [45, 30, 10, 15],
            colors: ['#10b981', '#f59e0b', '#ef4444', '#3b82f6']
        };
    }

    /**
     * Format activity for display
     */
    function formatActivity(activity) {
        const timeAgo = getRelativeTime(activity.created_at);
        return {
            ...activity,
            time: timeAgo,
            title: activity.description,
            description: activity.details
        };
    }

    /**
     * Get relative time string
     */
    function getRelativeTime(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
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
            return date.toLocaleDateString('en-PH', {
                month: 'short',
                day: 'numeric',
                year: 'numeric'
            });
        }
    }

    /**
     * Format PR status for display
     */
    function formatPRStatus(status) {
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
            'CANCELLED': 'Cancelled'
        };
        return statusMap[status] || status;
    }

    /**
     * Get status badge class
     */
    function getStatusBadgeClass(status) {
        const statusMap = {
            'PR_UNDER_REVIEW': 'badge-warning',
            'RFQ_READY': 'badge-info',
            'RFQ_DISSEMINATED': 'badge-info',
            'CANVASS_COMPLETE': 'badge-success',
            'BAC_DOCS_READY': 'badge-info',
            'BAC_APPROVED': 'badge-success',
            'PO_APPROVED': 'badge-success',
            'AWAITING_CONFORME': 'badge-warning',
            'PO_COMPLETE': 'badge-success',
            'COA_STAMPED': 'badge-success',
            'CANCELLED': 'badge-danger'
        };
        return statusMap[status] || 'badge-info';
    }

    // Export dashboard service
    window.dashboardService = {
        fetchDashboardStats,
        fetchRecentActivities,
        fetchPendingApprovals,
        fetchProcurementTrends,
        fetchBudgetByDepartment,
        fetchPRStatusDistribution,
        formatActivity,
        formatPRStatus,
        getStatusBadgeClass,
        getRelativeTime
    };

})();
