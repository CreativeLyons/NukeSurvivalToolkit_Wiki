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
            // Calculate active link offset within the scroll container.
            // offsetTop is stable for full page loads and avoids repeated scroll drift.
            var target = activeLink.offsetTop - ((sidebar.clientHeight - activeLink.clientHeight) / 2);
            var maxScroll = Math.max(0, sidebar.scrollHeight - sidebar.clientHeight);
            var clampedTarget = Math.max(0, Math.min(maxScroll, target));
            sidebar.scrollTop = clampedTarget;
        }
    }

    function scheduleScroll(delay) {
        setTimeout(scrollSidebar, delay);
    }

    // Run on initial page load and after all assets settle.
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            scheduleScroll(100);
        });
    } else {
        scheduleScroll(100);
    }
    window.addEventListener('load', function() {
        scheduleScroll(50);
    });
    
    // Listen for MkDocs Material instant navigation events
    // document$ is an RxJS observable provided by Material for MkDocs
    if (typeof document$ !== 'undefined') {
        document$.subscribe(function() {
            scheduleScroll(120);
        });
    }

    // Fallback for non-instant navigation: center shortly after nav link clicks.
    document.addEventListener('click', function(event) {
        var target = event.target && event.target.closest('.md-sidebar--primary a.md-nav__link');
        if (target) {
            scheduleScroll(120);
        }
    });
})();
