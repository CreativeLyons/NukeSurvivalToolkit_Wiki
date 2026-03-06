#!/bin/bash
set -euo pipefail

VERSION="${1:-v2.2.0}"
WIKI_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WIKI_DIR"

TMP_DIR="$(mktemp -d /tmp/nst-pdf-build.XXXXXX)"
trap 'rm -rf "$TMP_DIR"' EXIT

PLAYWRIGHT_PYTHON="${PLAYWRIGHT_PYTHON:-}"
if [[ -z "$PLAYWRIGHT_PYTHON" ]]; then
  for candidate in \
    "/Library/Frameworks/Python.framework/Versions/3.10/bin/python3" \
    "$(command -v python3)"; do
    if [[ -x "$candidate" ]] && "$candidate" -c 'import playwright' >/dev/null 2>&1; then
      PLAYWRIGHT_PYTHON="$candidate"
      break
    fi
  done
fi

if [[ -z "$PLAYWRIGHT_PYTHON" ]]; then
  echo "ERROR: no Python with Playwright available. Set PLAYWRIGHT_PYTHON to a working interpreter." >&2
  exit 1
fi

# Use the repo-managed PDF cover asset directly.
COVER_SRC="$WIKI_DIR/docs/img/pdf/NukeSurvivalToolkit_Splashpage_cover.jpg"
if [[ ! -f "$COVER_SRC" ]]; then
  echo "ERROR: cover image not found: $COVER_SRC" >&2
  exit 1
fi

# Use a temporary MkDocs config so only this build points cover_logo to /tmp.
TMP_CONFIG="$TMP_DIR/mkdocs.pdf.yml"
cp "$WIKI_DIR/mkdocs.pdf.yml" "$TMP_CONFIG"
perl -0pi -e "s|cover_logo:\\s+.*|cover_logo: $COVER_SRC|g" "$TMP_CONFIG"
perl -0pi -e "s|cover_subtitle:\\s+.*|cover_subtitle: Release ${VERSION}|g" "$TMP_CONFIG"
perl -0pi -e "s|hooks/pdf_preprocess.py|$WIKI_DIR/hooks/pdf_preprocess.py|g" "$TMP_CONFIG"
perl -0pi -e "s|enabled_if_env:\\s*ENABLE_PDF_EXPORT|enabled_if_env: ENABLE_PDF_EXPORT\\n      custom_template_path: $WIKI_DIR/templates|g" "$TMP_CONFIG"
perl -0pi -e "s|output_path:\\s+.*|output_path: browser-render-placeholder.pdf\\n      debug_html: true|g" "$TMP_CONFIG"
{
  echo ""
  echo "docs_dir: $WIKI_DIR/docs"
  echo "site_dir: $WIKI_DIR/site"
} >> "$TMP_CONFIG"

echo "Building NST PDF - ${VERSION}"
DEBUG_HTML="$TMP_DIR/merged-output.html"
ENABLE_PDF_EXPORT=1 \
DYLD_LIBRARY_PATH="/opt/homebrew/lib" \
PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig" \
mkdocs build -f "$TMP_CONFIG" > "$DEBUG_HTML"

if ! grep -q '^<html' "$DEBUG_HTML"; then
  echo "ERROR: merged HTML capture failed at $DEBUG_HTML" >&2
  exit 1
fi

python3 "$WIKI_DIR/scripts/prepare_browser_html.py" --html "$DEBUG_HTML"

DEFAULT_PDF="NukeSurvivalToolkit_Documentation_Release_v2.2.0.pdf"
TARGET_PDF="NukeSurvivalToolkit_Documentation_Release_${VERSION}.pdf"
TARGET_PATH="$WIKI_DIR/$TARGET_PDF"
FIRST_PASS_PDF="$TMP_DIR/first-pass.pdf"

echo "Rendering merged HTML with Chrome via Playwright (pass 1)"
"$PLAYWRIGHT_PYTHON" "$WIKI_DIR/scripts/render_browser_pdf.py" \
  --html "$DEBUG_HTML" \
  --output "$FIRST_PASS_PDF" \
  --css "$WIKI_DIR/docs/css/pdf-browser.css"

python3 "$WIKI_DIR/scripts/inject_browser_toc_page_numbers.py" \
  --html "$DEBUG_HTML" \
  --pdf "$FIRST_PASS_PDF"

echo "Rendering merged HTML with Chrome via Playwright (pass 2)"
"$PLAYWRIGHT_PYTHON" "$WIKI_DIR/scripts/render_browser_pdf.py" \
  --html "$DEBUG_HTML" \
  --output "$TARGET_PATH" \
  --css "$WIKI_DIR/docs/css/pdf-browser.css"

if [[ "$TARGET_PDF" != "$DEFAULT_PDF" ]]; then
  cp "$TARGET_PATH" "$WIKI_DIR/$DEFAULT_PDF"
fi

echo "Output: $TARGET_PATH"
pdfinfo "$TARGET_PATH" | sed -n '1,20p'
open "$TARGET_PATH" 2>/dev/null || true
