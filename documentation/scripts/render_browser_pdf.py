#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3
"""Render merged MkDocs HTML to PDF with Playwright + Chrome."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


SINGLE_TRAILING_IMAGE_FIT_SCRIPT = """
() => {
  const PX_PER_MM = 96 / 25.4;
  const CONTENT_HEIGHT_PX = 251.4 * PX_PER_MM; // Letter minus 16mm/12mm margins
  const SINGLE_TRAILING_MAX_PX = 170 * PX_PER_MM;
  const MIN_SCALE = 0.75;
  const BLOCK_BUFFER_PX = 8;
  const TIGHT_IMAGE_MARGIN_PX = 3;
  const TIGHT_BLOCK_MARGIN_BOTTOM_PX = 4;

  for (const block of document.querySelectorAll('section[data-url] .pdf-last-trailing-image')) {
    const img = block.querySelector('img');
    if (!img || !img.naturalWidth || !img.naturalHeight) {
      continue;
    }

    const prev = block.previousElementSibling;
    const section = block.closest('section[data-url]');
    if (!prev) {
      continue;
    }
    if (!section) {
      continue;
    }

    const sectionTop = section.getBoundingClientRect().top + window.scrollY;
    const prevBottom = prev.getBoundingClientRect().bottom + window.scrollY;
    const usedWithinSection = Math.max(0, prevBottom - sectionTop);
    const remainingOnPage = CONTENT_HEIGHT_PX - (usedWithinSection % CONTENT_HEIGHT_PX);
    const usableHeight = remainingOnPage - BLOCK_BUFFER_PX;
    if (usableHeight <= 0) {
      continue;
    }

    const blockRect = block.getBoundingClientRect();
    const imgRect = img.getBoundingClientRect();
    const prevRect = prev.getBoundingClientRect();
    const blockStyles = window.getComputedStyle(block);
    const blockMarginBottom = parseFloat(blockStyles.marginBottom) || 0;
    const nonImageFootprint = (blockRect.bottom - prevRect.bottom) - imgRect.height + blockMarginBottom;
    const availableImageHeight = usableHeight - nonImageFootprint - TIGHT_IMAGE_MARGIN_PX * 2 - TIGHT_BLOCK_MARGIN_BOTTOM_PX;
    const currentHeight = imgRect.height;
    if (!currentHeight || availableImageHeight <= 0) {
      continue;
    }
    const fullRenderedHeight = Math.min(currentHeight, SINGLE_TRAILING_MAX_PX);

    // Preserve the default auto/full size unless shrinking would actually allow
    // the image to fit on the current page at a reasonable scale.
    if (fullRenderedHeight <= usableHeight) {
      continue;
    }

    const requiredScale = availableImageHeight / fullRenderedHeight;
    if (requiredScale < MIN_SCALE) {
      continue;
    }

    img.style.setProperty('max-height', `${availableImageHeight}px`, 'important');
    img.style.setProperty('max-width', '100%', 'important');
    img.style.setProperty('height', 'auto', 'important');
    img.style.setProperty('width', 'auto', 'important');
    img.style.setProperty('margin-top', `${TIGHT_IMAGE_MARGIN_PX}px`, 'important');
    img.style.setProperty('margin-bottom', `${TIGHT_IMAGE_MARGIN_PX}px`, 'important');
    block.style.setProperty('margin-bottom', `${TIGHT_BLOCK_MARGIN_BOTTOM_PX}px`, 'important');
  }
}
"""


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
        page.evaluate(SINGLE_TRAILING_IMAGE_FIT_SCRIPT)
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
