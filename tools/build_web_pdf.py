"""index.html(웹사이트 그대로)을 A4 PDF 로 굽는다 -> uploads/최지현_portfolio_web.pdf

히어로의 «PDF 다운받기» 버튼이 이 파일을 내려준다. 인쇄본 요약판(print/index.html ->
최지현_portfolio.pdf, tools/build_pdf.py)과는 다른 파일이다. 사이트를 고친 뒤 다시 돌린다. 멱등하다.

화면에서 스크롤해야 생기는 것들을 굽기 전에 채운다:
- data-src 이미지는 src 로 옮긴다 (GIF 는 첫 프레임만 찍힌다)
- data-count 카운터는 최종값으로 박는다
- <details> 는 전부 연다 (담당 강의 목록 등)
카드 펼치기·헤더 숨기기는 index.html 의 @media print 규칙이 맡는다.

    python tools/build_web_pdf.py
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
SRC = SITE / "index.html"
OUT = SITE / "uploads" / "최지현_portfolio_web.pdf"

PREPARE = """
() => {
  document.querySelectorAll('img[data-src]').forEach(img => {
    if (!img.getAttribute('src')) img.setAttribute('src', img.dataset.src);
  });
  document.querySelectorAll('[data-count]').forEach(el => { el.textContent = el.dataset.count; });
  document.querySelectorAll('details').forEach(d => { d.open = true; });
  document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
}
"""


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 900})
        page.goto(SRC.as_uri(), wait_until="networkidle")  # Google Fonts 까지 받는다
        page.evaluate("document.fonts.ready.then(() => true)")
        page.evaluate(PREPARE)
        page.wait_for_load_state("networkidle")
        page.evaluate("Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })))")
        page.emulate_media(media="print")
        page.pdf(path=str(OUT), format="A4", print_background=True)
        browser.close()
    print(f"  {OUT.relative_to(SITE)}  {OUT.stat().st_size / 1e6:.2f}MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
