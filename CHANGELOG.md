# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Normalized markdown list spacing across documentation pages to prevent collapsed paragraph/list rendering.
- Updated `AdditiveKeyerPro` input section so each input bullet maps to the correct reference image, with those four input images displayed at 75% width.
- Initialized repository git metadata for this wiki project.
- Reworked `README.md` to prioritize the live wiki URL at the top, simplified section hierarchy, and clarified online/offline usage paths.
- Made the README header banner image clickable to the live documentation site.
- Updated `.gitignore` to allow versioning the official offline documentation PDF.
- Split MkDocs configuration into online (`documentation/mkdocs.yml`) and offline (`documentation/mkdocs.offline.yml`) builds so GitHub Pages behavior remains unchanged while local ZIP behavior is optimized for `file://`.
- Updated README and development docs with explicit online/offline build commands and offline ZIP entrypoint guidance (`site/index.html`).
- Switched documentation fonts to local assets and disabled remote font loading for offline reliability.

### Added

- Added README banner image asset at `documentation/docs/img/nst-wiki-large.jpeg`.
- Added offline PDF reference asset at `documentation/NukeSurvivalToolkit_Documentation_Release_v2.1.0.pdf`.
- Added local font assets under `documentation/docs/assets/fonts/` for Lato, JetBrains Mono, and Titillium Web.
- Added 48 compressed local video thumbnails under `documentation/docs/img/video-thumbs/` generated from YouTube/Vimeo sources.
- Added offline build plugins (`offline`, `privacy`) in `documentation/mkdocs.offline.yml` to support local `file://` search and bundled external assets.

### Fixed

- Fixed offline `file://` search visibility and sidebar layout behavior by using an offline-specific MkDocs configuration (including disabled `navigation.instant` for offline builds).
- Fixed offline video flicker by stabilizing render mode detection and preventing repeated embed/fallback re-renders.
- Fixed broken fallback thumbnail rendering by replacing invalid placeholder-image dependencies with a resilient inline SVG fallback and a generated-thumbnail fallback chain.

## [0.1.0] - 2026-02-06

### Added

- Initial MkDocs-based wiki structure under `documentation/` with authored tool pages and media assets.
- MkDocs configuration for local build/serve and GitHub Pages deployment workflow.
- Root repository scaffolding (`README.md`, `.gitignore`, `.github/workflows/mkdocs.yml`).
