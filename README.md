# NukeSurvivalToolkit Wiki

[![Nuke Survival Toolkit Documentation Banner](documentation/docs/img/nst-wiki-large.jpeg)](https://creativelyons.github.io/NukeSurvivalToolkit_Wiki/)

The NST Wiki is the documentation site for the Nuke Survival Toolkit. It covers the current NST release, installation guidance, menu overview, and reference pages for `175+` tools.

`Current wiki release: v2.2.0`  
`Read online:` <https://creativelyons.github.io/NukeSurvivalToolkit_Wiki/>  
`Download releases:` <https://github.com/CreativeLyons/NukeSurvivalToolkit_Wiki/releases>

If you just want the fastest path:

- Read the live site: [NST Wiki Online](https://creativelyons.github.io/NukeSurvivalToolkit_Wiki/)
- Use it offline without building: download the latest release zip and open `NST_Documentation/index.html`
- Build your own local copy: use the quick commands below
- Export a PDF copy: run `./export_pdf`

## What You Can Do Here

- Browse the NST wiki online through GitHub Pages.
- Use an offline HTML copy for local browsing.
- Export a local PDF reference copy of the wiki.
- Edit and maintain the wiki source in this repository.

## Online, Offline HTML, And PDF

There are three ways to use this wiki:

- Online site: the public website, best for normal reading and sharing links.
- Offline HTML: a local copy of the website, best when you want the wiki on disk or inside a release zip.
- PDF export: a single-file reference document, best for portable sharing, review, or printing.

## Quick Local Preview

If you are editing the wiki and want the normal website view, run:

```bash
cd documentation
mkdocs serve -f mkdocs.yml -a 127.0.0.1:8010
```

Then open `http://127.0.0.1:8010/`.

## Quick Offline Build

If you want a local offline HTML copy from source, run:

```bash
cd documentation
mkdocs build -f mkdocs.offline.yml
```

This writes the offline site to `documentation/site/`.

If you are using a prebuilt release zip instead, unzip it and open `NST_Documentation/index.html`.

## Offline PDF Export

If you want a portable PDF version of the wiki, use:

```bash
./export_pdf
```

By default this exports the full wiki to `output/pdf/`. For more PDF options, offline workflows, and step-by-step instructions, use the user guide below.

## More Help

- [User Guide](documentation/USER_GUIDE.md): step-by-step instructions for local preview, offline HTML, publishing, and PDF export.
- [Development Notes](documentation/DEVELOPMENT.md): contributor-facing repository structure, deployment behavior, and PDF internals.
- [Changelog](CHANGELOG.md): project history and current unreleased changes.
- [Wiki Home Source](documentation/docs/index.md): the markdown source for the site landing page.

## How It Is Hosted

The public wiki is hosted on GitHub Pages and built by GitHub Actions.

In brief:

- `documentation/mkdocs.yml` is the online website build.
- `documentation/mkdocs.offline.yml` is the offline HTML build used for local copies and release zips.
- Changes under `documentation/**` are built and deployed to GitHub Pages by `.github/workflows/mkdocs.yml`.
