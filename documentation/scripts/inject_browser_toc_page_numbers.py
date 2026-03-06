#!/usr/bin/env python3
"""Inject browser-compatible TOC page numbers into merged MkDocs HTML."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", required=True, help="Merged HTML file to mutate in place")
    parser.add_argument("--pdf", required=True, help="First-pass rendered PDF")
    return parser.parse_args()


def normalize(text: str) -> str:
    return " ".join(text.split())


def pdf_pages(pdf_path: Path) -> list[str]:
    raw = subprocess.check_output(["pdftotext", str(pdf_path), "-"], stderr=subprocess.DEVNULL)
    return [normalize(page) for page in raw.decode("utf-8", errors="ignore").split("\f")]


def first_meaningful_snippet(target: Tag) -> str | None:
    container = target.parent if target.name in {"h1", "h2", "h3", "h4", "h5", "h6"} else target

    for node in container.descendants:
        if not isinstance(node, Tag):
            continue
        if node.name not in {"p", "li"}:
            continue
        text = normalize(node.get_text(" ", strip=True))
        if not text:
            continue
        if text == "Tool Index":
            continue
        if text.startswith("Author:"):
            continue
        return text[:220]

    # Category pages often have the first real content inside the first nested section.
    for section in container.find_all("section"):
        snippet = first_meaningful_snippet(section)
        if snippet:
            return snippet

    return None


def page_for_target(target_id: str, soup: BeautifulSoup, pages: list[str]) -> int | None:
    target = soup.find(id=target_id)
    if target is None:
        return None

    if target_id == "doc-toc":
        for idx, page in enumerate(pages, start=1):
            if "Tool Index" in page:
                return idx
        return None

    snippet = first_meaningful_snippet(target)
    if snippet:
        for idx, page in enumerate(pages, start=1):
            if snippet in page:
                return idx

    heading = normalize(target.get_text(" ", strip=True))
    if heading:
        for idx, page in enumerate(pages, start=1):
            if heading in page and "Tool Index" not in page:
                return idx

    return None


def inject_numbers(html_path: Path, pages: list[str]) -> int:
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    toc = soup.find("article", id="doc-toc")
    if toc is None:
        raise SystemExit("ERROR: TOC article not found in merged HTML")

    injected = 0
    for link in toc.select("a[href^='#']"):
        target_id = link.get("href", "")[1:]
        page = page_for_target(target_id, soup, pages)
        if page is None:
            continue

        for old in link.select(".toc-page-number, .toc-label"):
            old.unwrap()

        label_contents = list(link.contents)
        link.clear()
        label = soup.new_tag("span", attrs={"class": "toc-label"})
        for child in label_contents:
            if isinstance(child, NavigableString):
                label.append(child)
            else:
                label.append(child)
        link.append(label)

        number = soup.new_tag("span", attrs={"class": "toc-page-number"})
        number.string = str(page)
        link.append(number)
        injected += 1

    html_path.write_text(str(soup), encoding="utf-8")
    return injected


def main() -> int:
    args = parse_args()
    html_path = Path(args.html).resolve()
    pdf_path = Path(args.pdf).resolve()

    if not html_path.is_file():
        raise SystemExit(f"ERROR: merged HTML not found: {html_path}")
    if not pdf_path.is_file():
        raise SystemExit(f"ERROR: first-pass PDF not found: {pdf_path}")

    pages = pdf_pages(pdf_path)
    injected = inject_numbers(html_path, pages)
    print(f"Injected {injected} TOC page numbers into {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
