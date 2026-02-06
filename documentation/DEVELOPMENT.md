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
