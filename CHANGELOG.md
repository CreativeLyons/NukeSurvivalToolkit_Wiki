# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

**New tool pages (29 pages with images):**

- 3D: MirrorDimension
- CG: aeRefracTHOR, Emission, LightSwitch, LightSwitchPuppet
- Channel: ID_Extractor
- Color: aeRelight2D
- Deep: DeepThickness
- Draw: BokehBuilder, ConstantPro, HexColor, LensEngine, Rings of Power, SpotLight
- Filter: aeShadows, ChromaSmear, fxT_ChromaticAberration, RadialDilate
- Filter/Blur: MotionBlurPaint
- Filter/Distort: apEdgeCrush, FastComplexityDistort
- Filter/Edges: GuidedBlur, iErode
- Keyer: PointCloudKeyer, SkyMatte
- Time: FrameHoldSpecial
- Transform: iTransform (archived page), RotoPaintTransform, Symmetry

**Infrastructure:**

- README banner image asset at `documentation/docs/img/nst-wiki-large.jpeg`.
- Offline PDF reference asset at `documentation/NukeSurvivalToolkit_Documentation_Release_v2.1.0.pdf`.
- Local font assets under `documentation/docs/assets/fonts/` for Lato, JetBrains Mono, and Titillium Web.
- PDF export source files for browser rendering under `documentation/mkdocs.pdf.yml`, `documentation/scripts/`, `documentation/templates/`, and `documentation/docs/css/`.
- Root-level `make_wiki_pdf` entrypoint for section-based local PDF builds, with current `cover`, `page2`, `technical-details`, `contact`, `special-thanks`, `pages-1-2`, `pages-1-5`, and `full-so-far` targets plus versioned review artifacts under `/tmp/nst-wiki-pdf/`.
- Dedicated PDF templates for the Technical Details, Contact, and Special Thanks slices under `documentation/templates/`.
- PDF cover source asset at `documentation/docs/img/pdf/NukeSurvivalToolkit_Splashpage_cover.jpg`.
- Local Julius Sans One font asset at `documentation/docs/assets/fonts/julius-sans-one-400-normal-latin.ttf` for PDF cover typography.
- 48 compressed local video thumbnails under `documentation/docs/img/video-thumbs/` generated from YouTube/Vimeo sources.
- Offline build plugins (`offline`, `privacy`) in `documentation/mkdocs.offline.yml` to support local `file://` search and bundled external assets.

### Changed

- Expanded iTransform_ae page with sourced images and usage details.
- Expanded VectorMathTools and DeepThickness pages with additional content and images.
- Renamed `bm-lightwrap.md` to `bm-optical-lightwrap.md` and updated filter index link to match toolkit rename.
- Normalized markdown list spacing across documentation pages to prevent collapsed paragraph/list rendering.
- Updated `AdditiveKeyerPro` input section so each input bullet maps to the correct reference image, with those four input images displayed at 75% width.
- Initialized repository git metadata for this wiki project.
- Reworked `README.md` to prioritize the live wiki URL at the top, simplified section hierarchy, and clarified online/offline usage paths.
- Made the README header banner image clickable to the live documentation site.
- Updated `.gitignore` to allow versioning the official offline documentation PDF.
- Split MkDocs configuration into online (`documentation/mkdocs.yml`) and offline (`documentation/mkdocs.offline.yml`) builds so GitHub Pages behavior remains unchanged while local ZIP behavior is optimized for `file://`.
- Updated README and development docs with explicit online/offline build commands and offline ZIP entrypoint guidance (`site/index.html`).
- Switched documentation fonts to local assets and disabled remote font loading for offline reliability.
- Added browser-PDF build instructions while clarifying that generated PDF test outputs stay local and should not be committed.
- Shifted the active PDF workflow toward section-by-section approval through `make_wiki_pdf` instead of treating the full-book browser build path as the only entrypoint.
- Replaced the placeholder About page with project credits, acknowledgments, and contact links.
- Standardized the interior PDF page shell around the approved page 2 layout so page margin, side padding, base typography, and link styling are shared across the standalone interior-section templates.
- Added a standalone Contact page template and appended it to the `full-so-far` PDF assembly so the current combined build now ends with the reference contact page.
- Updated the docs home page release label to `v2.2.0`.

### Fixed

- Fixed offline `file://` search visibility and sidebar layout behavior by using an offline-specific MkDocs configuration (including disabled `navigation.instant` for offline builds).
- Fixed offline video flicker by stabilizing render mode detection and preventing repeated embed/fallback re-renders.
- Fixed broken fallback thumbnail rendering by replacing invalid placeholder-image dependencies with a resilient inline SVG fallback and a generated-thumbnail fallback chain.
- Fixed long-form PDF export truncation after `AutoFlare` by rendering the merged HTML with Playwright + Chrome instead of relying on WeasyPrint's final PDF output.
- Fixed PDF cover softness by using the committed JPEG cover source instead of regenerating a low-resolution temporary cover image.

### Removed

- Removed orphaned DeepToPosition wiki page — gizmo no longer exists in the toolkit (#1).

## [0.1.0] - 2026-02-06

### Added

- Initial MkDocs-based wiki structure under `documentation/` with authored tool pages and media assets.
- MkDocs configuration for local build/serve and GitHub Pages deployment workflow.
- Root repository scaffolding (`README.md`, `.gitignore`, `.github/workflows/mkdocs.yml`).
