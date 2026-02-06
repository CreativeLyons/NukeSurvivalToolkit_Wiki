/**
 * Force Sidebar Scroll to Active Item
 * Ensures the active navigation item is visible in the sidebar on page load
 * and after instant navigation events.
 */
(function() {
    function scrollSidebar() {
        // Target the primary sidebar's scroll container
        var sidebar = document.querySelector('.md-sidebar--primary .md-sidebar__scrollwrap');
        // Target the active link (try current page link first, then any active)
        var activeLink = document.querySelector('.md-sidebar--primary .md-nav__link--active');
        
        if (sidebar && activeLink) {
            // Get dimensions
            var sidebarRect = sidebar.getBoundingClientRect();
            var activeRect = activeLink.getBoundingClientRect();
            
            // Calculate the position of the active link relative to the visible sidebar area
            var offsetFromTop = activeRect.top - sidebarRect.top;
            
            // Center the active link in the sidebar viewport
            var centerPosition = (sidebar.clientHeight / 2) - (activeLink.clientHeight / 2);
            var scrollAdjustment = offsetFromTop - centerPosition;
            
            // Use smooth scrolling for a better UX
            sidebar.scrollBy({ top: scrollAdjustment, behavior: 'smooth' });
        }
    }

    // Run on initial page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(scrollSidebar, 150);
        });
    } else {
        setTimeout(scrollSidebar, 150);
    }
    
    // Listen for MkDocs Material instant navigation events
    // document$ is an RxJS observable provided by Material for MkDocs
    if (typeof document$ !== 'undefined') {
        document$.subscribe(function() {
            setTimeout(scrollSidebar, 200);
        });
    } else {
        // Fallback: observe URL changes via popstate/pushstate for instant navigation
        var lastUrl = location.href;
        new MutationObserver(function() {
            if (location.href !== lastUrl) {
                lastUrl = location.href;
                setTimeout(scrollSidebar, 200);
            }
        }).observe(document, { subtree: true, childList: true });
    }
})();
