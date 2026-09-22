"""deck/index.html(16:9 슬라이드판)을 PDF 로 굽는다 -> uploads/최지현_portfolio.pdf

웹 PDF(index.html -> _web.pdf)와는 다른 파일이다. 사이트의 PDF 버튼 세 곳이 이 파일을 내려준다.
슬라이드는 1440 x 810px 고정이라, 굽기 전에 넘친 곳을 찾아 알려 준다. 넘친 슬라이드가 있으면 exit 1.

    python tools/build_deck_pdf.py            # PDF 굽기 + 넘침 검사
    python tools/build_deck_pdf.py --png DIR  # 슬라이드마다 PNG 도 저장 (눈으로 확인할 때)
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
SRC = SITE / "deck" / "index.html"
OUT = SITE / "uploads" / "최지현_portfolio.pdf"

# 슬라이드 아래 여백(꼬리말 자리)을 넘거나, 칸 안에서 잘린 요소를 찾는다.
CHECK = """
() => {
  const out = [];
  document.querySelectorAll('section.slide').forEach((s, i) => {
    const r = s.getBoundingClientRect();
    const limit = r.bottom - 44;  // 꼬리말(.foot) 위까지만 본문
    const bad = new Set();
    s.querySelectorAll('*').forEach(el => {
      if (el.closest('.foot')) return;
      const b = el.getBoundingClientRect();
      if (b.height === 0) return;
      if (b.bottom > limit + 1 || b.right > r.right - 40 + 1) {
        bad.add((el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : el.tagName.toLowerCase()) + ` +${Math.round(Math.max(b.bottom - limit, b.right - r.right + 40))}px`);
      }
    });
    if (bad.size) out.push({ slide: i + 1, items: [...bad].slice(0, 4) });
  });
  return out;
}
"""


def main() -> int:
    png_dir = None
    if "--png" in sys.argv:
        png_dir = Path(sys.argv[sys.argv.index("--png") + 1])
        png_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 810})
        page.goto(SRC.as_uri(), wait_until="networkidle")  # 폰트 · 이미지까지 받는다
        page.evaluate("document.fonts.ready.then(() => true)")
        page.emulate_media(media="print")
        n = page.evaluate("document.querySelectorAll('section.slide').length")
        over = page.evaluate(CHECK)

        if png_dir:
            for i, el in enumerate(page.query_selector_all("section.slide"), 1):
                el.screenshot(path=str(png_dir / f"slide{i:02d}.png"))

        page.pdf(path=str(OUT), prefer_css_page_size=True, print_background=True)
        browser.close()

    print(f"  {OUT.relative_to(SITE)}  {OUT.stat().st_size / 1e6:.2f}MB  (슬라이드 {n})")
    for o in over:
        print(f"  넘침 - {o['slide']:02d}쪽: {', '.join(o['items'])}")
    return 1 if over else 0


if __name__ == "__main__":
    raise SystemExit(main())
