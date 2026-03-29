# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.2.0] - 2026-03-29

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
- Offline PDF reference asset at `documentation/NukeSurvivalToolkit_Documentation_Release_v2.2.0.pdf`.
- Local font assets under `documentation/docs/assets/fonts/` for Lato, JetBrains Mono, and Titillium Web.
- PDF export source files for browser rendering under `documentation/mkdocs.pdf.yml`, `documentation/scripts/`, `documentation/templates/`, and `documentation/docs/css/`.
- Public root-level `./export_pdf` entrypoint that defaults to the full wiki PDF while exposing section/category filtering through one command.
- Root-level `make_wiki_pdf` entrypoint for section-based local PDF builds, with current `cover`, `about-installation`, `technical-details`, `menu`, `contact`, `special-thanks`, `pages-1-2`, `pages-1-5`, and `non-tool-sections` targets plus versioned review artifacts under `/tmp/nst-wiki-pdf/`.
- Dedicated PDF templates for the Technical Details, Contact, and Special Thanks slices under `documentation/templates/`.
- PDF cover source asset at `documentation/docs/img/pdf/NukeSurvivalToolkit_Splashpage_cover.jpg`.
- Local Julius Sans One font asset at `documentation/docs/assets/fonts/julius-sans-one-400-normal-latin.ttf` for PDF cover typography.
- 48 compressed local video thumbnails under `documentation/docs/img/video-thumbs/` generated from YouTube/Vimeo sources.
- Offline build plugins (`offline`, `privacy`) in `documentation/mkdocs.offline.yml` to support local `file://` search and bundled external assets.
- Standalone `documentation/docs/special-thanks.md` and `documentation/docs/contact.md` pages so those wiki sections can also be targeted directly in the PDF slice workflow.
- `documentation/scripts/stamp_pdf_page_numbers.py` plus the `pypdf` dependency so the finished approved-subset PDFs can receive one consistent post-render page-number treatment.
- `documentation/scripts/add_pdf_toc_links.py` so the merged `full-wiki` PDF can receive clickable Tool Index links and bookmark-outline navigation after the final merge.
- `./make_wiki_pdf full-wiki --category <slug>` for faster TOC and layout validation against a single tool menu while keeping the front matter, generated Tool Index, and end matter in place.
- Default local Ghostscript compression in `./export_pdf`, which now keeps the normal PDF and also writes a `__compressed.pdf` sibling unless `--no-compress` is used.

### Changed

- Expanded iTransform_ae page with sourced images and usage details.
- Expanded VectorMathTools and DeepThickness pages with additional content and images.
- Renamed `bm-lightwrap.md` to `bm-optical-lightwrap.md` and updated filter index link to match toolkit rename.
- Normalized markdown list spacing across documentation pages to prevent collapsed paragraph/list rendering.
- Updated `AdditiveKeyerPro` input section so each input bullet maps to the correct reference image, with those four input images displayed at 75% width.
- Initialized repository git metadata for this wiki project.
- Reworked `README.md` to prioritize the live wiki URL at the top, simplified section hierarchy, and clarified online/offline usage paths.
- Made the README header banner image clickable to the live documentation site.
- Refocused `README.md` into a user-facing landing page and moved practical build and export steps into `documentation/USER_GUIDE.md`, while trimming `documentation/DEVELOPMENT.md` back toward contributor-facing notes.
- Updated `.gitignore` to allow versioning the official offline documentation PDF.
- Split MkDocs configuration into online (`documentation/mkdocs.yml`) and offline (`documentation/mkdocs.offline.yml`) builds so GitHub Pages behavior remains unchanged while local ZIP behavior is optimized for `file://`.
- Updated README and development docs with explicit online/offline build commands and offline ZIP entrypoint guidance (`site/index.html`).
- Switched documentation fonts to local assets and disabled remote font loading for offline reliability.
- Added browser-PDF build instructions while clarifying that generated PDF test outputs stay local and should not be committed.
- Shifted the active PDF workflow toward section-by-section approval through `make_wiki_pdf` instead of treating the full-book browser build path as the only entrypoint.
- Split the old combined About end matter into standalone `special-thanks.md` and `contact.md` wiki pages, and removed `About` from the live nav because it no longer carried meaningful standalone content.
- Switched `make_wiki_pdf` content slices to a markdown-backed contextual build so `technical-details`, `menu`, `special-thanks`, and `contact` now render from the same source files as the wiki while preserving the approved PDF shell.
- Updated **`non-tool-sections`** to build the current approved subset from those markdown-backed slices instead of stitching standalone content templates together.
- Replaced per-template HTML footer numbering with one shared post-render PDF-numbering pass so the cover and all interior approved pages use the same visible number placement.
- Added a merged `full-wiki` PDF path that preserves the approved non-tool main-page render as truth, builds tool pages separately, then combines front main pages, tool pages, and end matter before stamping one consecutive page-number sequence across the merged result.
- Returned `make_tool_pages_pdf` to a tool-only build path while keeping category-limited subset renders for review and exposing an internal no-page-number mode for merged-PDF assembly.
- Updated `full-wiki` to insert a generated `Tool Index` PDF between the main pages and tool pages, resolve its page numbers from the rendered tool-pages PDF, and inject matching bookmark/sidebar navigation into the finished document.
- Consolidated the public PDF workflow around `./export_pdf` so users no longer need to learn separate entrypoint scripts for full, tool-only, or filtered exports.
- Updated `./export_pdf` to default generated PDFs into repo-local `output/pdf/` and use unique date-stamped release-style filenames with optional subset suffixes.
- Tuned the default `./export_pdf` compression profile around `128 dpi` color/gray image downsampling with forced JPEG recompression, and updated `--open` to prefer the compressed sibling when one is generated.
- Updated mixed/full PDF exports to compress the stamped PDF first and then reapply Tool Index links and bookmark-outline navigation to the compressed sibling so the release artifact keeps working navigation.
- Updated the docs home page release label to `v2.2.0`.
- Moved `export_pdf`, `make_wiki_pdf`, and `make_tool_pages_pdf` into `buildPDF/`; added a repo-root `./export_pdf` launcher script so the public command path stays the same.
- `make_wiki_pdf` **`non-tool-sections`** target: one merged PDF of all non-tool sections (cover through contact).

### Fixed

- Fixed offline `file://` search visibility and sidebar layout behavior by using an offline-specific MkDocs configuration (including disabled `navigation.instant` for offline builds).
- Fixed offline video flicker by stabilizing render mode detection and preventing repeated embed/fallback re-renders.
- Fixed broken fallback thumbnail rendering by replacing invalid placeholder-image dependencies with a resilient inline SVG fallback and a generated-thumbnail fallback chain.
- Fixed long-form PDF export truncation after `AutoFlare` by rendering the merged HTML with Playwright + Chrome instead of relying on WeasyPrint's final PDF output.
- Fixed PDF cover softness by using the committed JPEG cover source instead of regenerating a low-resolution temporary cover image.
- Fixed inconsistent approved-subset page number placement by stamping the final PDFs after render instead of relying on template-specific HTML placement.
- Fixed forced blank space in the `technical-details` review pages by allowing the markdown-derived content to paginate naturally before extracting the approved slice.
- Fixed stale `bm_Lightwrap` nav paths in the online, offline, and PDF MkDocs configs so the generated Tool Index can scan the full nav without hitting missing markdown files.
- Fixed `full-wiki` Tool Index grouping so `Special Thanks` and `Contact` stay in back matter and are not searched inside the tool-pages PDF.

### Removed

- Removed orphaned DeepToPosition wiki page — gizmo no longer exists in the toolkit (#1).

## [0.1.0] - 2026-02-06

### Added

- Initial MkDocs-based wiki structure under `documentation/` with authored tool pages and media assets.
- MkDocs configuration for local build/serve and GitHub Pages deployment workflow.
- Root repository scaffolding (`README.md`, `.gitignore`, `.github/workflows/mkdocs.yml`).
