# Development

Contributor-facing notes for the NST wiki repository.

For step-by-step build, preview, publishing, and PDF export instructions, start with `documentation/USER_GUIDE.md`. This file is for repository structure, deployment behavior, and deeper PDF implementation context.

**PDF decision history and dated experiments** (WeasyPrint vs Playwright, benchmarks, debugging notes): [PDF pipeline history](archive/pdf-pipeline-history.md) — tracked, not part of the MkDocs site.

**AI assistants:** see repo-root `AGENTS.md` for how this file relates to the archive and the user guide.

## Repository Layout

- `documentation/docs/`: markdown pages and static assets used by MkDocs. The public site’s landing page body is `documentation/docs/index.md` (MkDocs home at `/`).
- `documentation/mkdocs.yml`: online GitHub Pages configuration. **Sidebar `nav` is defined only here** (single source of truth).
- `documentation/mkdocs.offline.yml`: offline ZIP and local-file configuration. Uses MkDocs `INHERIT: mkdocs.yml` and overrides only plugins, theme, and scripts needed for `file://` viewing—do not duplicate `nav` in this file.
- `documentation/mkdocs.pdf.yml`: merged HTML configuration that supports the PDF pipeline.
- `documentation/site/`: local HTML build output (ignored in git).
- `.github/workflows/mkdocs.yml`: GitHub Pages build and deploy workflow.
- `./export_pdf`: public PDF export entrypoint (thin bash launcher at the repo root).
- `buildPDF/`: PDF export implementations — `export_pdf`, `make_wiki_pdf`, and `make_tool_pages_pdf` (the public command is still `./export_pdf` from the repo root).

## Build Modes

- Online/public site: driven by `documentation/mkdocs.yml`.
- Offline HTML wiki: driven by `documentation/mkdocs.offline.yml` (inherits `mkdocs.yml`; same sidebar as online).
- Offline PDF export: run through `./export_pdf`, which delegates to the internal PDF builder scripts.

## Deployment Summary

GitHub Pages deployment is handled by `.github/workflows/mkdocs.yml`.

The workflow triggers on pushes to `main` or `master` when files under `documentation/**` change, installs `mkdocs-material`, builds from `documentation/mkdocs.yml`, and deploys `documentation/site/`. It also runs `mkdocs build -f mkdocs.offline.yml` to a throwaway directory so a broken offline config fails the job before deploy.

## PDF pipeline

### Main entrypoint

- The main repo-visible PDF entrypoint is `./export_pdf` at the repository root.
- `./export_pdf` defaults to the `full-wiki` preset and exposes the supported user-facing selection controls:
  - presets: `full-wiki`, `tools-only`, `non-tools-only`
  - parts via `--sections`: `cover`, `about-installation`, `technical-specs`, `menu`, `toc`, `tool-pages`, `special-thanks`, `contacts`
  - tool filtering via `--tool-category`
- The existing `buildPDF/make_wiki_pdf` and `buildPDF/make_tool_pages_pdf` scripts remain in the repo as internal builder plumbing behind `./export_pdf`.
- Output defaults to repo-local `output/pdf/`, with `--output-dir` available as an override.
- Generated filenames follow `YYYYMMDD_HHMMSS__NukeSurvivalToolkit_Documentation_Release_vX.Y.Z[__suffix].pdf`.
- The older `documentation/scripts/build_pdf.sh` path remains useful for full-book experiments; section-by-section work also uses `./buildPDF/make_wiki_pdf`.

### Non-tool sections (`non-tool-sections`)

- One merged PDF of **every non-tool section** (cover through contact, no tool pages) is built with **`./buildPDF/make_wiki_pdf non-tool-sections`** (implemented as `build_non_tool_sections()` in `buildPDF/make_wiki_pdf`). This is separate from the default **`./export_pdf`** flow (presets, tool pages, Tool Index, cache, compression); use it when you need that merged slice for template or layout review.
- It merges **in this order** (see `pdfunite` sequence in `build_non_tool_sections`):
  - `cover`
  - `about-installation`
  - `technical-details`
  - `menu`
  - `special-thanks`
  - `contact`
- The about-installation page uses the dedicated approved shell template:
  - `documentation/templates/about-installation.html`
- The about-installation code block uses the repo-local JetBrains Mono asset and the replacement path string is intentionally red to warn users to change it.
- The about-installation page acts as the source-of-truth front-matter shell, while its content comes from:
  - `about-installation` → `documentation/docs/intro.md`
- The content slices after the about-installation page build from the wiki markdown pages instead of standalone content templates:
  - `technical-details` → `documentation/docs/techSpecs.md`
  - `menu` → `documentation/docs/menus.md`
  - `special-thanks` → `documentation/docs/special-thanks.md`
  - `contact` → `documentation/docs/contact.md`
- Individual section targets are rendered contextually from the combined subset and then extracted back out, so the current local review pages keep a consistent sequence.
- `technical-details` paginates as flowing content inside the approved shell, using two invisible context pages so Chrome lays it out as if it begins on page 3 before the real pages are extracted back out.
- Final visible page numbers are not trusted to template HTML alone. Section PDFs are produced with `documentation/scripts/stamp_pdf_page_numbers.py` via `stamp_page_numbers()` in `make_wiki_pdf` where each builder enables it. The **`non-tool-sections`** target **`pdfunite`s those section PDFs** and does **not** run a second pass over the merged file; **`full-wiki`** and **`./export_pdf`** stamp the **combined** PDF after merge (and run further TOC/link steps as documented below).

### Current architecture

- The repo's strongest proven path for **browsing** the wiki locally is the offline HTML build: `mkdocs build -f mkdocs.offline.yml`.
- For **PDF**, the user-facing command is **`./export_pdf`** (`buildPDF/export_pdf`). It orchestrates section and tool bundles, merge, stamping, optional TOC links, Ghostscript compression, and caching—on top of the same Playwright/MkDocs/`pypdf`/Poppler primitives used by `make_wiki_pdf` and `make_tool_pages_pdf`.
- `documentation/mkdocs.pdf.yml` remains useful as the merged-HTML source for PDF slice extraction. **Shipped PDFs use browser/Playwright printing, not WeasyPrint, as the final renderer** (why: see [PDF pipeline history](archive/pdf-pipeline-history.md)).
- The proven **internal** render/assemble chain for PDF slices and merged books is:
  - MkDocs merged HTML (per pipeline step)
  - Playwright/Chrome (or equivalent) print to PDF
  - `pypdf` page-number stamping where applicable
  - Poppler **`pdfseparate` / `pdfunite`** (and related tooling) for extraction and assembly

### Operational notes

- Treat `documentation/mkdocs.offline.yml` as the stable local HTML build config; edit sidebar structure only in `documentation/mkdocs.yml`.
- Run direct MkDocs offline commands from `documentation/` when possible so the privacy-plugin cache stays under `documentation/.cache/`; running those commands from the repo root can create an extra root `.cache/` directory.
- Rebuild and inspect HTML in a real browser before assuming a PDF problem is caused by markdown content.
- Prefer temp directories for PDF diagnostics; do not generate fallback image assets into the repo.
- Generated PDF test builds should remain local/temporary artifacts and should not be committed.
- The tracked `documentation/NukeSurvivalToolkit_Documentation_Release_v2.2.0.pdf` file is the original reference PDF, not a generated test iteration.
- The combined non-tool review target is **`non-tool-sections`**, which assembles cover, about-installation, Technical Details, Menus, Special Thanks, and Contact into one local review PDF.
- The current merged full-book target is `full-wiki`, which preserves the approved main-page build as truth and inserts the separately rendered tool-pages PDF between the front main pages and the end matter.
- `./buildPDF/make_wiki_pdf full-wiki --category <slug>` now supports reduced TOC/layout runs while keeping the front matter and end matter in the build.
- `make_wiki_pdf` currently depends on:
  - Playwright-capable Python
  - `pypdf`
  - Ghostscript for the default `./export_pdf` compressed sibling output
  - Poppler CLI tools `pdfinfo`, `pdfseparate`, and `pdfunite`

### Merged PDF assembly

- `make_tool_pages_pdf` is intentionally tool-only again. It should not re-render `Home`, `Intro`, `Tech Specs`, `Menus`, `Special Thanks`, or `Contact`.
- `make_tool_pages_pdf tool-pages` remains the review path for tool pages and still accepts repeated `--category` flags for limited subset builds.
- `make_tool_pages_pdf` now has an internal `--no-page-numbers` mode so `make_wiki_pdf` can reuse the tool-pages build during merged assembly without baking in an intermediate numbering pass.
- `make_wiki_pdf full-wiki` now assembles the final merged PDF as:
  - `cover`
  - `about-installation`
  - `technical-details`
  - `menu`
  - generated `Tool Index`
  - all tool pages from `make_tool_pages_pdf`
  - `special-thanks`
  - `contact`
- The merged `full-wiki` flow stamps page numbers once, after merge, so the final numbering belongs to the combined result rather than the per-section sequence used by **`non-tool-sections`**.
- The generated `Tool Index` is built from the MkDocs nav plus the first H1 from each tool markdown page. The script resolves the actual destination pages from the rendered tool-pages PDF using `pdftotext`, then rerenders the TOC until its own page count stabilizes.
- After the final merged PDF is stamped, `make_wiki_pdf` invokes `documentation/scripts/add_pdf_toc_links.py` (via `add_toc_links_and_outline()`) to inject clickable TOC rectangles and PDF bookmark-outline entries.
- `./export_pdf` now keeps that normal output and, by default, also writes a `__compressed.pdf` sibling via Ghostscript. The current recommended preset is tuned around `128 dpi` color/gray image downsampling with forced JPEG recompression. For mixed/full exports, the compressed sibling is generated from the stamped PDF and then receives its own TOC-link and bookmark injection pass so navigation survives the lossy rewrite.
- `./export_pdf` now also maintains a local bundle cache under `.cache/pdf-export/` for unstamped front-matter sections and per-category tool PDFs. The public flags are:
  - `--no-cache`
  - `--refresh-cache`
- Tool-category exports now prune the MkDocs nav before `mkdocs build` and render category bundles in nav order, rather than always building the full tool corpus and trimming it afterward.
- Back matter (`Special Thanks`, `Contact`) must stay out of the tool-group TOC scan; otherwise the TOC resolver will incorrectly search for those titles inside the tool-pages PDF.

### Common Validation Checks

Build validation:

```bash
cd documentation
mkdocs build
```

Offline validation:

```bash
cd documentation
mkdocs build -f mkdocs.offline.yml
```

Markdown list-spacing validation (MD032):

```bash
cat > /tmp/md032-only.json <<'JSON'
{
  "default": false,
  "MD032": true
}
JSON

npx --yes markdownlint-cli "documentation/docs/**/*.md" -c /tmp/md032-only.json
```

Rendered HTML check for collapsed list/paragraph patterns:

```bash
rg -n --pcre2 -U '<p>[^<]*\n\s*[0-9]+\.\s|<p>[^<]*\n\s*[-*]\s' documentation/site
```

## Content Editing Guidance

- Keep markdown list blocks separated by blank lines to avoid list rendering issues in generated HTML.
- Prefer explicit image placement for tool input/output sections when image-to-bullet mapping matters.
- Rebuild and spot-check affected pages in browser after structural markdown edits.
