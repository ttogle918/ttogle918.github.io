"""print/index.html 을 A4 PDF 로 굽는다 -> uploads/최지현_portfolio.pdf

헤더의 PDF 버튼이 이 파일을 그대로 내려준다. 인쇄본을 고친 뒤 다시 돌린다. 멱등하다.
@page { size: A4; margin: 0 } 과 .sheet { break-after: page } 를 그대로 따른다.

    python tools/build_pdf.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8")  # Windows cp949 콘솔
except Exception:
    pass

SITE = Path(__file__).resolve().parents[1]
SRC = SITE / "print" / "index.html"
OUT = SITE / "uploads" / "최지현_portfolio.pdf"


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(SRC.as_uri(), wait_until="networkidle")  # Google Fonts 까지 받는다
        page.evaluate("document.fonts.ready.then(() => true)")
        page.emulate_media(media="print")
        sheets = page.evaluate("document.querySelectorAll('section.sheet').length")
        page.pdf(path=str(OUT), prefer_css_page_size=True, print_background=True)
        browser.close()
    print(f"  {OUT.relative_to(SITE)}  {OUT.stat().st_size / 1e6:.2f}MB  (장 {sheets})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
