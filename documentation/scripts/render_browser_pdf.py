#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3
"""Render merged MkDocs HTML to PDF with Playwright + Chrome."""

from __future__ import annotations

import argparse
import json
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

PAGE_READY_SCRIPT = """
async () => {
  if (document.fonts && document.fonts.ready) {
    try {
      await document.fonts.ready;
    } catch (error) {
      // Ignore font readiness failures and continue with rendering.
    }
  }

  const loadPromises = [];
  for (const image of Array.from(document.images || [])) {
    if (image.complete) {
      continue;
    }
    loadPromises.push(new Promise((resolve) => {
      const finish = () => resolve();
      image.addEventListener('load', finish, { once: true });
      image.addEventListener('error', finish, { once: true });
    }));
  }

  if (loadPromises.length) {
    await Promise.all(loadPromises);
  }

  await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", help="Path to merged HTML file")
    parser.add_argument("--output", help="Target PDF path")
    parser.add_argument("--css", help="Browser print override CSS")
    parser.add_argument("--jobs-json", help="Path to a JSON file containing render jobs")
    parser.add_argument("--wait-ms", type=int, default=250)
    parser.add_argument("--timeout-ms", type=int, default=60000)
    return parser.parse_args()


def load_jobs(args: argparse.Namespace) -> list[dict[str, str]]:
    if args.jobs_json:
        jobs_path = Path(args.jobs_json).resolve()
        if not jobs_path.is_file():
            raise SystemExit(f"ERROR: jobs JSON not found: {jobs_path}")
        jobs = json.loads(jobs_path.read_text(encoding="utf-8"))
        if not isinstance(jobs, list) or not jobs:
            raise SystemExit("ERROR: jobs JSON must contain a non-empty array.")
        normalized_jobs = []
        for index, job in enumerate(jobs, start=1):
            if not isinstance(job, dict):
                raise SystemExit(f"ERROR: job {index} is not an object.")
            try:
                html_path = str(Path(job["html"]).resolve())
                output_path = str(Path(job["output"]).resolve())
                css_path = str(Path(job["css"]).resolve())
            except KeyError as exc:
                raise SystemExit(f"ERROR: job {index} is missing key: {exc.args[0]}") from exc
            normalized_jobs.append({"html": html_path, "output": output_path, "css": css_path})
        return normalized_jobs

    if not (args.html and args.output and args.css):
        raise SystemExit("ERROR: either --jobs-json or all of --html/--output/--css are required.")

    return [
        {
            "html": str(Path(args.html).resolve()),
            "output": str(Path(args.output).resolve()),
            "css": str(Path(args.css).resolve()),
        }
    ]


def render_job(page, job: dict[str, str], *, wait_ms: int, timeout_ms: int) -> None:
    html_path = Path(job["html"])
    output_path = Path(job["output"])
    css_path = Path(job["css"])

    if not html_path.is_file():
        raise SystemExit(f"ERROR: merged HTML not found: {html_path}")
    if not css_path.is_file():
        raise SystemExit(f"ERROR: browser print CSS not found: {css_path}")

    css_text = css_path.read_text(encoding="utf-8")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    page.goto(html_path.as_uri(), wait_until="domcontentloaded", timeout=timeout_ms)
    try:
        page.wait_for_load_state("networkidle", timeout=timeout_ms)
    except PlaywrightTimeoutError:
        pass

    page.add_style_tag(content=css_text)
    page.emulate_media(media="print")
    page.evaluate(PAGE_READY_SCRIPT)
    page.evaluate(SINGLE_TRAILING_IMAGE_FIT_SCRIPT)
    if wait_ms > 0:
        page.wait_for_timeout(wait_ms)
    page.pdf(
        path=str(output_path),
        format="Letter",
        print_background=True,
        display_header_footer=False,
        prefer_css_page_size=True,
    )
    print(output_path)


def main() -> int:
    args = parse_args()
    jobs = load_jobs(args)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(
            viewport={"width": 1280, "height": 1810},
            device_scale_factor=2,
        )
        for job in jobs:
            render_job(page, job, wait_ms=args.wait_ms, timeout_ms=args.timeout_ms)
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
