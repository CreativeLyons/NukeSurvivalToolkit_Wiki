# NukeSurvivalToolkit Wiki

Live Online Wiki: <https://creativelyons.github.io/NukeSurvivalToolkit_Wiki/>

[![Nuke Survival Toolkit Documentation Banner](documentation/docs/img/nst-wiki-large.jpeg)](https://creativelyons.github.io/NukeSurvivalToolkit_Wiki/)

## Repository Layout

This repository contains the source and deployment setup for the NST wiki.

- Docs source: `documentation/docs/`
- MkDocs online config (GitHub Pages): `documentation/mkdocs.yml`
- MkDocs offline config (ZIP/local file mode): `documentation/mkdocs.offline.yml`
- Local build output: `documentation/site/` (ignored)
- CI deploy workflow: `.github/workflows/mkdocs.yml`

## Deployment

Deployment is handled by GitHub Actions via `.github/workflows/mkdocs.yml` when changes are pushed to `main` under `documentation/**`.
CI builds with `documentation/mkdocs.yml` (online config).

## Options for Offline Documentation:

## A. Build From Source (Offline Wiki)

Requirements:

- Python 3.x
- `mkdocs`
- `mkdocs-material`

Build:

```bash
cd documentation
mkdocs build -f mkdocs.offline.yml
```

Serve locally:

```bash
cd documentation
mkdocs serve -f mkdocs.offline.yml -a 127.0.0.1:8010
```

Open:

<http://127.0.0.1:8010/>

## B. Offline Wiki (Prebuilt ZIP Release Asset)

A prebuilt static wiki ZIP will be provided in GitHub Releases so users can run the documentation offline without building from source.

When available, download the latest release asset ZIP from the Releases page, unzip it anywhere on your machine, and open `NST_Documentation/index.html` (or serve the `NST_Documentation/` folder locally). Release zips use that top-level folder name to match bundles such as `NST_Documentation_Release_2.1.1.zip`. Local builds from source still output to `documentation/site/`.

Releases:

<https://github.com/CreativeLyons/NukeSurvivalToolkit_Wiki/releases>

## C. Offline PDF Build (Local, Not Versioned)

The public PDF entrypoint for this repo is the root-level script `./export_pdf`.
By default it exports the `full-wiki` preset. The older `./make_wiki_pdf` and `./make_tool_pages_pdf` scripts still exist, but they are now internal builder plumbing behind `./export_pdf` rather than the main user-facing interface.
Generated PDFs now go to repo-local `output/pdf/` by default. Use `--output-dir` to override that destination with a relative or absolute path.
`./export_pdf` now keeps the normal PDF output and, by default, also writes a Ghostscript-compressed sibling PDF with a `__compressed.pdf` suffix. The current recommended preset is tuned around `128 dpi` image downsampling plus forced JPEG recompression. Use `--no-compress` to skip that post-processing step.
`./export_pdf` also keeps a local bundle cache under `.cache/pdf-export/` so unchanged front-matter sections and tool categories can be reused across runs. Use `--no-cache` to bypass that cache for one export, or `--refresh-cache` to rebuild the selected cached bundles before assembly.

Common examples:

- `./export_pdf`
- `./export_pdf full-wiki`
- `./export_pdf tools-only`
- `./export_pdf non-tools-only`
- `./export_pdf --no-compress`
- `./export_pdf --refresh-cache`
- `./export_pdf --no-cache`
- `./export_pdf --sections cover,about-installation,technical-specs,menu`
- `./export_pdf --sections toc,tool-pages --tool-category draw --tool-category filter`
- `./export_pdf --sections cover,menu,toc,tool-pages,special-thanks,contacts --tool-category draw`
- `./export_pdf --output-dir /tmp/nst-pdf-checks`

Selection rules:

- Presets: `full-wiki`, `tools-only`, and `non-tools-only`.
- Export parts: `cover`, `about-installation`, `technical-specs`, `menu`, `toc`, `tool-pages`, `special-thanks`, and `contacts`.
- Use `--sections` to override the preset and build exactly the listed parts.
- `toc` is only valid when `tool-pages` is also selected.
- Use `--tool-category` to limit tool pages to specific category slugs such as `draw`, `filter`, `transform`, `3d`, `cg`, `curves`, or `utilities`.
- The local bundle cache lives under `.cache/pdf-export/` and is ignored by git.
- Filenames use `YYYYMMDD_HHMMSS__NukeSurvivalToolkit_Documentation_Release_vX.Y.Z[__suffix].pdf`.

The content-backed PDF sections render from the wiki markdown source (`intro.md`, `techSpecs.md`, `menus.md`, `special-thanks.md`, `contact.md`) so the wiki and printable outputs stay aligned while preserving the approved PDF shell. Finished PDFs receive page numbers in one final stamping pass, and mixed/full exports with tool pages also generate a clickable `Tool Index` plus PDF sidebar bookmarks.
When compression is enabled, mixed/full exports compress the stamped PDF first and then inject Tool Index links and bookmarks into the compressed sibling so the release-style output keeps working navigation.

Requirements:

- Google Chrome installed locally
- A Python interpreter with `playwright` available
- Python packages from `documentation/requirements-pdf.txt` (includes `pypdf` for final page-number stamping and Tool Index link injection)
- Ghostscript available on `PATH` for the default compression step
- Poppler CLI tools `pdfinfo`, `pdfseparate`, and `pdfunite` available on `PATH`

Generated PDFs are local build artifacts for inspection and should not be committed.

## D. Offline Wiki (PDF Reference)

For the original offline reference version of the documentation, use the PDF:

- [NukeSurvivalToolkit_Documentation_Release_v2.2.0.pdf](documentation/NukeSurvivalToolkit_Documentation_Release_v2.2.0.pdf)


## Changelog

Project change history is tracked in `CHANGELOG.md`.
