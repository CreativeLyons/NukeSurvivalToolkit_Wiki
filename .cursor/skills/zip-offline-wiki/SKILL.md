---
name: zip-offline-wiki
description: >-
  Builds the MkDocs offline wiki (mkdocs.offline.yml) and zips it to the repo root
  as NST_Documentation_Release_<version>.zip with a single top-level folder
  NST_Documentation/ (same layout as NST_Documentation_Release_2.1.1.zip). Use when
  the user asks to zip the offline wiki, release wiki, zip wiki, build offline wiki
  zip, NST_Documentation_Release, or invokes skill zip-offline-wiki.
---

# Zip offline wiki (release layout)

## Reference (source of truth)

The canonical release layout is demonstrated by the tracked reference archive at the repo root:

- **Filename:** `NST_Documentation_Release_<version>.zip`  
  Example: `NST_Documentation_Release_2.1.1.zip`
- **Inside the zip:** exactly one top-level directory named **`NST_Documentation/`** containing the full static site (e.g. `NST_Documentation/index.html`, `NST_Documentation/search/`, `NST_Documentation/assets/`, category folders, etc.).
- **Not** the name `site/` at the zip root — that does not match the release format.

Verify with: `unzip -l NST_Documentation_Release_2.1.1.zip | head`

## When to run

- User wants a shippable offline wiki bundle matching past releases.
- Triggers: “zip offline wiki”, “release wiki”, “zip wiki”, `zip-offline-wiki`.

## Steps (agent)

1. **Choose `<version>`** — Semver string for the documentation bundle (e.g. `2.2.0`), usually aligned with the NST documentation release being shipped. If the user did not specify it, ask once before building.
2. **Build offline HTML** (from repo root):

   ```bash
   cd documentation && mkdocs build -f mkdocs.offline.yml
   ```

   - Run from `documentation/` so plugin cache stays under `documentation/.cache/` (see `documentation/DEVELOPMENT.md`).
3. **Package** — Prefer the repo script (keeps layout identical every time):

   ```bash
   .cursor/skills/zip-offline-wiki/scripts/build_offline_wiki_zip.sh <version>
   ```

   Output path: **`NST_Documentation_Release_<version>.zip`** at the **repository root**.

4. **Confirm** — Quick check:

   ```bash
   unzip -l NST_Documentation_Release_<version>.zip | head -20
   ```

   First entries must show `NST_Documentation/...`, not `site/...`.

5. **Git** — `*.zip` is gitignored by default. Only `git add -f` a release zip if the user explicitly wants it committed or attached to a release.

## Requirements

- Python environment with `mkdocs` and `mkdocs-material` (and offline build plugins from `mkdocs.offline.yml`: `offline`, `privacy`).
- `zip` CLI (macOS built-in).

## Do not

- Change the inner folder name to `site/` for release zips (breaks parity with `NST_Documentation_Release_2.1.1.zip`).
- Rename or restructure files inside the built tree beyond copying `documentation/site` → staging folder `NST_Documentation` for the archive.
