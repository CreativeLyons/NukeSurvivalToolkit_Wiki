#!/usr/bin/env python3
"""Adjust merged mkdocs-with-pdf HTML for browser-based PDF rendering."""

from __future__ import annotations

import argparse
from pathlib import Path

from bs4 import BeautifulSoup


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", required=True, help="Merged HTML file to modify in place")
    return parser.parse_args()


def move_toc_after_menus(soup: BeautifulSoup) -> None:
    toc = soup.find("article", id="doc-toc")
    menus = soup.find("article", attrs={"data-url": "/menus/"})
    if not toc or not menus:
        return
    toc.extract()
    menus.insert_after(toc)


def main() -> int:
    args = parse_args()
    html_path = Path(args.html).resolve()
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")

    move_toc_after_menus(soup)

    html_path.write_text(str(soup), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
