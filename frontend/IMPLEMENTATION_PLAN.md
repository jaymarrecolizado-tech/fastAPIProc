# Frontend Logic Implementation Plan

## Overview
The UI pages are complete (18 HTML files). This document outlines the phased implementation of frontend logic to connect the UI with the backend API.

---

## **PHASE 1: Core Infrastructure & Authentication** 🔐
**Priority: CRITICAL | Estimated Time: 2-3 days**

### 1.1 API Client Setup
- [ ] Create centralized API client (`src/utils/api.js`)
  - Base URL configuration
  - Request/response interceptors
  - Token management (access/refresh)
  - Error handling middleware
  - Request retry logic

### 1.2 Authentication State Management
- [ ] Create auth store (`src/stores/auth.js`)
  - User state management
  - Token storage (localStorage/sessionStorage)
  - Auto token refresh logic
  - Logout functionality
  - Session persistence

### 1.3 Auth Service Integration
- [ ] Complete login page logic (`login.html`)
  - API integration (already partially done)
  - Error handling improvements
  - Token storage
  - Redirect after login
- [ ] Logout functionality
  - Clear tokens
  - Clear user data
  - Redirect to login
- [ ] Token refresh mechanism
  - Auto-refresh before expiry
  - Handle refresh failures
- [ ] Protected route guard
  - Check authentication on page load
  - Redirect to login if not authenticated

### 1.4 User Profile Management
- [ ] Profile page (`profile.html`)
  - Fetch current user data
  - Update profile information
  - Change password functionality
  - Display user role and permissions

---

## **PHASE 2: Dashboard & Navigation** 📊
**Priority: HIGH | Estimated Time: 2-3 days**

### 2.1 Dashboard Data Integration
- [ ] Dashboard statistics (`dashboard.html`)
  - Fetch real-time stats (total PRs, approved, pending, budget)
  - API endpoint: `/api/v1/dashboard/stats`
  - Real-time data updates
  - Loading states

### 2.2 Dashboard Charts
- [ ] Procurement trends chart
  - Fetch historical data
  - Update Chart.js with real data
- [ ] Budget by department chart
  - Fetch department-wise budget data
- [ ] PR status distribution chart
  - Fetch status breakdown

### 2.3 Recent Activity Feed
- [ ] Activity log integration
  - Fetch recent activities
  - Real-time updates (polling or WebSocket)
  - Filter by activity type

### 2.4 Pending Approvals Widget
- [ ] Fetch pending PRs for current user
  - Filter by user role
  - Display actionable items
  - Quick approve/reject actions

### 2.5 Navigation & Sidebar
- [ ] Role-based menu visibility
  - Show/hide menu items based on user role
  - Active route highlighting
  - Breadcrumb navigation

---

## **PHASE 3: Purchase Request Management** 📝
**Priority: CRITICAL | Estimated Time: 4-5 days**

### 3.1 Create Purchase Request
- [ ] Create PR form (`create-pr.html`)
  - Multi-step form validation
  - Dynamic item addition/removal
  - File upload for documents
  - Budget validation
  - Submit to API: `POST /api/v1/purchase-requests`
  - Success/error handling
  - Form reset after submission

### 3.2 Purchase Request List
- [ ] PR list page (`purchase-requests.html`)
  - Fetch paginated PR list: `GET /api/v1/purchase-requests`
  - Filtering (status, department, date range)
  - Sorting (date, amount, status)
  - Search functionality
  - Pagination controls
  - Export to CSV/PDF

### 3.3 Purchase Request Detail
- [ ] PR detail page (`pr-detail.html`)
  - Fetch PR details: `GET /api/v1/purchase-requests/{id}`
  - Display all PR information
  - Show PR items
  - Display approval workflow
  - Show activity timeline
  - Document viewer/download
  - Status update actions (if permitted)

### 3.4 PR Item Management
- [ ] Add/edit/delete PR items
  - Inline editing
  - Quantity/price calculations
  - Total amount recalculation
  - Validation

### 3.5 PR Status Workflow
- [ ] Status transitions
  - Submit for review
  - Approve/reject actions
  - Status change notifications
  - Workflow visualization

---

## **PHASE 4: User Management** 👥
**Priority: HIGH | Estimated Time: 2-3 days**

### 4.1 User List
- [ ] Users page (`users.html`)
  - Fetch user list: `GET /api/v1/users`
  - Role-based filtering
  - Department filtering
  - Active/inactive status filter
  - Search users
  - Pagination

### 4.2 Create User
- [ ] Create user form (`create-user.html`)
  - Form validation
  - Role selection
  - Department assignment
  - Email uniqueness check
  - Submit: `POST /api/v1/users`
  - Success/error handling

### 4.3 Edit User
- [ ] Edit user functionality
  - Pre-populate form
  - Update user: `PUT /api/v1/users/{id}`
  - Deactivate/activate user
  - Reset password functionality

### 4.4 User Permissions
- [ ] Role-based access control
  - Check permissions before actions
  - Disable UI elements based on role
  - Show appropriate error messages

---

## **PHASE 5: Supplier Management** 🏪
**Priority: HIGH | Estimated Time: 3-4 days**

### 5.1 Supplier List
- [ ] Suppliers page (`suppliers.html`)
  - Fetch supplier list: `GET /api/v1/suppliers`
  - Filter by accreditation status
  - Search suppliers
  - Sort by name, status, rating
  - Pagination

### 5.2 Supplier Detail
- [ ] Supplier detail view
  - Fetch supplier info: `GET /api/v1/suppliers/{id}`
  - Display supplier information
  - Show quotation history
  - Performance metrics
  - Accreditation documents

### 5.3 Supplier CRUD
- [ ] Create supplier
  - Form validation
  - Submit: `POST /api/v1/suppliers`
- [ ] Edit supplier
  - Update: `PUT /api/v1/suppliers/{id}`
- [ ] Delete supplier (soft delete)
  - `DELETE /api/v1/suppliers/{id}`

### 5.4 Supplier Accreditation
- [ ] Accreditation status management
  - Update accreditation status
  - Upload accreditation documents
  - Accreditation expiry tracking

---

## **PHASE 6: RFQ & Canvassing** 📋
**Priority: HIGH | Estimated Time: 4-5 days**

### 6.1 RFQ List
- [ ] RFQ list page (`rfq-list.html`)
  - Fetch RFQs: `GET /api/v1/rfqs`
  - Filter by status, PR number
  - Search functionality
  - Status badges
  - Pagination

### 6.2 RFQ Detail
- [ ] RFQ detail page (`rfq-detail.html`)
  - Fetch RFQ details: `GET /api/v1/rfqs/{id}`
  - Display RFQ information
  - Show associated PR
  - Display supplier quotations
  - RFQ status management

### 6.3 Create RFQ
- [ ] RFQ creation from PR
  - Generate RFQ from approved PR
  - Select procurement mode
  - Add RFQ items
  - Submit: `POST /api/v1/rfqs`

### 6.4 RFQ Dissemination
- [ ] Send RFQ to suppliers
  - Select suppliers
  - Send RFQ notifications
  - Track dissemination status

### 6.5 Canvassing Management
- [ ] Canvass task assignment
  - Assign canvassers
  - Track canvass progress
  - Upload canvass results
  - Mark canvass complete

### 6.6 Supplier Quotations
- [ ] View quotations
  - Display all quotations for RFQ
  - Quotation comparison
  - Compliance checking
  - Best value determination

---

## **PHASE 7: Purchase Orders** 🛒
**Priority: HIGH | Estimated Time: 3-4 days**

### 7.1 Purchase Order List
- [ ] PO list page (`purchase-orders.html`)
  - Fetch POs: `GET /api/v1/purchase-orders`
  - Filter by status, supplier, date
  - Search functionality
  - Status tracking
  - Pagination

### 7.2 Create Purchase Order
- [ ] Generate PO from approved PR
  - Select winning quotation
  - Generate PO number
  - Create PO items
  - Submit: `POST /api/v1/purchase-orders`

### 7.3 Purchase Order Detail
- [ ] PO detail view
  - Fetch PO details: `GET /api/v1/purchase-orders/{id}`
  - Display PO information
  - Show PO items
  - Display supplier information
  - Conforme status tracking

### 7.4 PO Approval Workflow
- [ ] PO approval process
  - Submit for approval
  - Approve/reject PO
  - Track approval status

### 7.5 PO Dissemination
- [ ] Send PO to supplier
  - Generate PO document
  - Send to supplier
  - Track dissemination

### 7.6 Conforme Management
- [ ] Supplier conforme tracking
  - Accept conforme
  - Reject conforme
  - Update PO status

---

## **PHASE 8: Documents & BAC Documents** 📄
**Priority: MEDIUM | Estimated Time: 3-4 days**

### 8.1 Document Management
- [ ] Documents page (`documents.html`)
  - Fetch documents: `GET /api/v1/documents`
  - Filter by category, entity type
  - Search documents
  - Document preview
  - Download documents

### 8.2 Document Upload
- [ ] Upload functionality
  - Multi-file upload
  - Progress tracking
  - File validation (type, size)
  - Submit: `POST /api/v1/documents`
  - Associate with PR/RFQ/PO

### 8.3 Document Viewer
- [ ] Document preview
  - PDF viewer
  - Image viewer
  - Office document preview
  - Download functionality

### 8.4 BAC Documents
- [ ] BAC documents page (`bac-documents.html`)
  - Fetch BAC docs: `GET /api/v1/bac-documents`
  - Filter by type, status
  - Document generation
  - Approval workflow

### 8.5 BAC Document Generation
- [ ] Auto-generate BAC documents
  - Abstract of Quotations
  - Price Matrix
  - TWG Certificate
  - Recommendation
  - Resolution

### 8.6 BAC Document Approval
- [ ] BAC document approval
  - Submit for approval
  - Approve/reject
  - Track approval status

---

## **PHASE 9: Notifications & Activity Logs** 🔔
**Priority: MEDIUM | Estimated Time: 2-3 days**

### 9.1 Notification System
- [ ] Notification bell (`dashboard.html`)
  - Fetch notifications: `GET /api/v1/notifications`
  - Unread count badge
  - Notification dropdown
  - Mark as read
  - Real-time updates (polling)

### 9.2 Notification Types
- [ ] Handle different notification types
  - Approval required
  - Status updates
  - Deadline alerts
  - Overdue alerts
  - Supplier conforme

### 9.3 Activity Log
- [ ] Audit trail page (`audit-trail.html`)
  - Fetch activity logs: `GET /api/v1/activity-logs`
  - Filter by user, action, date
  - Search functionality
  - Export logs

### 9.4 Activity Timeline
- [ ] Display activity timeline
  - Show on PR/PO detail pages
  - Chronological order
  - User information
  - Action details

---

## **PHASE 10: Reports & Analytics** 📈
**Priority: MEDIUM | Estimated Time: 3-4 days**

### 10.1 Reports Page
- [ ] Reports page (`reports.html`)
  - Report type selection
  - Date range picker
  - Filter options
  - Generate reports

### 10.2 Report Types
- [ ] Implement report generators
  - PR Status Report
  - Budget Utilization Report
  - Supplier Performance Report
  - Procurement Timeline Report
  - Department-wise Report

### 10.3 Report Export
- [ ] Export functionality
  - Export to PDF
  - Export to Excel/CSV
  - Print reports

### 10.4 Dashboard Analytics
- [ ] Enhanced dashboard charts
  - Real-time data
  - Interactive charts
  - Drill-down capabilities
  - Custom date ranges

---

## **PHASE 11: Advanced Features** ⚡
**Priority: LOW | Estimated Time: 4-5 days**

### 11.1 Approval Routing
- [ ] Approval workflow management
  - Configure approval routes
  - Multi-level approvals
  - Parallel approvals
  - Approval delegation

### 11.2 Advanced Search
- [ ] Global search functionality
  - Search across all entities
  - Advanced filters
  - Saved searches

### 11.3 Bulk Operations
- [ ] Bulk actions
  - Bulk approve/reject
  - Bulk status update
  - Bulk export

### 11.4 Data Validation
- [ ] Enhanced validation
  - Budget checks
  - Duplicate detection
  - Compliance validation
  - Business rule enforcement

### 11.5 Performance Optimization
- [ ] Optimize performance
  - Lazy loading
  - Virtual scrolling for large lists
  - Image optimization
  - Caching strategies

---

## **PHASE 12: Testing & Polish** ✨
**Priority: HIGH | Estimated Time: 3-4 days**

### 12.1 Error Handling
- [ ] Comprehensive error handling
  - Network errors
  - API errors
  - Validation errors
  - User-friendly error messages

### 12.2 Loading States
- [ ] Loading indicators
  - Skeleton loaders
  - Progress bars
  - Spinner animations

### 12.3 Form Validation
- [ ] Client-side validation
  - Real-time validation
  - Error messages
  - Field-level validation

### 12.4 Responsive Design
- [ ] Mobile optimization
  - Test on mobile devices
  - Touch interactions
  - Mobile navigation

### 12.5 Accessibility
- [ ] A11y improvements
  - Keyboard navigation
  - Screen reader support
  - ARIA labels
  - Focus management

### 12.6 Browser Compatibility
- [ ] Cross-browser testing
  - Chrome, Firefox, Safari, Edge
  - Feature detection
  - Polyfills if needed

---

## **Implementation Notes**

### API Base URL
- Development: `http://127.0.0.1:8000/api/v1`
- Production: Configure via environment variable

### Authentication Flow
1. User logs in → Receive access_token & refresh_token
2. Store tokens in localStorage
3. Include access_token in Authorization header for all requests
4. Auto-refresh token before expiry
5. On 401 error → Attempt refresh → If fails → Redirect to login

### State Management
- Use Vue 3 Composition API with reactive refs
- Consider Pinia for complex state management (optional)

### File Structure
```
frontend/
├── public/
│   └── *.html (UI pages - COMPLETE)
└── src/
    ├── utils/
    │   ├── api.js (API client)
    │   └── helpers.js (Utility functions)
    ├── stores/
    │   ├── auth.js (Authentication state)
    │   └── app.js (App-wide state)
    └── components/ (Reusable components if needed)
```

### Error Handling Strategy
- Centralized error handler in API client
- Toast notifications for user feedback
- Console logging for debugging
- Error boundary for critical errors

---

## **Recommended Implementation Order**

1. **Start with Phase 1** (Core Infrastructure) - Foundation for everything
2. **Then Phase 2** (Dashboard) - Quick wins, visible progress
3. **Then Phase 3** (Purchase Requests) - Core business logic
4. **Continue with Phases 4-7** based on business priority
5. **Finish with Phases 8-12** for polish and advanced features

---

## **Questions to Consider**

1. Which phase should we start with? (Recommended: Phase 1)
2. Do you want real-time updates (WebSocket) or polling?
3. What's the priority order for business features?
4. Any specific requirements for file uploads?
5. Export format preferences (PDF, Excel, CSV)?

---

**Total Estimated Time: 35-45 days** (depending on team size and complexity)
