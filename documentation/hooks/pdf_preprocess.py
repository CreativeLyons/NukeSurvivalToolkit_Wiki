"""MkDocs PDF preprocessing hook.

This hook prepares wiki pages for PDF export by:
1) Replacing dynamic video embeds with static linked thumbnails.
2) Replacing <video> elements with still images.
3) Classifying page density to guide page-break behavior.
"""

from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import quote

from bs4 import BeautifulSoup, Tag


VIDEO_CONTAINER_RE = re.compile(
    r"<div\s+class=[\"']video-container[\"'](?P<attrs>[^>]*)>\s*</div>",
    re.IGNORECASE | re.DOTALL,
)
VIDEO_TAG_RE = re.compile(
    r"<video(?P<attrs>[^>]*)>(?P<body>.*?)</video>",
    re.IGNORECASE | re.DOTALL,
)
SOURCE_SRC_RE = re.compile(r"<source[^>]*\ssrc=[\"'](?P<src>[^\"']+)[\"'][^>]*>", re.IGNORECASE)
ATTR_RE = re.compile(r"([a-zA-Z_:][-a-zA-Z0-9_:.]*)=[\"']([^\"']*)[\"']")
TAG_RE = re.compile(r"<[^>]+>")
IMG_RE = re.compile(r"<img\b", re.IGNORECASE)
H1_RE = re.compile(r"<h1(?P<attrs>[^>]*)>.*?</h1>", re.IGNORECASE | re.DOTALL)
LEADING_IMAGE_RE = re.compile(
    r'^\s*<p>\s*<img[^>]+alt="[^"]*"[^>]*>\s*</p>\s*',
    re.IGNORECASE | re.DOTALL,
)
TRAILING_SECTION_RE = re.compile(
    r"<h2[^>]*>\s*(Tool Categories|Getting Started|About the Toolkit)\s*</h2>.*$",
    re.IGNORECASE | re.DOTALL,
)

YOUTUBE_WATCH_BASE = "https://www.youtube.com/watch?v="
VIMEO_WATCH_BASE = "https://vimeo.com/"

KNOWN_SHARED_TOOL_TITLES = {
    "apChromaUnpremult",
    "apChromaPremult",
    "apChromaMerge",
    "Chromatik",
    "DefocusSwirlyBokeh",
    "deHaze",
    "X_Sharpen",
    "X_Soften",
    "DespillToColor",
    "AdditiveKeyerPro",
    "ContactSheetAuto",
    "KeymixBBox",
    "iMorph",
    "Symmetry",
    "RP_Reformat",
    "CardToTrack",
    "CProject",
    "TransformMatrix",
    "CornerPin2D_Matrix",
    "MorphDissolve",
    "ITransform",
    "PlanarProjection",
    "Reconcile3DFast",
    "aPCard",
    "DummyCam",
    "SSMesh",
    "Unify3DCoordinate",
    "DeepSampleCount",
    "DeepSer",
    "Relight_Simple",
    "Reproject3D",
    "apDirLight",
    "apFresnel",
    "NormalsRotate",
    "EnvReflect_BB",
    "SimpleSSS",
    "aPmatte",
    "P_Project",
    "GlueP",
    "CurveRemapper",
    "NoiseGen",
    "GUI_Switch",
    "NAN_INF_Killer",
    "apViewerBlocker",
    "Python_and_TCL",
    "ViewerRender",
    "NukeZ",
    "Advanced Keying Template Stamps",
    "STMap Keyer Setup",
}


def _svg_placeholder_data_uri() -> str:
    svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#24292f"/>
      <stop offset="100%" stop-color="#111418"/>
    </linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#bg)"/>
  <circle cx="640" cy="360" r="88" fill="#000000AA"/>
  <polygon points="615,310 615,410 700,360" fill="#FFFFFF"/>
  <text x="640" y="560" text-anchor="middle" fill="#D0D7DE" font-family="Arial, sans-serif" font-size="40">
    Video Preview
  </text>
</svg>
""".strip()
    return "data:image/svg+xml;charset=utf-8," + quote(svg)


def _parse_attrs(attr_blob: str) -> dict[str, str]:
    return {k.lower(): v for k, v in ATTR_RE.findall(attr_blob or "")}


def _page_depth(src_uri: str) -> int:
    parent = Path(src_uri).parent
    if str(parent) in (".", ""):
        return 0
    return len(parent.parts)


def _prefix_for_page(src_uri: str) -> str:
    return "../" * _page_depth(src_uri)


def _resolve_relative_to_docs(docs_dir: str, src_uri: str, rel_path: str) -> Path:
    page_dir = Path(docs_dir) / Path(src_uri).parent
    return (page_dir / rel_path).resolve()


def _exists_relative_to_page(docs_dir: str, src_uri: str, candidate: str | None) -> bool:
    if not candidate:
        return False
    if candidate.startswith(("http://", "https://", "data:")):
        return True
    return _resolve_relative_to_docs(docs_dir, src_uri, candidate).exists()


def _watch_url(video_id: str, video_type: str) -> str:
    if video_type == "vimeo":
        return f"{VIMEO_WATCH_BASE}{video_id}"
    return f"{YOUTUBE_WATCH_BASE}{video_id}"


def _generated_thumb_src(src_uri: str, video_type: str, video_id: str) -> str:
    return f"{_prefix_for_page(src_uri)}img/video-thumbs/{video_type}-{video_id}.webp"


def _video_container_repl(match: re.Match[str], *, page, docs_dir: str) -> str:
    attrs = _parse_attrs(match.group("attrs"))
    video_id = attrs.get("data-video-id", "").strip()
    if not video_id:
        return match.group(0)

    video_type = attrs.get("data-video-type", "youtube").strip().lower() or "youtube"
    if video_type not in {"youtube", "vimeo"}:
        video_type = "youtube"

    watch_url = _watch_url(video_id, video_type)
    explicit_thumb = attrs.get("data-thumbnail", "").strip()
    generated_thumb = _generated_thumb_src(page.file.src_uri, video_type, video_id)

    if _exists_relative_to_page(docs_dir, page.file.src_uri, explicit_thumb):
        thumb_src = explicit_thumb
    elif _exists_relative_to_page(docs_dir, page.file.src_uri, generated_thumb):
        thumb_src = generated_thumb
    else:
        thumb_src = _svg_placeholder_data_uri()

    return (
        '<div class="pdf-video-thumb">'
        f'<a href="{html.escape(watch_url, quote=True)}">'
        f'<img src="{html.escape(thumb_src, quote=True)}" alt="Video thumbnail"></a>'
        "</div>"
    )


def _derive_still_from_video_src(video_src: str | None) -> str | None:
    if not video_src:
        return None
    stem, _sep, _ext = video_src.rpartition(".")
    if not stem:
        return None
    return f"{stem}.webp"


def _video_tag_repl(match: re.Match[str], *, page, docs_dir: str) -> str:
    attrs = _parse_attrs(match.group("attrs"))
    body = match.group("body") or ""

    poster = attrs.get("poster")
    src_in_video = attrs.get("src")
    src_in_source = None
    src_match = SOURCE_SRC_RE.search(body)
    if src_match:
        src_in_source = src_match.group("src")
    video_src = src_in_video or src_in_source
    derived_still = _derive_still_from_video_src(video_src)

    if _exists_relative_to_page(docs_dir, page.file.src_uri, poster):
        img_src = poster
    elif _exists_relative_to_page(docs_dir, page.file.src_uri, derived_still):
        img_src = derived_still
    else:
        img_src = _svg_placeholder_data_uri()

    img_html = f'<img src="{html.escape(img_src, quote=True)}" alt="Video thumbnail">'
    if video_src:
        return (
            '<div class="pdf-video-thumb">'
            f'<a href="{html.escape(video_src, quote=True)}">{img_html}</a>'
            "</div>"
        )
    return f'<div class="pdf-video-thumb">{img_html}</div>'


def _classify_page(content: str, src_uri: str, title: str) -> str:
    text = TAG_RE.sub(" ", content)
    text = re.sub(r"\s+", " ", text).strip()
    text_len = len(text)
    img_count = len(IMG_RE.findall(content))
    classes: list[str] = []

    if src_uri == "index.md":
        classes.append("pdf-small")
        return " ".join(classes)

    if src_uri == "intro.md":
        classes.append("pdf-small")
        return " ".join(classes)

    # Non-home index pages act as section landing pages and should force a break.
    if src_uri.endswith("/index.md"):
        classes.append("pdf-category-header")
        return " ".join(classes)

    # Calibrated against known v2.1.0 shared-page pairs.
    if title in KNOWN_SHARED_TOOL_TITLES:
        classes.append("pdf-small")
    elif text_len < 600 and img_count <= 1:
        classes.append("pdf-small")
    elif text_len <= 2000 and img_count <= 2:
        classes.append("pdf-medium")
    else:
        classes.append("pdf-large")

    return " ".join(classes)


def _reshape_front_matter(content: str, src_uri: str) -> str:
    if src_uri != "index.md":
        return content

    soup = BeautifulSoup(content, "html.parser")

    h1 = soup.find("h1")
    if h1:
        order = h1.find("span", class_="pdf-order")
        h1.clear()
        if order:
            h1.append(order)
            h1.append(" ")
        h1.append("About")

    release_marker = soup.find("code", string=re.compile(r"Release v", re.IGNORECASE))
    if release_marker and release_marker.parent:
        release_marker.parent.decompose()

    first_img = soup.find("img")
    if first_img:
        container = first_img.parent
        if container and getattr(container, "name", None) in {"p", "figure"}:
            container.decompose()
        else:
            first_img.decompose()

    for h2 in soup.find_all("h2"):
        if h2.get_text(" ", strip=True) in {"Tool Categories", "Getting Started", "About the Toolkit"}:
            for sibling in list(h2.find_all_next()):
                sibling.decompose()
            h2.decompose()
            break

    return str(soup)


def _reshape_intro(content: str, src_uri: str) -> str:
    if src_uri != "intro.md":
        return content

    soup = BeautifulSoup(content, "html.parser")
    for img in soup.find_all("img"):
        img.decompose()
    return str(soup)


def _is_standalone_image_block(node: Tag) -> bool:
    if node.name not in {"p", "figure", "div"}:
        return False

    if node.name == "div":
        classes = node.get("class", [])
        return "pdf-video-thumb" in classes and len(node.find_all("img", recursive=False)) == 1

    children = [child for child in node.children if isinstance(child, Tag)]
    return len(children) == 1 and children[0].name == "img" and not node.get_text(" ", strip=True)


def _compact_trailing_image_blocks(content: str) -> str:
    soup = BeautifulSoup(content, "html.parser")
    top_level_tags = [node for node in soup.contents if isinstance(node, Tag)]

    # Consecutive standalone image blocks trigger poor pagination in Chrome's
    # PDF renderer. Insert an invisible separator between adjacent blocks so the
    # layout behaves like there is a line of content between them, without
    # changing the visible output.
    previous_was_image = False
    for node in top_level_tags:
        current_is_image = _is_standalone_image_block(node)
        if current_is_image and previous_was_image:
            separator = soup.new_tag("div")
            separator["class"] = ["pdf-image-flow-break"]
            separator["aria-hidden"] = "true"
            node.insert_before(separator)
        previous_was_image = current_is_image

    # Preserve the useful single-trailing-image case for large lone screenshots.
    refreshed_tags = [node for node in soup.contents if isinstance(node, Tag)]
    trailing_blocks: list[Tag] = []
    for node in reversed(refreshed_tags):
        if _is_standalone_image_block(node):
            trailing_blocks.append(node)
            continue
        break

    if len(trailing_blocks) == 1:
        trailing = trailing_blocks[0]
        classes = list(trailing.get("class", []))
        if "pdf-single-trailing-image" not in classes:
            classes.append("pdf-single-trailing-image")
        trailing["class"] = classes

    return str(soup)


def on_page_content(html_content, page, config, files):  # pylint: disable=unused-argument
    docs_dir = str(config["docs_dir"])

    processed = VIDEO_CONTAINER_RE.sub(
        lambda m: _video_container_repl(m, page=page, docs_dir=docs_dir),
        html_content,
    )
    processed = VIDEO_TAG_RE.sub(
        lambda m: _video_tag_repl(m, page=page, docs_dir=docs_dir),
        processed,
    )
    processed = _reshape_front_matter(processed, page.file.src_uri)
    processed = _reshape_intro(processed, page.file.src_uri)
    processed = _compact_trailing_image_blocks(processed)

    page_class = _classify_page(processed, page.file.src_uri, getattr(page, "title", ""))
    return f'<div class="{page_class}">\n{processed}\n</div>'
