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

When available, download the latest release asset ZIP from the Releases page, unzip it anywhere on your machine, and open `site/index.html` (or serve the `site/` folder locally) to browse the full wiki offline.

Releases:

<https://github.com/CreativeLyons/NukeSurvivalToolkit_Wiki/releases>

## C. Offline PDF Build (Local, Not Versioned)

The main PDF entrypoint for this repo is the root-level Python script `./make_wiki_pdf`.
Its purpose is to generate the printable PDF documentation from the wiki source, first as approved section builds and eventually as the complete assembled PDF book.

Current implemented targets:

- `cover`
- `page2`
- `technical-details`
- `menu`
- `contact`
- `special-thanks`
- `pages-1-2`
- `pages-1-5`
- `full-so-far`

The content-backed slice targets now render from the wiki markdown source (`techSpecs.md`, `menus.md`, `special-thanks.md`, `contact.md`) so the wiki and the printable subset builds stay aligned while preserving the approved PDF shell. `page2` remains a dedicated front-matter template.

The finished review PDFs now receive page numbers in one final stamping pass, so the cover and interior pages share the same numbering position.

Requirements:

- Google Chrome installed locally
- A Python interpreter with `playwright` available
- Python packages from `documentation/requirements-pdf.txt` (includes `pypdf` for final page-number stamping)
- Poppler CLI tools `pdfinfo`, `pdfseparate`, and `pdfunite` available on `PATH`

Generated PDFs are local build artifacts for inspection and should not be committed.

## D. Offline Wiki (PDF Reference)

For the original offline reference version of the documentation, use the PDF:

- [NukeSurvivalToolkit_Documentation_Release_v2.1.0.pdf](documentation/NukeSurvivalToolkit_Documentation_Release_v2.1.0.pdf)


## Changelog

Project change history is tracked in `CHANGELOG.md`.
