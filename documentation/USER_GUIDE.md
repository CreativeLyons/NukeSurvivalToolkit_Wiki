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

Use the offline config when you want a local copy that behaves correctly from disk or inside a downloadable Release zip.

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

Run `./export_pdf` from the repository root (it calls `buildPDF/export_pdf`). For the exact argparse text, run:

```bash
./export_pdf --help
```

### Presets (positional `mode`)

Optional first argument; default is **`full-wiki`**.

| Mode | What it includes |
|------|------------------|
| `full-wiki` | All sections below, Tool Index (`toc`), and all tool pages. |
| `tools-only` | Tool pages only (no front/back matter). |
| `non-tools-only` | Cover, about, technical specs, menus, special thanks, contacts — no tool pages or Tool Index. |

### Section names (`--sections`)

Use **`--sections`** one or more times. Each value can be a comma-separated list. Valid **part** names:

`cover`, `about-installation`, `technical-specs`, `menu`, `toc`, `tool-pages`, `special-thanks`, `contacts`

- Omit `--sections` to use the preset’s default list.
- Use **`none`** in a `--sections` value to ignore the preset and build only what you list next (for example: `--sections none --sections cover,menu,tool-pages`).
- **`all`** or **`*`** expands to every part above.

The exporter also accepts common aliases (for example `technical` → `technical-specs`, `tools` → `tool-pages`, `contact` → `contacts`). Unknown names are rejected with an error that lists valid parts.

**Rules:**

- If you include **`toc`** (Tool Index), you must also include **`tool-pages`**.
- **`--tool-category`** only applies when **`tool-pages`** is part of the export.

### Tool categories (`--tool-category`)

Limit tool pages to one or more wiki category folders (repeat the flag or use comma-separated values). Examples: `draw`, `filter`, `transform`, `3d`, `cg`, `curves`, `utilities`, `color`. Names match the documentation directory slugs under `documentation/docs/`.

### Other flags

| Flag | Purpose |
|------|---------|
| `--version STRING` | Release label on the cover and in the output filename. Default matches `DEFAULT_VERSION` in `buildPDF/make_wiki_pdf` (currently `v2.2.0`). |
| `--output-dir PATH` | Write PDFs here instead of the repo’s `output/pdf/`. Relative paths are resolved from the current working directory. |
| `--no-compress` | Skip the Ghostscript pass; only the main PDF is written (no `__compressed.pdf` sibling). Use if `gs` is not installed — the tool will otherwise require Ghostscript for compression. |
| `--open` | After a successful build, open the compressed PDF if one was produced, otherwise the main PDF. |
| `--verbose` | Print output from the underlying renderer commands. |
| `--no-cache` | Disable the local PDF bundle cache under `.cache/pdf-export/` for this run. |
| `--refresh-cache` | Rebuild cached section/tool bundles before assembling the export. |

### Output location and artifacts

By default, PDFs go to **`output/pdf/`** with a timestamped, release-style basename. Custom exports add suffix segments to the filename so the preset and scope are obvious.

The export always produces the main PDF. Unless **`--no-compress`** is set, it also writes a **`__compressed.pdf`** sibling (smaller file; requires Ghostscript on `PATH`). **Do not commit** these outputs — they are local build artifacts.

### Examples

```bash
# Full wiki (default preset)
./export_pdf
```

```bash
# Tool pages for one category only
./export_pdf tools-only --tool-category draw
```

```bash
# Multiple tool categories
./export_pdf tools-only --tool-category draw,filter
```

```bash
# Non-tool sections only (preset)
./export_pdf non-tools-only
```

```bash
# Custom section list (clear preset, then choose parts)
./export_pdf --sections none --sections cover,about-installation,technical-specs,menu,special-thanks,contacts
```

```bash
# Tool pages + Tool Index for one category
./export_pdf --sections tool-pages,toc --tool-category color
```

```bash
./export_pdf --no-compress
```

```bash
./export_pdf --output-dir /tmp/nst-pdf-checks
```

```bash
./export_pdf --version v2.3.0 --open --verbose
```

## Offline HTML vs Offline PDF

Use the offline HTML build when you want the full interactive wiki experience with sidebar navigation, search, and direct page browsing.

Use the PDF export when you need a single portable document for reference, review, printing, or sharing outside the website flow.

## Repo Pointers

- Wiki source pages: `documentation/docs/`
- Public Pages workflow: `.github/workflows/mkdocs.yml`
- Contributor notes and PDF internals: `documentation/DEVELOPMENT.md`
