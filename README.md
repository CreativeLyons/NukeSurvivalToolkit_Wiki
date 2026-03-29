# NukeSurvivalToolkit Wiki

[![Nuke Survival Toolkit Documentation Banner](documentation/docs/img/nst-wiki-large.jpeg)](https://creativelyons.github.io/NukeSurvivalToolkit_Wiki/)

## About

The NST Wiki is the documentation site for the Nuke Survival Toolkit. It covers the current NST release, installation guidance, menu overview, and reference pages for `175+` tools.

**Toolkit (gizmos, menu, releases):** [NukeSurvivalToolkit_publicRelease on GitHub](https://github.com/CreativeLyons/NukeSurvivalToolkit_publicRelease)

`Current wiki release: v2.2.0`
`Read online:` <https://creativelyons.github.io/NukeSurvivalToolkit_Wiki/>
`This wiki on GitHub:` <https://github.com/CreativeLyons/NukeSurvivalToolkit_Wiki>
`Download release offline wiki zip files:` <https://github.com/CreativeLyons/NukeSurvivalToolkit_Wiki/releases>

If you just want the fastest path:

- Visit the live site, hosted on github pages: [NST Wiki Online](https://creativelyons.github.io/NukeSurvivalToolkit_Wiki/)
- To use it offline: download the latest NST_Documentation Release zip and open `NST_Documentation/index.html`

## What You Can Do Here

- Browse the NST wiki online through GitHub Pages.
- Use an offline HTML copy for local browsing.
- Build your own local copy: use the quick commands below
- Export a local PDF reference copy of the wiki.
- Export a PDF copy: run `./export_pdf`
- Edit and maintain the wiki source in this repository.


## Online, Offline HTML, And PDF

There are three ways to access the wiki:

- Online site: the public Github hosted website, best for normal reading and sharing links.
- Offline HTML: a local copy of the website, best when you want the see the wiki offline.
- PDF export: a single-file reference document, best for portable sharing, review, or printing.

## Quick Local Preview

If you are editing the wiki and want the normal website view, run:

```bash
cd documentation
mkdocs serve -f mkdocs.yml -a 127.0.0.1:8010
```

Then open `http://127.0.0.1:8010/`.

## Quick Offline Release Zip

If you are using a prebuilt release zip instead, unzip it and open `NST_Documentation/index.html`.

## Quick Offline Build

If you want a local offline HTML copy from source, run:

```bash
cd documentation
mkdocs build -f mkdocs.offline.yml
```

This writes the offline site to `documentation/site/`.


## Offline PDF Export

If you want a portable PDF version of the wiki, navigate into the repo folder and use:

```bash
./export_pdf
```

`./export_pdf` is the user-facing entry point; it delegates to the scripts under `buildPDF/` (Python commands and export tooling). By default the full wiki is written to `output/pdf/`.

For more PDF options, offline workflows, and step-by-step instructions, see the [User Guide](documentation/USER_GUIDE.md).

## More Help

- [User Guide](documentation/USER_GUIDE.md): step-by-step instructions for local preview, offline HTML, publishing, and PDF export.
- [Development Notes](documentation/DEVELOPMENT.md): contributor-facing repository structure, deployment behavior, and PDF internals.
- [AGENTS.md](AGENTS.md): map of DEVELOPMENT vs archived PDF history vs user guide (for assistants and advanced contributors).
- [Changelog](CHANGELOG.md): project history and current unreleased changes.

## How It's Hosted

The public wiki is hosted on GitHub Pages and built by GitHub Actions.

In brief:

- `documentation/mkdocs.yml` is the online website build.
- Changes under `documentation/**` are built and deployed to GitHub Pages by `.github/workflows/mkdocs.yml`.
- `documentation/mkdocs.offline.yml` is the offline HTML build used for local copies and release zips.
