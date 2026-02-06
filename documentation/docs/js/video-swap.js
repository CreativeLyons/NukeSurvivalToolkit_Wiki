/**
 * Nuke Survival Toolkit - Video Swap Script
 * Detects online/offline status and swaps video embeds accordingly
 * - Online: Shows embedded video player (YouTube/Vimeo iframe)
 * - Offline: Shows thumbnail with link to video URL
 */

(function() {
    'use strict';

    // Configuration
    const YOUTUBE_EMBED_BASE = 'https://www.youtube.com/embed/';
    const VIMEO_EMBED_BASE = 'https://player.vimeo.com/video/';
    const YOUTUBE_WATCH_BASE = 'https://www.youtube.com/watch?v=';
    const VIMEO_WATCH_BASE = 'https://vimeo.com/';
    
    // Default thumbnail if none specified
    const DEFAULT_THUMBNAIL = 'img/video-placeholder.jpg';

    /**
     * Check if we're online
     */
    function isOnline() {
        return navigator.onLine;
    }

    /**
     * Generate embed URL based on video type
     */
    function getEmbedUrl(videoId, videoType) {
        if (videoType === 'vimeo') {
            return VIMEO_EMBED_BASE + videoId + '?byline=0&portrait=0';
        }
        // Default to YouTube
        return YOUTUBE_EMBED_BASE + videoId + '?rel=0';
    }

    /**
     * Generate watch URL based on video type
     */
    function getWatchUrl(videoId, videoType) {
        if (videoType === 'vimeo') {
            return VIMEO_WATCH_BASE + videoId;
        }
        // Default to YouTube
        return YOUTUBE_WATCH_BASE + videoId;
    }

    /**
     * Create online embed (iframe)
     */
    function createEmbed(container, videoId, videoType) {
        const embedUrl = getEmbedUrl(videoId, videoType);
        container.innerHTML = `
            <div class="video-embed-wrapper" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
                <iframe 
                    src="${embedUrl}" 
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen>
                </iframe>
            </div>
        `;
    }

    /**
     * Create offline fallback (thumbnail + link)
     */
    function createOfflineFallback(container, videoId, videoType, thumbnailPath) {
        const watchUrl = getWatchUrl(videoId, videoType);
        const thumbnail = thumbnailPath || DEFAULT_THUMBNAIL;
        const platformName = videoType === 'vimeo' ? 'Vimeo' : 'YouTube';
        
        container.innerHTML = `
            <div class="video-offline-wrapper" style="position: relative; max-width: 640px;">
                <a href="${watchUrl}" target="_blank" rel="noopener noreferrer" title="Watch on ${platformName}">
                    <img src="${thumbnail}" alt="Video thumbnail" style="width: 100%; display: block; border-radius: 4px;" onerror="this.src='${DEFAULT_THUMBNAIL}'">
                    <div class="video-play-overlay" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(0,0,0,0.7); border-radius: 50%; width: 72px; height: 72px; display: flex; align-items: center; justify-content: center;">
                        <svg width="32" height="32" viewBox="0 0 24 24" fill="white">
                            <path d="M8 5v14l11-7z"/>
                        </svg>
                    </div>
                </a>
                <p style="margin-top: 8px; font-size: 14px; color: #666;">
                    <em>You appear to be offline.</em> 
                    <a href="${watchUrl}" target="_blank" rel="noopener noreferrer">Watch on ${platformName}</a> when online.
                </p>
            </div>
        `;
    }

    /**
     * Process all video containers on the page
     */
    function processVideoContainers() {
        const containers = document.querySelectorAll('.video-container');
        const online = isOnline();

        containers.forEach(function(container) {
            const videoId = container.getAttribute('data-video-id');
            const videoType = container.getAttribute('data-video-type') || 'youtube';
            const thumbnail = container.getAttribute('data-thumbnail');

            if (!videoId) {
                console.warn('Video container missing data-video-id attribute');
                return;
            }

            if (online) {
                createEmbed(container, videoId, videoType);
            } else {
                createOfflineFallback(container, videoId, videoType, thumbnail);
            }
        });
    }

    /**
     * Re-process when online status changes
     */
    function handleOnlineStatusChange() {
        processVideoContainers();
    }

    /**
     * Initialize
     */
    function init() {
        processVideoContainers();
        // Remove existing listeners to avoid duplicates if re-initializing
        window.removeEventListener('online', handleOnlineStatusChange);
        window.removeEventListener('offline', handleOnlineStatusChange);
        
        window.addEventListener('online', handleOnlineStatusChange);
        window.addEventListener('offline', handleOnlineStatusChange);
    }

    // Support for MkDocs Material 'instant' loading
    if (typeof document$ !== 'undefined') {
        document$.subscribe(function() {
            init();
        });
    } 
    // Fallback for standard themes
    else if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
