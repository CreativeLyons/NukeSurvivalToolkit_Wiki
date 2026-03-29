# NST Wiki User Guide

This guide covers the practical workflows for previewing, building, publishing, and exporting the Nuke Survival Toolkit wiki.

## Choose The Right Build

| Goal | Use this | Main file or command |
| --- | --- | --- |
| Preview or publish the public website | Online MkDocs build | `documentation/mkdocs.yml` |
| Create a local HTML wiki that works offline | Offline MkDocs build | `documentation/mkdocs.offline.yml` |
| Create a local PDF reference build | PDF export workflow | `./export_pdf` |

## Requirements

### HTML wiki builds

- Python 3
- `mkdocs-material`

### PDF export builds

- Google Chrome installed locally
- A Python environment with `playwright`
- Python packages from `documentation/requirements-pdf.txt`
- Ghostscript on `PATH` for the default compressed sibling PDF
- Poppler CLI tools on `PATH`: `pdfinfo`, `pdfseparate`, and `pdfunite`

## Maintain And Publish The Online Wiki

Edit the wiki source under `documentation/docs/`.

Preview the public-site build locally:

```bash
cd documentation
mkdocs serve -f mkdocs.yml -a 127.0.0.1:8010
```

Build the public-site output once without serving:

```bash
cd documentation
mkdocs build -f mkdocs.yml
```

When changes under `documentation/**` are pushed to `main` or `master`, `.github/workflows/mkdocs.yml` rebuilds the site and deploys `documentation/site/` to GitHub Pages.

## Build The Offline HTML Wiki

Use the offline config when you want a local copy that behaves correctly from disk or inside a downloadable zip.

Build:

```bash
cd documentation
mkdocs build -f mkdocs.offline.yml
```

Preview locally with the offline config:

```bash
cd documentation
mkdocs serve -f mkdocs.offline.yml -a 127.0.0.1:8010
```

The generated site is written to `documentation/site/`.

### Offline search and opening files from disk (`file://`)

The offline build includes `search/search_index.js` and the iframe-worker shim so search can work without a network. **Browsers still limit `file://` pages:** Chrome in particular may block or partially run local scripts and workers, so search can stay on “Initializing search” or look broken even when the files are present.

**Reliable way to verify search (and match how the online site behaves over HTTP):** serve the built folder over HTTP, for example:

```bash
cd documentation/site
python3 -m http.server 8765
```

Then open `http://127.0.0.1:8765` in Chrome. Alternatively use `mkdocs serve -f mkdocs.offline.yml` (see above), which serves the same config over HTTP.

**Avoid comparing** the online build and offline build **only** by double-clicking `index.html` in both output folders: the online build does not ship `search_index.js`, and `file://` restrictions apply differently in each case. Use HTTP for both, or compare the public site on GitHub Pages to an offline build served locally.

If you are opening a prebuilt release zip instead of building from source, unzip it and open `NST_Documentation/index.html`, or use a local HTTP server in the unzipped folder for full search.

## What The YAML Files Do

- `documentation/mkdocs.yml`: online/public configuration used by GitHub Pages. Sidebar navigation is edited only in this file.
- `documentation/mkdocs.offline.yml`: offline/local-file configuration used for local HTML builds and release zips. It inherits `mkdocs.yml` and adds offline-only plugins and theme settings (same sidebar as the online build).
- `documentation/mkdocs.pdf.yml`: merged HTML source used by the PDF pipeline. This is supporting infrastructure; the public entrypoint is still `./export_pdf`.

The PDF implementations live under `buildPDF/` (`export_pdf`, `make_wiki_pdf`, `make_tool_pages_pdf`). The `./export_pdf` file at the repository root is a small launcher that runs `buildPDF/export_pdf` so you do not need to type the folder path for normal exports.

## Export The Offline PDF

Use `./export_pdf` from the repository root. The default export mode is `full-wiki`.

Basic export:

```bash
./export_pdf
```

Export only tool pages from one category:

```bash
./export_pdf tools-only --tool-category draw
```

Export without the default compressed sibling:

```bash
./export_pdf --no-compress
```

Write output somewhere else:

```bash
./export_pdf --output-dir /tmp/nst-pdf-checks
```

By default, finished PDFs go to `output/pdf/` and use release-style filenames with a timestamp.

The export keeps the normal PDF and, unless disabled, also writes a `__compressed.pdf` sibling. Generated PDFs are local build artifacts and should not be committed.

## Offline HTML vs Offline PDF

Use the offline HTML build when you want the full interactive wiki experience with sidebar navigation, search, and direct page browsing.

Use the PDF export when you need a single portable document for reference, review, printing, or sharing outside the website flow.

## Repo Pointers

- Wiki source pages: `documentation/docs/`
- Public Pages workflow: `.github/workflows/mkdocs.yml`
- Contributor notes and PDF internals: `documentation/DEVELOPMENT.md`
