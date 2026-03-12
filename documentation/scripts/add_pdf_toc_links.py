#!/usr/bin/env python3
"""Add clickable TOC links and outline entries to an existing PDF."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Link
from pypdf.generic import NameObject


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the post-render TOC link injection pass."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Source PDF path")
    parser.add_argument("--output", required=True, help="Output PDF path")
    parser.add_argument("--spec", required=True, help="JSON spec with links and outline entries")
    return parser.parse_args()


def main() -> int:
    """Apply clickable TOC links and bookmarks to an existing PDF."""
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    spec_path = Path(args.spec).resolve()

    if not input_path.is_file():
        raise SystemExit(f"ERROR: input PDF not found: {input_path}")
    if not spec_path.is_file():
        raise SystemExit(f"ERROR: link spec not found: {spec_path}")

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    reader = PdfReader(str(input_path))
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    for link in spec.get("links", []):
        source_page_index = int(link["source_page_number"]) - 1
        dest_page_index = int(link["dest_page_number"]) - 1
        if not (0 <= source_page_index < len(writer.pages)):
            raise SystemExit(f"ERROR: invalid source page number {link['source_page_number']}")
        if not (0 <= dest_page_index < len(writer.pages)):
            raise SystemExit(f"ERROR: invalid destination page number {link['dest_page_number']}")

        writer.add_annotation(
            source_page_index,
            Link(
                rect=tuple(link["rect"]),
                target_page_index=dest_page_index,
            ),
        )

    parents: dict[int, object | None] = {-1: None}
    for item in spec.get("outline", []):
        level = int(item.get("level", 0))
        page_index = int(item["page_number"]) - 1
        if not (0 <= page_index < len(writer.pages)):
            raise SystemExit(f"ERROR: invalid outline destination page {item['page_number']}")

        parent = parents.get(level - 1)
        outline_ref = writer.add_outline_item(
            item["title"],
            page_index,
            parent=parent,
            is_open=True,
        )
        parents[level] = outline_ref
        for deeper_level in [key for key in parents if key > level]:
            del parents[deeper_level]

    writer._root_object[NameObject("/PageMode")] = NameObject("/UseOutlines")

    with output_path.open("wb") as handle:
        writer.write(handle)

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
