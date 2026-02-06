/**
 * Open all external links in new tabs
 * Checks if the link hostname differs from the current window hostname
 */
(function() {
    'use strict';

    function fixExternalLinks() {
        var currentHost = window.location.hostname;
        
        document.querySelectorAll('a').forEach(function(link) {
            // Only act on http/https links
            if (link.protocol.startsWith('http')) {
                // If the hostname is different, it's external
                if (link.hostname !== currentHost) {
                    if (!link.hasAttribute('target')) {
                        link.setAttribute('target', '_blank');
                        link.setAttribute('rel', 'noopener noreferrer');
                    }
                }
            }
        });
    }

    // Support for MkDocs Material 'instant' loading
    if (typeof document$ !== 'undefined') {
        document$.subscribe(function() {
            fixExternalLinks();
        });
    } 
    // Fallback for standard themes
    else if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fixExternalLinks);
    } else {
        fixExternalLinks();
    }
})();
