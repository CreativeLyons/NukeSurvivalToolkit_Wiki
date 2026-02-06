# NukeSurvivalToolkit Wiki

MkDocs-based documentation site for Nuke Survival Toolkit.

## Overview

This repository contains the source content and configuration used to build and deploy the NST wiki.

- Docs source: `documentation/docs/`
- MkDocs config: `documentation/mkdocs.yml`
- Built local site output: `documentation/site/`
- CI deploy workflow: `.github/workflows/mkdocs.yml`

## Local Development

### Prerequisites

- Python 3.x
- `mkdocs`
- `mkdocs-material`

### Build

```bash
cd documentation
mkdocs build
```

### Serve Locally

```bash
cd documentation
mkdocs serve -a 127.0.0.1:8010
```

Then open:

- <http://127.0.0.1:8010/>

## Deployment

Deployment is handled by GitHub Actions via `.github/workflows/mkdocs.yml` when changes are pushed to `main` or `master` under `documentation/**`.

## Changelog

Project change history is tracked in `CHANGELOG.md`.
