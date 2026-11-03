"""cv/index.html(A4 이력서판)을 PDF 로 굽는다 -> uploads/최지현_이력서.pdf

슬라이드판(build_deck_pdf.py)과 같은 방식이다. 쪽은 794 x 1123px(A4) 고정이라, 굽기 전에 넘친 곳을
찾아 알려 준다. 넘친 쪽이 있으면 exit 1.

    python tools/build_cv_pdf.py            # PDF 굽기 + 넘침 검사
    python tools/build_cv_pdf.py --png DIR  # 쪽마다 PNG 도 저장 (눈으로 확인할 때)
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
SRC = SITE / "cv" / "index.html"
OUT = SITE / "uploads" / "최지현_이력서.pdf"

# 쪽 아래 여백(쪽 번호 자리)을 넘거나, 오른쪽으로 삐져나간 요소를 찾는다.
CHECK = """
() => {
  const out = [];
  document.querySelectorAll('section.page').forEach((s, i) => {
    const r = s.getBoundingClientRect();
    const limit = r.bottom - 36;  // 쪽 번호(.pno) 위까지만 본문
    const bad = new Set();
    s.querySelectorAll('*').forEach(el => {
      if (el.closest('.pno, .pno-l')) return;
      const b = el.getBoundingClientRect();
      if (b.height === 0) return;
      if (b.bottom > limit + 1 || b.right > r.right - 50 + 1) {
        bad.add((el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : el.tagName.toLowerCase()) + ` +${Math.round(Math.max(b.bottom - limit, b.right - r.right + 50))}px`);
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
        page = browser.new_page(viewport={"width": 900, "height": 1200})
        page.goto(SRC.as_uri(), wait_until="networkidle")  # 폰트 · 이미지까지 받는다
        page.evaluate("document.fonts.ready.then(() => true)")
        page.emulate_media(media="print")
        n = page.evaluate("document.querySelectorAll('section.page').length")
        over = page.evaluate(CHECK)

        if png_dir:
            for i, el in enumerate(page.query_selector_all("section.page"), 1):
                el.screenshot(path=str(png_dir / f"page{i}.png"))

        page.pdf(path=str(OUT), prefer_css_page_size=True, print_background=True)
        browser.close()

    print(f"  {OUT.relative_to(SITE)}  {OUT.stat().st_size / 1e6:.2f}MB  (쪽 {n})")
    for o in over:
        print(f"  넘침 - {o['slide']}쪽: {', '.join(o['items'])}")
    return 1 if over else 0


if __name__ == "__main__":
    raise SystemExit(main())
