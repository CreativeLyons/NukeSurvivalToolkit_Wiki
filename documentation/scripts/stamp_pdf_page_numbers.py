#!/usr/bin/env python3
"""Stamp consecutive page numbers onto an existing PDF."""

from __future__ import annotations

import argparse
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf._codecs.core_fontmetrics import CORE_FONT_METRICS
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject


PAGE_NUMBER_GRAY = 17 / 255


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Source PDF path")
    parser.add_argument("--output", required=True, help="Stamped PDF path")
    parser.add_argument("--first-page-index", type=int, required=True, help="1-based first page to stamp")
    parser.add_argument("--last-page-index", type=int, required=True, help="1-based last page to stamp")
    parser.add_argument("--start-number", type=int, required=True, help="First page number to draw")
    parser.add_argument("--font-name", default="Helvetica", help="Built-in PDF font name")
    parser.add_argument("--font-size-pt", type=float, default=11.04, help="Page number font size in points")
    parser.add_argument("--right-gap-pt", type=float, default=33.0, help="Gap from the right page edge")
    parser.add_argument("--bottom-gap-pt", type=float, default=14.0, help="Gap from the bottom page edge")
    return parser.parse_args()


def escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def text_width_points(text: str, *, font_name: str, font_size_pt: float) -> float:
    metrics = CORE_FONT_METRICS[font_name]
    widths = metrics.character_widths
    return sum(widths.get(char, widths.get(" ", 278)) for char in text) * font_size_pt / 1000.0


def baseline_y(*, font_name: str, font_size_pt: float, bottom_gap_pt: float) -> float:
    metrics = CORE_FONT_METRICS[font_name]
    return bottom_gap_pt + abs(metrics.descent) * font_size_pt / 1000.0


def make_overlay_page(
    text: str,
    *,
    width: float,
    height: float,
    font_name: str,
    font_size_pt: float,
    right_gap_pt: float,
    bottom_gap_pt: float,
):
    writer = PdfWriter()
    page = writer.add_blank_page(width=width, height=height)

    font = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/Font"),
            NameObject("/Subtype"): NameObject("/Type1"),
            NameObject("/BaseFont"): NameObject(f"/{font_name}"),
        }
    )
    font_ref = writer._add_object(font)
    page[NameObject("/Resources")] = DictionaryObject(
        {
            NameObject("/Font"): DictionaryObject({NameObject("/F1"): font_ref}),
        }
    )

    text_width_pt = text_width_points(text, font_name=font_name, font_size_pt=font_size_pt)
    x = width - right_gap_pt - text_width_pt
    y = baseline_y(font_name=font_name, font_size_pt=font_size_pt, bottom_gap_pt=bottom_gap_pt)
    stream = DecodedStreamObject()
    stream.set_data(
        (
            f"BT /F1 {font_size_pt:.2f} Tf {PAGE_NUMBER_GRAY:.6f} g "
            f"1 0 0 1 {x:.3f} {y:.3f} Tm ({escape_pdf_text(text)}) Tj ET"
        ).encode("utf-8")
    )
    stream_ref = writer._add_object(stream)
    page.replace_contents(stream_ref)

    buffer = BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    if not input_path.is_file():
        raise SystemExit(f"ERROR: input PDF not found: {input_path}")
    if args.first_page_index < 1 or args.last_page_index < args.first_page_index:
        raise SystemExit("ERROR: invalid page stamp range.")
    if args.font_name not in CORE_FONT_METRICS:
        raise SystemExit(f"ERROR: unsupported built-in font: {args.font_name}")

    reader = PdfReader(str(input_path))
    total_pages = len(reader.pages)
    if args.last_page_index > total_pages:
        raise SystemExit(
            f"ERROR: requested page range {args.first_page_index}-{args.last_page_index} exceeds {total_pages} pages."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()

    for page_index, page in enumerate(reader.pages, start=1):
        writer.add_page(page)
        if args.first_page_index <= page_index <= args.last_page_index:
            number_text = str(args.start_number + (page_index - args.first_page_index))
            overlay = make_overlay_page(
                number_text,
                width=float(page.mediabox.width),
                height=float(page.mediabox.height),
                font_name=args.font_name,
                font_size_pt=args.font_size_pt,
                right_gap_pt=args.right_gap_pt,
                bottom_gap_pt=args.bottom_gap_pt,
            )
            writer.pages[-1].merge_page(overlay)

    with output_path.open("wb") as handle:
        writer.write(handle)

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
