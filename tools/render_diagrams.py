"""tools/diagrams/*.mmd 를 assets/ 의 PNG 로 굽는다.

원본 레포에 mermaid 코드만 있고 이미지가 없는 프로젝트용. optimize_assets.py 가
«레포에 있는 파일을 줄여 복사»라면, 이 스크립트는 «코드로만 있는 도식을 그림으로».

렌더러: Playwright(Chromium) + mermaid(jsDelivr). mmdc 는 이 환경에 없다.
배경은 흰색이다 — 카드 그림 칸의 다른 도식(K-Bridge)과 같은 규칙. 멱등하다.

    python tools/render_diagrams.py
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8")  # Windows cp949 콘솔
except Exception:
    pass

SITE = Path(__file__).resolve().parents[1]
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"

# 대상 파일: 원본 .mmd
DIAGRAMS: dict[str, str] = {
    "spendq/architecture.png": "tools/diagrams/spendq-architecture.mmd",
}

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<style>body{margin:0;background:#fff}#d{display:inline-block;padding:24px}</style>
<script src="%s"></script></head><body><div id="d"></div></body></html>""" % MERMAID


def render(src: str, page) -> bytes:
    page.set_content(PAGE)
    page.wait_for_function("window.mermaid !== undefined")
    page.evaluate(
        """async (code) => {
            mermaid.initialize({startOnLoad: false, theme: 'base', securityLevel: 'loose',
              themeVariables: {fontFamily: '"Pretendard", "Malgun Gothic", sans-serif', fontSize: '15px',
                               lineColor: '#6B7280', clusterBkg: '#FAFAFB', clusterBorder: '#C9CDD4', edgeLabelBackground: '#FFFFFF'},
              flowchart: {curve: 'basis', padding: 14, nodeSpacing: 36, rankSpacing: 56}});
            const {svg} = await mermaid.render('g', code);
            const d = document.getElementById('d');
            d.innerHTML = svg;
            // mermaid 는 svg 에 width:100%·max-width 를 건다 — inline-block 안에서 줄어들어 글자가 깨알이 된다.
            const el = d.querySelector('svg');
            el.style.maxWidth = 'none';
            el.setAttribute('width', el.viewBox.baseVal.width);
            el.setAttribute('height', el.viewBox.baseVal.height);
        }""",
        src,
    )
    png = page.locator("#d").screenshot()
    im = Image.open(io.BytesIO(png)).convert("RGB")
    buf = io.BytesIO()
    im.quantize(colors=256, method=Image.MEDIANCUT).save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(device_scale_factor=2)
        for dest_rel, src_rel in DIAGRAMS.items():
            data = render((SITE / src_rel).read_text(encoding="utf-8"), page)
            dest = SITE / "assets" / dest_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            w, h = Image.open(dest).size
            print(f"  {dest_rel:32s} {w}x{h} {len(data)/1e3:.0f}KB")
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
