/**
 * Navigation Component
 * Reusable navigation component for all pages
 */

(function() {
    'use strict';

    /**
     * Render navigation bar
     */
    function renderNavbar(user, onLogout) {
        return `
            <nav class="glass shadow-sm border-b border-white/20 h-16">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full">
                    <div class="flex justify-between items-center h-full">
                        <div class="flex items-center">
                            <a href="/dashboard.html" class="flex-shrink-0 flex items-center">
                                <div class="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center shadow-lg">
                                    <i class="ph ph-buildings text-white text-xl"></i>
                                </div>
                                <span class="ml-3 text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">DICT Procurement</span>
                            </a>
                        </div>
                        <div class="flex items-center gap-4">
                            <button class="notification-dot p-2 rounded-lg hover:bg-gray-100 transition-colors relative">
                                <i class="ph ph-bell text-gray-600 text-xl"></i>
                            </button>
                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 rounded-xl gradient-info flex items-center justify-center text-white font-bold">
                                    ${user?.name?.charAt(0) || 'U'}
                                </div>
                                <span class="text-gray-700 font-medium hidden md:inline">${user?.name || 'User'}</span>
                            </div>
                            <button
                                onclick="window.navigationComponent.handleLogout()"
                                class="btn-secondary text-sm"
                            >
                                <i class="ph ph-sign-out mr-2"></i>
                                <span class="hidden md:inline">Logout</span>
                            </button>
                        </div>
                    </div>
                </div>
            </nav>
        `;
    }

    /**
     * Render sidebar navigation
     */
    function renderSidebar(user, currentPageId) {
        if (!window.navigationService) {
            return '<div>Navigation service not loaded</div>';
        }

        const visibleItems = window.navigationService.getVisibleMenuItems(user?.role);
        
        const menuItemsHtml = visibleItems.map(item => {
            const active = window.navigationService.isActive(item);
            return `
                <a href="${item.path}" 
                   class="sidebar-link ${active ? 'active' : ''}"
                   data-menu-id="${item.id}">
                    <i class="${item.icon}"></i>
                    <span>${item.label}</span>
                </a>
            `;
        }).join('');

        return `
            <aside class="hidden lg:flex flex-col w-64 bg-white border-r border-gray-200" style="height: calc(100vh - 4rem);">
                <div class="p-4 border-b border-gray-200">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
                            <i class="ph ph-buildings text-white text-xl"></i>
                        </div>
                        <div>
                            <h2 class="font-bold text-gray-900">DICT Procurement</h2>
                            <p class="text-xs text-gray-500">${user?.role?.replace('_', ' ') || 'User'}</p>
                        </div>
                    </div>
                </div>
                
                <nav class="flex-1 p-4 space-y-1 overflow-y-auto">
                    ${menuItemsHtml}
                </nav>
                
                <div class="p-4 border-t border-gray-200 space-y-1">
                    <a href="/profile.html" class="sidebar-link">
                        <i class="ph ph-user"></i>
                        <span>Profile</span>
                    </a>
                    <button onclick="window.navigationComponent.handleLogout()" class="sidebar-link text-red-600 hover:text-red-700 w-full text-left">
                        <i class="ph ph-sign-out"></i>
                        <span>Logout</span>
                    </button>
                </div>
            </aside>
        `;
    }

    /**
     * Render mobile menu
     */
    function renderMobileMenu(user, isOpen) {
        if (!window.navigationService) {
            return '';
        }

        const visibleItems = window.navigationService.getVisibleMenuItems(user?.role);
        
        const menuItemsHtml = visibleItems.map(item => {
            const active = window.navigationService.isActive(item);
            return `
                <a href="${item.path}" 
                   class="mobile-menu-link ${active ? 'active' : ''}"
                   data-menu-id="${item.id}">
                    <i class="${item.icon}"></i>
                    <span>${item.label}</span>
                </a>
            `;
        }).join('');

        return `
            <div class="mobile-menu-overlay ${isOpen ? 'open' : ''}" onclick="window.navigationComponent.toggleMobileMenu()">
                <div class="mobile-menu ${isOpen ? 'open' : ''}" onclick="event.stopPropagation()">
                    <div class="p-4 border-b border-gray-200 flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
                                <i class="ph ph-buildings text-white text-xl"></i>
                            </div>
                            <span class="font-bold text-gray-900">Menu</span>
                        </div>
                        <button onclick="window.navigationComponent.toggleMobileMenu()" class="p-2 rounded-lg hover:bg-gray-100">
                            <i class="ph ph-x text-gray-600 text-xl"></i>
                        </button>
                    </div>
                    <nav class="p-4 space-y-1 overflow-y-auto">
                        ${menuItemsHtml}
                        <a href="/profile.html" class="mobile-menu-link">
                            <i class="ph ph-user"></i>
                            <span>Profile</span>
                        </a>
                        <button onclick="window.navigationComponent.handleLogout()" class="mobile-menu-link text-red-600 hover:text-red-700 w-full text-left">
                            <i class="ph ph-sign-out"></i>
                            <span>Logout</span>
                        </button>
                    </nav>
                </div>
            </div>
        `;
    }

    /**
     * Render breadcrumbs
     */
    function renderBreadcrumbs() {
        if (!window.navigationService) {
            return '';
        }

        const breadcrumbs = window.navigationService.getBreadcrumbs();
        
        const breadcrumbsHtml = breadcrumbs.map((crumb, index) => {
            const isLast = index === breadcrumbs.length - 1;
            return `
                <li class="flex items-center">
                    ${index > 0 ? '<i class="ph ph-caret-right text-gray-400 mx-2"></i>' : ''}
                    ${isLast ? `
                        <span class="text-gray-900 font-medium">${crumb.label}</span>
                    ` : `
                        <a href="${crumb.path}" class="text-gray-600 hover:text-indigo-600 transition-colors">
                            ${crumb.icon ? `<i class="${crumb.icon} mr-1"></i>` : ''}
                            ${crumb.label}
                        </a>
                    `}
                </li>
            `;
        }).join('');

        return `
            <nav class="mb-6" aria-label="Breadcrumb">
                <ol class="flex items-center space-x-2 text-sm">
                    ${breadcrumbsHtml}
                </ol>
            </nav>
        `;
    }

    /**
     * Initialize navigation component
     */
    function initNavigation(containerId, user) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Navigation container #${containerId} not found`);
            return;
        }

        // Render navigation
        const navbarHtml = renderNavbar(user);
        container.innerHTML = navbarHtml;
        
        // Add mobile menu toggle button
        const nav = container.querySelector('nav');
        if (nav) {
            const logoArea = nav.querySelector('.flex-shrink-0');
            if (logoArea) {
                const mobileToggle = document.createElement('button');
                mobileToggle.className = 'lg:hidden ml-4 p-2 rounded-lg hover:bg-gray-100 transition-colors';
                mobileToggle.innerHTML = '<i class="ph ph-list text-gray-600 text-xl"></i>';
                mobileToggle.onclick = () => window.navigationComponent.toggleMobileMenu();
                logoArea.appendChild(mobileToggle);
            }
        }

        // Add mobile menu to body if not already added
        if (!document.querySelector('.mobile-menu-overlay')) {
            const mobileMenuHtml = renderMobileMenu(user, false);
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = mobileMenuHtml;
            document.body.appendChild(tempDiv.firstElementChild);
        }
    }

    /**
     * Initialize sidebar
     */
    function initSidebar(containerId, user) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Sidebar container #${containerId} not found`);
            return;
        }

        container.innerHTML = renderSidebar(user);
    }

    /**
     * Initialize breadcrumbs
     */
    function initBreadcrumbs(containerId) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Breadcrumbs container #${containerId} not found`);
            return;
        }

        container.innerHTML = renderBreadcrumbs();
    }

    /**
     * Toggle mobile menu
     */
    function toggleMobileMenu() {
        const overlay = document.querySelector('.mobile-menu-overlay');
        const menu = document.querySelector('.mobile-menu');
        
        if (overlay && menu) {
            const isOpen = overlay.classList.contains('open');
            if (isOpen) {
                overlay.classList.remove('open');
                menu.classList.remove('open');
            } else {
                overlay.classList.add('open');
                menu.classList.add('open');
            }
        }
    }

    /**
     * Handle logout
     */
    async function handleLogout() {
        if (confirm('Are you sure you want to logout?')) {
            try {
                if (window.authStore) {
                    await window.authStore.logout();
                } else {
                    // Fallback: clear tokens manually
                    if (window.TokenManager) {
                        window.TokenManager.clearTokens();
                    }
                    localStorage.clear();
                }
                window.location.href = '/login.html';
            } catch (err) {
                console.error('Logout error:', err);
                // Force logout
                if (window.TokenManager) {
                    window.TokenManager.clearTokens();
                }
                localStorage.clear();
                window.location.href = '/login.html';
            }
        }
    }

    // Export navigation component
    window.navigationComponent = {
        renderNavbar,
        renderSidebar,
        renderMobileMenu,
        renderBreadcrumbs,
        initNavigation,
        initSidebar,
        initBreadcrumbs,
        toggleMobileMenu,
        handleLogout
    };

})();
