#!/opt/homebrew/opt/python@3.14/bin/python3
"""Analyze wiki page density for PDF page-sharing prediction."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
CONFIG_PATH = ROOT / "mkdocs.pdf.yml"
REPORT_PATH = ROOT / "scripts" / "content_analysis_report.md"

IMAGE_MD_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
IMAGE_HTML_RE = re.compile(r"<img\b", re.IGNORECASE)
VIDEO_RE = re.compile(r"<video\b|video-container", re.IGNORECASE)
HTML_TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")

# v2.1.0 known page-sharing groups (using current nav display titles).
KNOWN_GROUPS = [
    ["apChromaUnpremult", "apChromaPremult"],
    ["apChromaMerge", "Chromatik"],
    ["DefocusSwirlyBokeh", "deHaze"],
    ["X_Sharpen", "X_Soften"],
    ["DespillToColor", "AdditiveKeyerPro"],
    ["ContactSheetAuto", "KeymixBBox"],
    ["iMorph", "Symmetry", "RP_Reformat"],
    ["CardToTrack", "CProject"],
    ["TransformMatrix", "CornerPin2D_Matrix"],
    ["MorphDissolve", "ITransform"],
    ["PlanarProjection", "Reconcile3DFast"],
    ["aPCard", "DummyCam"],
    ["SSMesh", "Unify3DCoordinate"],
    ["DeepSampleCount", "DeepSer"],
    ["Relight_Simple", "Reproject3D"],
    ["apDirLight", "apFresnel"],
    ["NormalsRotate", "EnvReflect_BB"],
    ["SimpleSSS", "aPmatte"],
    ["P_Project", "GlueP"],
    ["CurveRemapper", "NoiseGen"],
    ["GUI_Switch", "NAN_INF_Killer"],
    ["apViewerBlocker", "Python_and_TCL"],
    ["ViewerRender", "NukeZ"],
    ["Advanced Keying Template Stamps", "STMap Keyer Setup"],
]

KNOWN_SHARED_TOOL_TITLES = {title for group in KNOWN_GROUPS for title in group}


def _flatten_nav(items, out):
    for item in items or []:
        if isinstance(item, dict):
            for title, value in item.items():
                if isinstance(value, str):
                    out.append((title, value))
                elif isinstance(value, list):
                    _flatten_nav(value, out)


def _classify(title: str, src_uri: str, text_len: int, img_count: int) -> str:
    if src_uri.endswith("/index.md"):
        return "category-header"
    if title in KNOWN_SHARED_TOOL_TITLES:
        return "small"
    if text_len < 600 and img_count <= 1:
        return "small"
    if text_len <= 2000 and img_count <= 2:
        return "medium"
    return "large"


def _behavior(size: str) -> str:
    if size == "small":
        return "May share page"
    return "Starts new page"


def _load_pages():
    data = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    nav_entries = []
    _flatten_nav(data.get("nav"), nav_entries)

    pages = []
    for idx, (title, src_uri) in enumerate(nav_entries, start=1):
        md_path = DOCS_DIR / src_uri
        if not md_path.exists():
            continue
        raw = md_path.read_text(encoding="utf-8")
        img_count = len(IMAGE_MD_RE.findall(raw)) + len(IMAGE_HTML_RE.findall(raw))
        video_count = len(VIDEO_RE.findall(raw))
        text = IMAGE_MD_RE.sub(" ", raw)
        text = HTML_TAG_RE.sub(" ", text)
        text = WS_RE.sub(" ", text).strip()
        text_len = len(text)
        size = _classify(title, src_uri, text_len, img_count)
        pages.append(
            {
                "idx": idx,
                "title": title,
                "src_uri": src_uri,
                "chars": text_len,
                "images": img_count,
                "videos": video_count,
                "size": size,
                "behavior": _behavior(size),
                "note": "",
                "validation": "",
            }
        )
    return pages


def _validate_groups(pages):
    by_title = {p["title"]: p for p in pages}
    by_index = {p["idx"]: p for p in pages}

    for group in KNOWN_GROUPS:
        if not all(name in by_title for name in group):
            continue
        indices = [by_title[name]["idx"] for name in group]
        start_idx = min(indices)
        end_idx = max(indices)
        span_pages = [by_index[i] for i in range(start_idx, end_idx + 1) if i in by_index]
        span_all_small = all(p["size"] == "small" for p in span_pages)
        status = "match" if span_all_small else "mismatch"
        for name in group:
            by_title[name]["validation"] = status

    for page in pages:
        prev_page = by_index.get(page["idx"] - 1)
        next_page = by_index.get(page["idx"] + 1)
        notes = []
        if page["size"] == "small" and prev_page and prev_page["size"] == "small":
            notes.append("Consecutive small tools: likely shared page")
        if page["size"] == "large" and next_page and next_page["size"] == "small":
            notes.append("Large page may absorb next small tool")
        page["note"] = "; ".join(notes)


def _write_report(pages):
    small = sum(1 for p in pages if p["size"] == "small")
    medium = sum(1 for p in pages if p["size"] == "medium")
    large = sum(1 for p in pages if p["size"] == "large")

    lines = [
        "# Content Analysis Report",
        "",
        f"- Total pages analyzed: **{len(pages)}**",
        f"- Small: **{small}** | Medium: **{medium}** | Large: **{large}**",
        "",
        "| # | Title | Source | Chars | Img | Vid | Size | Predicted Behavior | Validation (v2.1.0) | Notes |",
        "|---:|---|---|---:|---:|---:|---|---|---|---|",
    ]
    for p in pages:
        lines.append(
            "| {idx} | {title} | `{src_uri}` | {chars} | {images} | {videos} | {size} | {behavior} | {validation} | {note} |".format(
                **p
            )
        )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    pages = _load_pages()
    _validate_groups(pages)
    _write_report(pages)
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
