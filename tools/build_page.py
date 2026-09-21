"""src/index.html + src/partials/** 를 이어 붙여 index.html 을 만든다.

    python tools/build_page.py           # index.html 다시 쓰기
    python tools/build_page.py --check   # index.html 이 src/ 와 같은지만 확인 (다르면 exit 1)

템플릿 안의 `<!-- @include 경로 -->` 한 줄이 그 파일 내용으로 바뀐다.
- 경로는 **그 줄이 들어 있는 파일** 기준 상대 경로다 (src/index.html 이면 src/ 기준).
- partial 은 들여쓰기 없이 적고, include 줄의 들여쓰기가 모든 줄 앞에 붙는다.
- partial 안에서도 include 를 쓸 수 있다 (01-qmesh/card.html 이 서브카드를 부른다).

GitHub Pages 배포 워크플로도 이 스크립트를 돌리므로, 커밋 전에 빌드를 잊어도
사이트는 src/ 기준으로 나간다. 다만 로컬에서 index.html 을 열어 보거나
PDF 를 구우려면 먼저 빌드해야 한다.
"""
from __future__ import annotations

import sys as _sys
for _stream in (_sys.stdout, _sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")  # Windows cp949 콘솔에서 한국어 출력이 죽는다
    except Exception:
        pass

import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
SRC = SITE / "src"
OUT = SITE / "index.html"
INCLUDE = re.compile(r"^(\s*)<!-- @include (\S+) -->\s*$")


def expand(path: Path, stack: tuple[Path, ...] = ()) -> list[str]:
    if path in stack:
        sys.exit(f"include 순환: {' -> '.join(p.name for p in stack + (path,))}")
    if not path.is_file():
        where = stack[-1].relative_to(SRC) if stack else "?"
        sys.exit(f"include 대상이 없다: {path.relative_to(SITE)} (불린 곳: src/{where})")
    out: list[str] = []
    for line in path.read_text(encoding="utf-8").split("\n"):
        m = INCLUDE.match(line)
        if not m:
            out.append(line)
            continue
        indent, rel = m.groups()
        child = expand((path.parent / rel).resolve(), stack + (path,))
        while child and child[-1] == "":
            child.pop()
        out += [indent + c if c.strip() else "" for c in child]
    return out


def build() -> str:
    return "\n".join(expand(SRC / "index.html"))


def main() -> None:
    html = build()
    if "--check" in sys.argv:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current.replace("\r\n", "\n") != html:
            print("index.html 이 src/ 와 다르다 - python tools/build_page.py 를 실행하세요")
            sys.exit(1)
        print("index.html 이 src/ 와 같다")
        return
    OUT.write_text(html, encoding="utf-8", newline="\n")
    print(f"index.html 생성 - {html.count(chr(10)) + 1}줄")


if __name__ == "__main__":
    main()
