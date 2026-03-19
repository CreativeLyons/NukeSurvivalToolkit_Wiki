#!/usr/bin/env bash
# Build is NOT run here — run `mkdocs build -f mkdocs.offline.yml` in documentation/ first.
# Packages documentation/site into repo-root NST_Documentation_Release_<version>.zip
# with top-level folder NST_Documentation/ (matches NST_Documentation_Release_2.1.1.zip).
set -euo pipefail

VERSION="${1:-}"
if [[ -z "${VERSION}" ]]; then
  echo "Usage: $0 <version>" >&2
  echo "  Example: $0 2.2.0" >&2
  echo "  Writes: <repo-root>/NST_Documentation_Release_<version>.zip" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../.." && pwd)"
DOCS="${REPO_ROOT}/documentation"
SITE="${DOCS}/site"
STAGING_NAME="NST_Documentation"
STAGING_PATH="${DOCS}/${STAGING_NAME}"
OUT_ZIP="${REPO_ROOT}/NST_Documentation_Release_${VERSION}.zip"

if [[ ! -d "${SITE}" ]] || [[ ! -f "${SITE}/index.html" ]]; then
  echo "error: ${SITE} missing or not built (no index.html). Run:" >&2
  echo "  cd documentation && mkdocs build -f mkdocs.offline.yml" >&2
  exit 1
fi

if [[ -e "${STAGING_PATH}" ]]; then
  echo "error: staging path already exists, remove it first: ${STAGING_PATH}" >&2
  exit 1
fi

cleanup() {
  rm -rf "${STAGING_PATH}"
}
trap cleanup EXIT

cp -R "${SITE}" "${STAGING_PATH}"
(
  cd "${DOCS}"
  rm -f "${OUT_ZIP}"
  zip -r -q "${OUT_ZIP}" "${STAGING_NAME}" -x "*.DS_Store" -x "*/.DS_Store"
)

echo "Wrote ${OUT_ZIP}"
ls -lh "${OUT_ZIP}"
