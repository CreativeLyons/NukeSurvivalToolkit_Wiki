#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3
"""Render merged MkDocs HTML to PDF with Playwright + Chrome."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", required=True, help="Path to merged HTML file")
    parser.add_argument("--output", required=True, help="Target PDF path")
    parser.add_argument("--css", required=True, help="Browser print override CSS")
    parser.add_argument("--wait-ms", type=int, default=1200)
    parser.add_argument("--timeout-ms", type=int, default=60000)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    html_path = Path(args.html).resolve()
    output_path = Path(args.output).resolve()
    css_path = Path(args.css).resolve()

    if not html_path.is_file():
        print(f"ERROR: merged HTML not found: {html_path}", file=sys.stderr)
        return 1

    if not css_path.is_file():
        print(f"ERROR: browser print CSS not found: {css_path}", file=sys.stderr)
        return 1

    css_text = css_path.read_text(encoding="utf-8")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(
            viewport={"width": 1280, "height": 1810},
            device_scale_factor=2,
        )

        page.goto(html_path.as_uri(), wait_until="domcontentloaded", timeout=args.timeout_ms)
        try:
            page.wait_for_load_state("networkidle", timeout=args.timeout_ms)
        except PlaywrightTimeoutError:
            pass

        page.add_style_tag(content=css_text)
        page.emulate_media(media="print")
        page.wait_for_timeout(args.wait_ms)
        page.pdf(
            path=str(output_path),
            format="Letter",
            print_background=True,
            display_header_footer=False,
            prefer_css_page_size=True,
        )
        browser.close()

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
