"""index.html / print/index.html 의 구조 불변식 검사.

정적 사이트라 테스트 프레임워크가 없다. 여기서 잡는 것은 전부
「브라우저에서 열어보기 전에는 안 보이는데, 열면 조용히 깨져 있는」 종류다.

C1  data-modal="X" 에 대응하는 id="X" 가 있는가      -- 모달이 안 열리는 것
C2  data-ko 와 data-en 이 쌍으로 있는가              -- 전환 시 문구 소실
C3  data-ko 요소 안에 <img>/<svg> 가 없는가          -- applyLang() 이 innerHTML 로 지운다
C4  data-src 경로의 파일이 실재하는가                -- 죽은 이미지
C5  모달 section 안에 data-count 가 없는가           -- 숨김 상태에선 발화하지 않아 0 으로 남는다
"""
from __future__ import annotations

import sys as _sys
for _stream in (_sys.stdout, _sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")  # Windows cp949 콘솔에서 한국어 출력이 죽는다
    except Exception:
        pass

import sys
from html.parser import HTMLParser
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
TARGETS = ["index.html", "print/index.html"]

VOID = {"img", "br", "hr", "input", "meta", "link", "source", "area", "base", "col", "embed",
        "param", "track", "wbr"}
MEDIA = {"img", "svg", "picture", "video", "canvas"}


class Collector(HTMLParser):
    """data-* 속성과 요소 중첩 관계를 모은다."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.modal_refs: list[tuple[str, int]] = []
        self.ids: set[str] = set()
        self.lang_issues: list[tuple[str, int]] = []
        self.srcs: list[tuple[str, int]] = []
        self.media_in_lang: list[tuple[str, int]] = []
        self.count_in_modal: list[tuple[str, int]] = []
        self._lang_depth = 0
        self._section_depth = 0
        self._stack: list[tuple[str, bool, bool]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}
        line = self.getpos()[0]

        if "data-modal" in a:
            self.modal_refs.append((a["data-modal"], line))
        if "id" in a:
            self.ids.add(a["id"])
        if "data-src" in a:
            self.srcs.append((a["data-src"], line))

        has_ko, has_en = "data-ko" in a, "data-en" in a
        if has_ko != has_en:
            which = "data-en" if has_ko else "data-ko"
            self.lang_issues.append((f"<{tag}> 에 {which} 가 없다", line))

        if self._lang_depth > 0 and tag in MEDIA:
            self.media_in_lang.append((f"data-ko 요소 안의 <{tag}>", line))
        if self._section_depth > 0 and "data-count" in a:
            self.count_in_modal.append(("모달 안의 data-count", line))

        opens_lang = has_ko
        opens_section = tag == "section" and a.get("id", "").startswith("f-")
        if tag not in VOID:
            self._stack.append((tag, opens_lang, opens_section))
            if opens_lang:
                self._lang_depth += 1
            if opens_section:
                self._section_depth += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # <img ... /> 같은 자기닫음 태그도 속성 검사는 받아야 한다
        self.handle_starttag(tag, attrs)
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                self._pop_from(i)
                return

    def _pop_from(self, i: int) -> None:
        for _, opens_lang, opens_section in self._stack[i:]:
            if opens_lang:
                self._lang_depth -= 1
            if opens_section:
                self._section_depth -= 1
        del self._stack[i:]

    def handle_endtag(self, tag: str) -> None:
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                self._pop_from(i)
                return


def check(path: Path) -> list[str]:
    c = Collector()
    c.feed(path.read_text(encoding="utf-8"))
    rel = path.relative_to(SITE).as_posix()
    out: list[str] = []

    for mid, line in c.modal_refs:                                    # C1
        if mid not in c.ids:
            out.append(f'{rel}:{line}  C1 data-modal="{mid}" 에 대응하는 id 가 없다')
    for msg, line in c.lang_issues:                                   # C2
        out.append(f"{rel}:{line}  C2 {msg}")
    for msg, line in c.media_in_lang:                                 # C3
        out.append(f"{rel}:{line}  C3 {msg} -- applyLang() 이 innerHTML 로 지운다")
    for src, line in c.srcs:                                          # C4
        if not (SITE / src).exists():
            out.append(f'{rel}:{line}  C4 data-src="{src}" 파일이 없다')
    for msg, line in c.count_in_modal:                                # C5
        out.append(f"{rel}:{line}  C5 {msg} -- 숨김 상태에선 발화하지 않아 0 으로 남는다")
    return out


def main() -> int:
    problems: list[str] = []
    for name in TARGETS:
        p = SITE / name
        if not p.exists():
            problems.append(f"{name} 이 없다")
            continue
        problems.extend(check(p))

    if problems:
        print(f"위반 {len(problems)}건:\n", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1
    print(f"통과 -- {', '.join(TARGETS)} 구조 불변식 5종 이상 없음")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
