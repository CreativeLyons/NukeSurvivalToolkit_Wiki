# Development Notes

## Repository Layout

- `documentation/docs/`: markdown pages and static assets used by MkDocs.
- `documentation/mkdocs.yml`: online GitHub Pages configuration.
- `documentation/mkdocs.offline.yml`: offline ZIP/local-file configuration.
- `documentation/site/`: local build output (ignored in git).
- `.github/workflows/mkdocs.yml`: GitHub Pages build/deploy workflow.

## Local Workflow

### Build

```bash
cd documentation
mkdocs build
```

Offline build:

```bash
cd documentation
mkdocs build -f mkdocs.offline.yml
```

### Serve

```bash
cd documentation
mkdocs serve -a 127.0.0.1:8010
```

Offline serve:

```bash
cd documentation
mkdocs serve -f mkdocs.offline.yml -a 127.0.0.1:8010
```

## PDF Export Findings (2026-03-05)

### Main entrypoint

- The main repo-visible PDF entrypoint is `./export_pdf` at the repository root.
- `./export_pdf` defaults to the `full-wiki` preset and exposes the supported user-facing selection controls:
  - presets: `full-wiki`, `tools-only`, `non-tools-only`
  - parts via `--sections`: `cover`, `about-installation`, `technical-specs`, `menu`, `toc`, `tool-pages`, `special-thanks`, `contacts`
  - tool filtering via `--tool-category`
- The existing `./make_wiki_pdf` and `./make_tool_pages_pdf` scripts remain in the repo as internal builder plumbing behind `./export_pdf`.
- Output defaults to repo-local `output/pdf/`, with `--output-dir` available as an override.
- Generated filenames follow `YYYYMMDD_HHMMSS__NukeSurvivalToolkit_Documentation_Release_vX.Y.Z[__suffix].pdf`.
- The older `documentation/scripts/build_pdf.sh` path remains useful for full-book experiments, but the section-by-section workflow should be built out through `./make_wiki_pdf`.

### Current approved slice

- The current approved subset is built through `./make_wiki_pdf full-so-far`.
- It assembles:
  - `cover`
  - `about-installation`
  - `technical-details`
  - `menu`
  - `special-thanks`
  - `contact`
- The about-installation page uses the dedicated approved shell template:
  - `/Users/tonylyons/Dropbox/Public/GitHub/NukeSurvivalToolkit_Wiki/documentation/templates/about-installation.html`
- The about-installation code block uses the repo-local JetBrains Mono asset and the replacement path string is intentionally red to warn users to change it.
- The about-installation page now acts as the source-of-truth front-matter shell, while its content comes from:
  - `about-installation` -> `documentation/docs/intro.md`
- The content slices after the about-installation page now build from the wiki markdown pages instead of standalone content templates:
  - `technical-details` -> `documentation/docs/techSpecs.md`
  - `menu` -> `documentation/docs/menus.md`
  - `special-thanks` -> `documentation/docs/special-thanks.md`
  - `contact` -> `documentation/docs/contact.md`
- Individual section targets are rendered contextually from the combined subset and then extracted back out, so the current local review pages keep a consistent sequence.
- The older `page2` target name still works as a legacy alias, but `about-installation` is now the canonical name.
- `About` is no longer part of the live nav, and the old `documentation/docs/about.md` page has been removed.
- `technical-details` now paginates as flowing content inside the approved shell, using two invisible context pages so Chrome lays it out as if it begins on page 3 before the real pages are extracted back out.
- Final visible page numbers are no longer trusted to template HTML. The finished PDFs are stamped afterward by:
  - `/Users/tonylyons/Dropbox/Public/GitHub/NukeSurvivalToolkit_Wiki/documentation/scripts/stamp_pdf_page_numbers.py`
- The legacy cover HTML page number is hidden in:
  - `/Users/tonylyons/Dropbox/Public/GitHub/NukeSurvivalToolkit_Wiki/documentation/docs/css/pdf-browser.css`
- This means the cover and interior pages all share one post-render page-number position.

### Current state

- The repo's strongest proven path is still the offline/local HTML build:
  - `mkdocs build -f mkdocs.offline.yml`
- `mkdocs.pdf.yml` is still useful as the merged-HTML source for PDF slice extraction, but WeasyPrint is not reliable as the final renderer for this document.
- The current proven PDF path is:
  - MkDocs merged HTML
  - Playwright/Chrome render
  - `pypdf` page-number stamping
  - `pdfseparate` / `pdfunite` extraction and assembly

### Verified renderer behavior

- `mkdocs-with-pdf` + WeasyPrint can build a merged HTML document containing all later chapters and end matter.
- The resulting WeasyPrint PDF truncates around `Draw/AutoFlare` in long renders.
- The same merged HTML, when printed with Chrome/Playwright, includes the later pages that WeasyPrint drops.
- `Google Chrome.app` and the `playwright` CLI are already available locally, so a browser-renderer path is viable without adding dependencies.

### Important debugging conclusions

- The truncation is not caused solely by:
  - `documentation/docs/css/pdf.css`
  - `documentation/hooks/pdf_preprocess.py`
  - `draw/bokeh-builder.md` on its own
  - `BokehBuilder` images
- The `AutoFlare` page image is a confirmed trigger for the WeasyPrint truncation in the long combined document.
- Removing only that image in a temp diagnostic build allowed `AutoFlare` text and `BokehBuilder` to appear.
- Converting that image to PNG did not fix the issue, so the problem is not simply WebP format support.

### Recommended export direction

- Build local HTML with MkDocs first.
- Render the final PDF with a browser engine (preferably Playwright using the Chrome channel).
- Tune browser print CSS rather than continuing to chase WeasyPrint-specific layout failures.

### Browser-renderer results now verified

- `documentation/scripts/build_pdf.sh` now captures the merged HTML output and hands that HTML to a Playwright + Chrome renderer.
- The first full browser-rendered build completed successfully on March 5, 2026.
- Output file: `documentation/NukeSurvivalToolkit_Documentation_Release_v2.2.0.pdf`
- Resulting browser-rendered PDF stats:
  - 466 pages
  - A4
  - 164.6 MB
- The browser-rendered PDF now includes:
  - page 1 splash/cover image
  - `AutoFlare` on page 44
  - `BokehBuilder` on page 45
  - final `About / Special Thanks / Contact` page at page 466
- This confirms the renderer pivot fixed the truncation bug.
- The cover-image sharpness issue was traced to `documentation/scripts/build_pdf.sh`, which was converting the splash image to a temp PNG at only `640px` width before render.
- Keeping the temp cover asset at native source resolution allows the browser-rendered PDF to embed the cover image at `1280x720` instead of `640x360`, which materially improves sharpness.
- The committed PDF cover asset now lives at `documentation/docs/img/pdf/NukeSurvivalToolkit_Splashpage_cover.jpg`.
- Both `documentation/mkdocs.pdf.yml` and `documentation/scripts/build_pdf.sh` now use that JPEG cover asset for page 1 so the build no longer depends on regenerating the cover from the softer WebP source.
- Remaining issues are now quality/pagination issues rather than completeness:
  - page count is still far above the 305-page reference
  - cover typography and footer placement still differ noticeably from v2.1.0
  - shared-page behavior and whitespace need more tuning under browser print CSS

### Operational notes

- Treat `documentation/mkdocs.offline.yml` as the stable local HTML build config.
- Run direct MkDocs offline commands from `documentation/` when possible so the privacy-plugin cache stays under `documentation/.cache/`; running those commands from the repo root can create an extra root `.cache/` directory.
- Rebuild and inspect HTML in a real browser before assuming a PDF problem is caused by markdown content.
- Prefer temp directories for PDF diagnostics; do not generate fallback image assets into the repo.
- Generated PDF test builds should remain local/temporary artifacts and should not be committed.
- The tracked `documentation/NukeSurvivalToolkit_Documentation_Release_v2.1.0.pdf` file is the original reference PDF, not a generated test iteration.
- The current combined review target is `full-so-far`, which assembles cover, page 2, Technical Details, Menus, Special Thanks, and Contact into one local review PDF.
- The current merged full-book target is `full-wiki`, which preserves the approved main-page build as truth and inserts the separately rendered tool-pages PDF between the front main pages and the end matter.
- `./make_wiki_pdf full-wiki --category <slug>` now supports reduced TOC/layout runs while keeping the front matter and end matter in the build.
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
- The merged `full-wiki` flow stamps page numbers once, after merge, so the final numbering belongs to the combined result rather than the old `full-so-far` sequence.
- The generated `Tool Index` is built from the MkDocs nav plus the first H1 from each tool markdown page. The script resolves the actual destination pages from the rendered tool-pages PDF using `pdftotext`, then rerenders the TOC until its own page count stabilizes.
- After the final merged PDF is stamped, `make_wiki_pdf` runs:
  - `/Users/tonylyons/Dropbox/Public/GitHub/NukeSurvivalToolkit_Wiki/documentation/scripts/add_pdf_toc_links.py`
  to inject clickable TOC rectangles and PDF bookmark-outline entries.
- `./export_pdf` now keeps that normal output and, by default, also writes a `__compressed.pdf` sibling via Ghostscript. The current recommended preset is tuned around `128 dpi` color/gray image downsampling with forced JPEG recompression. For mixed/full exports, the compressed sibling is generated from the stamped PDF and then receives its own TOC-link and bookmark injection pass so navigation survives the lossy rewrite.
- `./export_pdf` now also maintains a local bundle cache under `.cache/pdf-export/` for unstamped front-matter sections and per-category tool PDFs. The public flags are:
  - `--no-cache`
  - `--refresh-cache`
- Tool-category exports now prune the MkDocs nav before `mkdocs build` and render category bundles in nav order, rather than always building the full tool corpus and trimming it afterward.
- Verified full-book TOC run on March 12, 2026:
  - `./make_wiki_pdf full-wiki --artifact-version 20260312`
  - output: `459` pages
  - size: `166.8 MB`
  - wall time: `4 min 16.90 sec`
  - outline items: `260`
  - link annotations: `948`
- A stale nav reference to `filter/bm-lightwrap.md` blocked the first full TOC run. The MkDocs configs now point to `filter/bm-optical-lightwrap.md`, which matches the renamed markdown file.
- Back matter (`Special Thanks`, `Contact`) must stay out of the tool-group TOC scan; otherwise the TOC resolver will incorrectly search for those titles inside the tool-pages PDF.

### AI Handoff Files (2026-03-12)

- Current export-PDF handoff prompt:
  - `/Users/tonylyons/Dropbox/Public/GitHub/NukeSurvivalToolkit_Wiki/.ai/20260312_004439_export-pdf_HANDOFF.md`
- Current export-PDF factual status report:
  - `/Users/tonylyons/Dropbox/Public/GitHub/NukeSurvivalToolkit_Wiki/.ai/20260312_004439_export-pdf_STATUS_REPORT.md`
- Previous general handoff prompt:
  - `/Users/tonylyons/Dropbox/Public/GitHub/NukeSurvivalToolkit_Wiki/.ai/20260306_HANDOFF.md`
- Previous general factual status report:
  - `/Users/tonylyons/Dropbox/Public/GitHub/NukeSurvivalToolkit_Wiki/.ai/20260306_STATUS_REPORT.md`

Use the 2026-03-12 export-PDF handoff files first when continuing the current branch-integration and TOC-transplant work. Use the 2026-03-06 files as older background on the earlier markdown-backed PDF architecture shift.

Current takeover priority:
- markdown-driven content sourcing is now in place for `technical-details`, `menu`, `special-thanks`, and `contact`
- natural-flow technical-details pagination and universal post-stamped page numbering are now in place for the approved subset workflow
- the next agent should extend the same approach to later section groups without changing the approved page shells

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
