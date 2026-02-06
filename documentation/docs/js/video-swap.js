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
    const RENDER_MODE_ATTR = 'data-video-render-mode';
    let statusChangeTimer = null;
    let defaultThumbnailUrl = null;
    let siteBaseUrl = null;

    function getSiteBaseUrl() {
        if (siteBaseUrl) {
            return siteBaseUrl;
        }

        try {
            const configEl = document.getElementById('__config');
            if (configEl) {
                const config = JSON.parse(configEl.textContent || '{}');
                const base = config.base || '.';
                siteBaseUrl = new URL(base + '/', window.location.href);
                return siteBaseUrl;
            }
        } catch (error) {
            // Fall through to a location-based default path.
        }

        siteBaseUrl = new URL('./', window.location.href);
        return siteBaseUrl;
    }

    function getDefaultThumbnailUrl() {
        if (defaultThumbnailUrl) {
            return defaultThumbnailUrl;
        }
        const svg = `
            <svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
                <defs>
                    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
                        <stop offset="0%" stop-color="#24292f"/>
                        <stop offset="100%" stop-color="#111418"/>
                    </linearGradient>
                </defs>
                <rect width="1280" height="720" fill="url(#bg)"/>
                <circle cx="640" cy="360" r="88" fill="#000000AA"/>
                <polygon points="615,310 615,410 700,360" fill="#FFFFFF"/>
                <text x="640" y="560" text-anchor="middle" fill="#D0D7DE" font-family="Arial, sans-serif" font-size="40">
                    Video Preview
                </text>
            </svg>
        `.trim();
        defaultThumbnailUrl = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
        return defaultThumbnailUrl;
    }

    function getGeneratedThumbnailUrl(videoId, videoType) {
        const baseUrl = getSiteBaseUrl();
        return new URL(`img/video-thumbs/${videoType}-${videoId}.webp`, baseUrl).toString();
    }

    /**
     * Check if we're online
     */
    function getRenderMode() {
        // file:// builds should always use offline fallback mode to avoid
        // flaky network/worker checks in local browser security contexts.
        if (window.location.protocol === 'file:') {
            return 'offline';
        }
        return navigator.onLine ? 'online' : 'offline';
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
        const fallbackThumbnail = getDefaultThumbnailUrl();
        const generatedThumbnail = getGeneratedThumbnailUrl(videoId, videoType);
        const platformName = videoType === 'vimeo' ? 'Vimeo' : 'YouTube';

        container.innerHTML = `
            <div class="video-offline-wrapper" style="position: relative; max-width: 640px;">
                <a href="${watchUrl}" target="_blank" rel="noopener noreferrer" title="Watch on ${platformName}">
                    <img alt="Video thumbnail" style="width: 100%; display: block; border-radius: 4px;">
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

        const imgEl = container.querySelector('img');
        if (!imgEl) {
            return;
        }

        const candidates = [];
        const pushUnique = function(src) {
            if (src && !candidates.includes(src)) {
                candidates.push(src);
            }
        };

        pushUnique(generatedThumbnail);
        pushUnique(thumbnailPath);
        pushUnique(fallbackThumbnail);

        let idx = 0;
        const loadNext = function() {
            idx += 1;
            if (idx < candidates.length) {
                imgEl.src = candidates[idx];
            } else {
                imgEl.onerror = null;
            }
        };

        imgEl.onerror = loadNext;
        imgEl.src = candidates[0];
    }

    /**
     * Process all video containers on the page
     */
    function processVideoContainers(forceRender) {
        const containers = document.querySelectorAll('.video-container');
        const mode = getRenderMode();
        const online = mode === 'online';

        containers.forEach(function(container) {
            const videoId = container.getAttribute('data-video-id');
            const videoType = container.getAttribute('data-video-type') || 'youtube';
            const thumbnail = container.getAttribute('data-thumbnail');
            const previousMode = container.getAttribute(RENDER_MODE_ATTR);

            if (!videoId) {
                console.warn('Video container missing data-video-id attribute');
                return;
            }

            if (!forceRender && previousMode === mode) {
                return;
            }

            if (online) {
                createEmbed(container, videoId, videoType);
            } else {
                createOfflineFallback(container, videoId, videoType, thumbnail);
            }

            container.setAttribute(RENDER_MODE_ATTR, mode);
        });
    }

    /**
     * Re-process when online status changes
     */
    function handleOnlineStatusChange() {
        if (statusChangeTimer) {
            clearTimeout(statusChangeTimer);
        }
        statusChangeTimer = setTimeout(function() {
            processVideoContainers(false);
        }, 250);
    }

    /**
     * Initialize
     */
    function init() {
        processVideoContainers(true);
        // Remove existing listeners to avoid duplicates if re-initializing
        window.removeEventListener('online', handleOnlineStatusChange);
        window.removeEventListener('offline', handleOnlineStatusChange);

        // No network-event listeners for local file:// mode; stay in fallback.
        if (window.location.protocol !== 'file:') {
            window.addEventListener('online', handleOnlineStatusChange);
            window.addEventListener('offline', handleOnlineStatusChange);
        }
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
