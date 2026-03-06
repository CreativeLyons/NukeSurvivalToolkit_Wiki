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

- The main repo-visible PDF entrypoint is `./make_wiki_pdf` at the repository root.
- The script is intentionally target-based so each approved section can be rebuilt without touching the rest of the book.
- Current implemented targets:
  - `cover`
  - `page2`
  - `technical-details`
  - `special-thanks`
  - `pages-1-2`
  - `pages-1-5`
  - `full-so-far`
- Output defaults to `/tmp/nst-wiki-pdf/`.
- The reviewed combined artifact naming scheme is `nst_wiki_vN.pdf`.
- The older `documentation/scripts/build_pdf.sh` path remains useful for full-book experiments, but the section-by-section workflow should be built out through `./make_wiki_pdf`.

### Current approved slice

- The current locked approved front-matter artifact is:
  - `/tmp/nst-wiki-pdf/nst_wiki_v7.pdf`
- It contains the approved cover plus the approved About + Installation page.
- Page 2 is rendered from the dedicated template:
  - `/Users/tonylyons/Dropbox/Public/GitHub/NukeSurvivalToolkit_Wiki/documentation/templates/page2.html`
- The page 2 code block uses the repo-local JetBrains Mono asset and the replacement path string is intentionally red to warn users to change it.
- Page 2 now acts as the source-of-truth interior shell for shared page margin, side padding, base typography, and link styling in the standalone interior-section templates.
- Special Thanks uses that shared page 2 shell directly.
- Technical Details uses the same shared page frame, while keeping denser content-specific typography so the fixed slice still fits reference pages 3-5.

### Current state

- The repo's strongest proven path is still the offline/local HTML build:
  - `mkdocs build -f mkdocs.offline.yml`
- The newer `mkdocs.pdf.yml` path can assemble the full merged HTML for PDF export, but WeasyPrint is not reliable as the final renderer for this document.

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
- Rebuild and inspect HTML in a real browser before assuming a PDF problem is caused by markdown content.
- Prefer temp directories for PDF diagnostics; do not generate fallback image assets into the repo.
- Generated PDF test builds should remain local/temporary artifacts and should not be committed.
- The tracked `documentation/NukeSurvivalToolkit_Documentation_Release_v2.1.0.pdf` file is the original reference PDF, not a generated test iteration.
- The current combined review target is `full-so-far`, which assembles cover, page 2, Technical Details, and Special Thanks into one local review PDF.

### AI Handoff Files (2026-03-06)

- Current handoff prompt for another agent:
  - `/Users/tonylyons/Dropbox/Public/GitHub/NukeSurvivalToolkit_Wiki/.ai/20260306_HANDOFF.md`
- Current factual status report:
  - `/Users/tonylyons/Dropbox/Public/GitHub/NukeSurvivalToolkit_Wiki/.ai/20260306_STATUS_REPORT.md`

Use those files as the first stop when handing this PDF work to another agent. They capture the current branch, the section-by-section `make_wiki_pdf` workflow, the user communication constraints, the locked page 1 + page 2 artifact, and the explicit boundary that Technical Details should not resume until the user says to continue.

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
