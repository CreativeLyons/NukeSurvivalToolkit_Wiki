# PDF pipeline — history and experiments

Tracked lab notebook for the NST wiki PDF export work: renderer decisions, debugging sessions, dated benchmarks, and pointers to optional local handoff files.

**Operational reference (current behavior):** see `documentation/DEVELOPMENT.md`.  
**User-facing usage (`./export_pdf`, flags):** see `documentation/USER_GUIDE.md`.

This file is not under `documentation/docs/` and is not part of the published MkDocs site.

---

## Verified renderer behavior

- `mkdocs-with-pdf` + WeasyPrint can build a merged HTML document containing all later chapters and end matter.
- The resulting WeasyPrint PDF truncates around `Draw/AutoFlare` in long renders.
- The same merged HTML, when printed with Chrome/Playwright, includes the later pages that WeasyPrint drops.
- `Google Chrome.app` and the `playwright` CLI are already available locally, so a browser-renderer path is viable without adding dependencies.

## Important debugging conclusions

- The truncation is not caused solely by:
  - `documentation/docs/css/pdf.css`
  - `documentation/hooks/pdf_preprocess.py`
  - `draw/bokeh-builder.md` on its own
  - `BokehBuilder` images
- The `AutoFlare` page image is a confirmed trigger for the WeasyPrint truncation in the long combined document.
- Removing only that image in a temp diagnostic build allowed `AutoFlare` text and `BokehBuilder` to appear.
- Converting that image to PNG did not fix the issue, so the problem is not simply WebP format support.

## Recommended export direction

- Build local HTML with MkDocs first.
- Render the final PDF with a browser engine (preferably Playwright using the Chrome channel).
- Tune browser print CSS rather than continuing to chase WeasyPrint-specific layout failures.

## Browser-renderer results (March 5, 2026)

- `documentation/scripts/build_pdf.sh` captures the merged HTML output and hands that HTML to a Playwright + Chrome renderer.
- The first full browser-rendered build completed successfully on March 5, 2026.
- Output file: `documentation/NukeSurvivalToolkit_Documentation_Release_v2.2.0.pdf`
- Resulting browser-rendered PDF stats:
  - 466 pages
  - A4
  - 164.6 MB
- The browser-rendered PDF includes:
  - page 1 splash/cover image
  - `AutoFlare` on page 44
  - `BokehBuilder` on page 45
  - final `About / Special Thanks / Contact` page at page 466
- This run confirmed the renderer pivot addressed the truncation issue.
- The cover-image sharpness issue was traced to `documentation/scripts/build_pdf.sh`, which was converting the splash image to a temp PNG at only `640px` width before render.
- Keeping the temp cover asset at native source resolution allows the browser-rendered PDF to embed the cover image at `1280x720` instead of `640x360`, which materially improves sharpness.
- The committed PDF cover asset lives at `documentation/docs/img/pdf/NukeSurvivalToolkit_Splashpage_cover.jpg`.
- Both `documentation/mkdocs.pdf.yml` and `documentation/scripts/build_pdf.sh` use that JPEG cover asset for page 1 so the build no longer depends on regenerating the cover from the softer WebP source.

## Remaining QA notes (dated snapshot)

At the time of the March 2026 browser-render pivot, remaining issues were quality and pagination rather than completeness:

- Page count was still far above the 305-page reference.
- Cover typography and footer placement still differed noticeably from v2.1.0.
- Shared-page behavior and whitespace needed more tuning under browser print CSS.

## Verified full-book TOC run (March 12, 2026)

- Command: `./buildPDF/make_wiki_pdf full-wiki --artifact-version 20260312`
- Output: `459` pages
- Size: `166.8 MB`
- Wall time: `4 min 16.90 sec`
- Outline items: `260`
- Link annotations: `948`

## Nav incident: `bm-lightwrap` → `bm-optical-lightwrap`

A stale nav reference to `filter/bm-lightwrap.md` blocked an early full TOC run. The MkDocs configs were updated to point to `filter/bm-optical-lightwrap.md`, matching the renamed markdown file.

## Optional local handoff files (`.ai/`, not tracked)

The repository `.gitignore` excludes `.ai/`. If you have that folder locally from earlier work, it may contain session-specific prompts and status reports (for example `20260312_004439_export-pdf_HANDOFF.md`). Those files are **not** in a fresh clone; treat them as optional local context, not source of truth.

## Takeover notes (2026-03)

- Markdown-driven content sourcing is in place for `technical-details`, `menu`, `special-thanks`, and `contact`.
- Natural-flow `technical-details` pagination and universal post-stamped page numbering are in place for the approved subset workflow.
- Follow-up work was to extend the same approach to later section groups without changing the approved page shells.
