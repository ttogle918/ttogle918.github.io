# QMesh 중첩 드롭다운 + 기능 모달 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `index.html`의 QMesh 카드 안에 FinAllQ·InsuQ·MaintQ 하위 드롭다운을 만들고, 각 프로젝트의 기능을 다이어그램·흐름·실제 화면 캡처가 담긴 모달로 열 수 있게 한다. SpendQ 카드를 실측 상태로 교체하고 인쇄본을 동기화한다.

**Architecture:** 빌드 없는 단일 파일 정적 사이트. 하위 드롭다운은 기존 `.pcard` 아코디언과 같은 클래스 토글 패턴을 재사용한다. 모달 본문은 처음부터 DOM에 있고 `hidden`만 토글해 기존 `applyLang()`이 그대로 닿게 한다(복제 금지). 데모 자산은 Pillow로 최적화해 이 레포에 담고 모달을 열 때만 로드한다.

**Tech Stack:** 순수 HTML/CSS/JS (인라인, 빌드 없음) · Python 3.13 + Pillow 12.3.0 (자산 최적화·검증 스크립트)

**설계서:** [`docs/superpowers/specs/2026-09-11-qmesh-nested-cards-and-feature-modals-design.md`](../specs/2026-09-11-qmesh-nested-cards-and-feature-modals-design.md) — 이하 **SPEC**. 콘텐츠 사실은 전부 SPEC §3에 있다.

---

## 진행 상황 (2026-09-11 중단 시점)

**Task 1~10 완료 · Task 11(종단 검증)만 남음 · 아직 push 하지 않았다.**

| Task | 커밋 | 확인한 것 |
|---|---|---|
| 1 자산 | `423e7c4` | 26종 · 26.9MB → 5.7MB(21%) · 원본 없으면 exit 1 · 공개 안전성 육안 확인 |
| 2 검사 하네스 | `cbeea0e` | 뮤턴트 5종 전부 잡음 |
| 3 CSS | `a3c8b16` | 기존 카드 8개 무손상 |
| 4 JS | `673230e` | 초기 GIF 요청 0건 · ESC/배경/✕ · **모달 연 상태 KO/EN 전환** |
| 5 QMesh | `3a8d09a` | 모달 2 · 3경로→5경로 정정 |
| 6 FinAllQ | `db90c99` | 모달 7 · 기능 먼저, 그 아래 "왜 LLM이 없는가" |
| 7 InsuQ | `a005070` | 모달 4 · LangGraph 흐름도 · 다이어그램 CSS 공용화 |
| 8 MaintQ | `4036680` | 모달 7 · 기능 먼저, 그 아래 MCP |
| 9 SpendQ + AS_OF | `6ed963b` | 실측 상태로 교체 · 기준일 2026-09-11 |
| 10 인쇄본 | `635e05d` | 9장 전부 한 페이지에 맞음(297mm 실측) |

**Task 11에서 이미 끝난 것**
- `tools/check_page.py` 통과
- `tools/optimize_assets.py` 재실행 후 `git status` 비어 있음(멱등성 확인)
- 버튼 20 / 모달 20 완전 대응 (양쪽 차집합 0)
- 모달 20개 전수 열림 · GIF `src` 주입 · 텍스트 겹침 0 · viewBox 넘침 0

**Task 11에서 남은 것** — 아래 Step 3~6
- 브라우저 전수 확인 7항목(중첩 토글·모달 3경로 닫기·모달 내 언어 전환·GIF 지연 로딩·다크 테마·400px 모바일·인쇄 미리보기)
- SPEC §3 수치를 `resume/` 원본과 1:1 재대조
- `README.md` 갱신(`assets/`·`tools/` 규약, AS_OF 예시)
- **최종 커밋 + `git push origin master`**, 배포본에서 재확인

**재개 방법**
```bash
cd /c/Users/ttogl/workspace/ttogle918.github.io
python -m http.server 8899    # http://localhost:8899/index.html
python tools/check_page.py
```

**작업 중 알게 된 것 (재개 시 유의)**
- Python 이 `index.html` 을 다시 쓰면 내용이 같아도 `git status` 가 `M` 으로 뜬다 — blob 해시로 대조할 것(Task 2 Step 4의 함정 상자 참고)
- 파일을 건드리는 정규식은 앵커를 좁히고 **적용 전에 매칭 수를 먼저 확인**할 것. 넓은 `<style>.*?</style>` 하나로 메인 스타일시트 2,170줄을 날린 적이 있다(커밋본에서 복구 완료)
- SVG 안에 `style` 요소를 두면 규칙이 **문서 전역**이 된다. 새 다이어그램은 반드시 `.fdiag .dg-*` 공용 어휘를 쓸 것 — 인라인 스타일을 다시 넣지 말 것

---

## Global Constraints

이 섹션의 규칙은 **모든 태스크에 암묵적으로 포함**된다.

1. **`applyLang()`은 `el.innerHTML = v`로 덮어쓴다** (`index.html:3125`). 따라서 **`data-ko`를 가진 요소 안에 `<img>`·`<svg>`를 두면 언어 전환 시 사라진다.** `data-ko`는 **텍스트만 담는 말단 요소**에만 붙인다.
2. 모든 사용자 문구는 `data-ko` / `data-en` **두 속성 + 태그 안쪽 내용** 3곳을 함께 쓴다.
3. **모달 본문은 복제하지 않는다.** `cloneNode`로 만든 노드는 `applyLang()`을 못 받는다.
4. **모달 안에 `data-count`를 쓰지 않는다.** 카운터 IntersectionObserver는 `display:none` 상태에서 발화하지 않는다. 모달 수치는 정적 텍스트로 적는다.
5. 색은 전부 CSS 변수를 쓴다: `--ink` `--text` `--muted` `--faint` `--line` `--line-2` `--panel` `--paper` `--accent` `--accent-soft` `--gold` `--gold-soft` `--gold-ink` `--gold-line` `--ok` `--mono` `--radius`. SVG는 `currentColor`와 이 변수만 쓴다 — 하드코딩 색상 금지(다크 테마에서 깨진다).
6. **스프린트 번호를 카드 본문에 쓰지 않는다** (README 경고 — "Sprint 4"가 6일 만에 "Sprint 21"이 됐다).
7. **분모가 다른 수치를 나란히 놓지 않는다** — InsuQ 트랙1(27문항)/트랙4(52문항), QMesh "5경로"(검증된 통신 경로)/"6종"(MaintQ 발신 스킬 수).
8. 기간은 SPEC §3을 따른다. git 날짜로 단언하지 않는다.
9. **Python 스크립트는 stdout/stderr 를 UTF-8 로 재설정한다.** Windows 기본 콘솔이 cp949 라
   한국어·em dash(`—`)를 출력하는 순간 `UnicodeEncodeError` 로 죽는다(실측 확인). 두 스크립트 모두
   `from __future__ import annotations` 바로 아래에 다음을 넣는다:
   ```python
   import sys as _sys
   for _stream in (_sys.stdout, _sys.stderr):
       try:
           _stream.reconfigure(encoding="utf-8")
       except Exception:
           pass
   ```
10. 하위 프로세스로 Python 스크립트를 돌릴 때는 `subprocess.run(..., encoding="utf-8")` 을 준다.
11. 커밋 메시지는 한국어. 끝에 다음 두 줄을 붙인다:
   ```
   Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
   Claude-Session: https://claude.ai/code/session_0178E3o2o2BuCsyArzc1XSsr
   ```

---

## File Structure

| 파일 | 책임 |
|---|---|
| `tools/optimize_assets.py` | **신규.** 각 프로젝트 레포의 원본 GIF/JPG를 읽어 `assets/` 아래로 최적화 복사. 멱등 재실행 |
| `tools/check_page.py` | **신규.** `index.html`·`print/index.html`의 구조 불변식 검사. Global Constraints 1·2·4와 링크 무결성을 기계로 강제 |
| `assets/maintq/*.gif` | **신규.** 기능 GIF 7종 |
| `assets/insuq/*.gif` | **신규.** 기능 GIF 4종 |
| `assets/finallq/*.jpg` | **신규.** 화면 캡처 13장 |
| `assets/qmesh/*.gif` | **신규.** A2A GIF 2종 |
| `index.html` | **수정.** CSS 블록(`.pcard` 규칙 뒤) · 프로젝트 섹션 · JS 블록(6번 아코디언 뒤) · `AS_OF` · 인쇄 CSS |
| `print/index.html` | **수정.** Q 시리즈·SpendQ 본문을 같은 사실로 동기화 (중첩 없이 펼친 형태) |

`qmesh/assets/` 3종은 `qmesh/` 랜딩이 참조 중이므로 **건드리지 않는다.**

---

## Task 1: 자산 최적화 파이프라인

**Files:**
- Create: `tools/optimize_assets.py`
- Create: `assets/maintq/` · `assets/insuq/` · `assets/finallq/` · `assets/qmesh/` (스크립트가 생성)

**Interfaces:**
- Produces: 아래 26개 파일 경로. 이후 모든 태스크가 `assets/<proj>/<name>`으로 참조한다.

| 대상 경로 | 원본 |
|---|---|
| `assets/maintq/unknown-error-code.gif` | `MaintQ/docs/demo-captures/assets/unknown-error-code.gif` |
| `assets/maintq/alternative-parts.gif` | `MaintQ/docs/demo-captures/assets/alternative-parts.gif` |
| `assets/maintq/repeat-failure-hold.gif` | `MaintQ/docs/demo-captures/assets/repeat-failure-hold.gif` |
| `assets/maintq/disposal-precheck.gif` | `MaintQ/docs/demo-captures/assets/disposal-precheck.gif` |
| `assets/maintq/disposal-evidence-bundle.gif` | `MaintQ/docs/demo-captures/assets/disposal-evidence-bundle.gif` |
| `assets/maintq/deadline-risk-grade.gif` | `MaintQ/docs/demo-captures/assets/deadline-risk-grade.gif` |
| `assets/maintq/expenditure-classification.gif` | `MaintQ/docs/demo-captures/assets/expenditure-classification.gif` |
| `assets/insuq/grounded-citation.gif` | `A2A_Q/docs/presentation/assets/insuq-qa-grounded-citation.gif` |
| `assets/insuq/refusal-gate.gif` | `A2A_Q/docs/presentation/assets/insuq-qa-refusal-gate.gif` |
| `assets/insuq/ambiguous-domain-merge.gif` | `A2A_Q/docs/presentation/assets/insuq-qa-ambiguous-domain-merge.gif` |
| `assets/insuq/claim-approval.gif` | `A2A_Q/docs/presentation/assets/insuq-pro-inbox-claim-approval.gif` |
| `assets/qmesh/request-settlement.gif` | `A2A_Q/docs/presentation/assets/04-maintq-finallq-request-settlement.gif` |
| `assets/qmesh/approval-inbox-arrival.gif` | `A2A_Q/docs/presentation/assets/02b-finallq-approval-inbox-a2a-arrival.gif` |
| `assets/finallq/01_login.jpg` … `13_ai_chat_fail_soft.jpg` (13장) | `FinAllQ/docs/img/*.jpg` (번호 순서 그대로, 타임스탬프 접미사 제거) |

- [ ] **Step 1: 스크립트 작성**

`tools/optimize_assets.py`:

```python
"""각 프로젝트 레포의 데모 자산을 이 레포의 assets/ 로 최적화 복사한다.

왜 이 레포에 담는가: MaintQ·InsuQ·FinAllQ·SpendQ 레포가 전부 private 이라
raw 핫링크도 Pages 리다이렉트도 성립하지 않는다. 파일 단위로 고른 것만
public 인 이 레포에 담는 것이 곧 선택적 공개다. (설계서 §2)

원본은 각 프로젝트 레포에 그대로 남는다 — 화질이 아쉬우면 MAXW 를 올려
다시 돌리면 된다. 멱등하다.
"""
from __future__ import annotations

import sys as _sys
for _stream in (_sys.stdout, _sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")  # Windows cp949 콘솔에서 한국어 출력이 죽는다
    except Exception:
        pass

import io
import os
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageSequence

# 모달 표시 폭은 최대 ~760px 다. 900px 면 고해상도 화면에서도 충분하고,
# 1280~1568px 원본 대비 용량이 약 1/5 로 떨어진다(실측).
MAXW = 900
COLORS = 128

WS = Path(__file__).resolve().parents[2]   # .../workspace
SITE = Path(__file__).resolve().parents[1]  # .../ttogle918.github.io

GIFS: dict[str, str] = {
    "maintq/unknown-error-code.gif": "MaintQ/docs/demo-captures/assets/unknown-error-code.gif",
    "maintq/alternative-parts.gif": "MaintQ/docs/demo-captures/assets/alternative-parts.gif",
    "maintq/repeat-failure-hold.gif": "MaintQ/docs/demo-captures/assets/repeat-failure-hold.gif",
    "maintq/disposal-precheck.gif": "MaintQ/docs/demo-captures/assets/disposal-precheck.gif",
    "maintq/disposal-evidence-bundle.gif": "MaintQ/docs/demo-captures/assets/disposal-evidence-bundle.gif",
    "maintq/deadline-risk-grade.gif": "MaintQ/docs/demo-captures/assets/deadline-risk-grade.gif",
    "maintq/expenditure-classification.gif": "MaintQ/docs/demo-captures/assets/expenditure-classification.gif",
    "insuq/grounded-citation.gif": "A2A_Q/docs/presentation/assets/insuq-qa-grounded-citation.gif",
    "insuq/refusal-gate.gif": "A2A_Q/docs/presentation/assets/insuq-qa-refusal-gate.gif",
    "insuq/ambiguous-domain-merge.gif": "A2A_Q/docs/presentation/assets/insuq-qa-ambiguous-domain-merge.gif",
    "insuq/claim-approval.gif": "A2A_Q/docs/presentation/assets/insuq-pro-inbox-claim-approval.gif",
    "qmesh/request-settlement.gif": "A2A_Q/docs/presentation/assets/04-maintq-finallq-request-settlement.gif",
    "qmesh/approval-inbox-arrival.gif": "A2A_Q/docs/presentation/assets/02b-finallq-approval-inbox-a2a-arrival.gif",
}

# FinAllQ 스크린샷은 이미 작아서(27~54KB) 최적화 없이 이름만 정리해 복사한다.
FINALLQ_SRC = "FinAllQ/docs/img"
FINALLQ: dict[str, str] = {
    "01_login.jpg": "01_login_260823_221728.jpg",
    "02_dashboard.jpg": "02_dashboard_260823_221904.jpg",
    "03_loan_list.jpg": "03_loan_list_260823_221947.jpg",
    "04_loan_assessment.jpg": "04_loan_assessment_260823_222002.jpg",
    "05_loan_disbursement.jpg": "05_loan_disbursement_260823_222241.jpg",
    "06_transfer_apply_form.jpg": "06_transfer_apply_form_260823_222350.jpg",
    "07_transfer_pending_approval.jpg": "07_transfer_pending_approval_260823_222442.jpg",
    "08_manager_approval_queue.jpg": "08_manager_approval_queue_260823_222529.jpg",
    "09_transfer_2fa_required.jpg": "09_transfer_2fa_required_260823_222722.jpg",
    "10_smishing_empty.jpg": "10_smishing_empty_260823_222814.jpg",
    "11_smishing_result.jpg": "11_smishing_result_260823_222920.jpg",
    "12_ai_chat_out_of_scope.jpg": "12_ai_chat_out_of_scope_260823_223051.jpg",
    "13_ai_chat_fail_soft.jpg": "13_ai_chat_fail_soft_260823_223159.jpg",
}


def shrink_gif(src: Path, maxw: int = MAXW, colors: int = COLORS) -> bytes:
    im = Image.open(src)
    frames, durations = [], []
    for frame in ImageSequence.Iterator(im):
        f = frame.convert("RGBA")
        if f.width > maxw:
            f = f.resize((maxw, round(f.height * maxw / f.width)), Image.LANCZOS)
        frames.append(f.convert("P", palette=Image.ADAPTIVE, colors=colors))
        durations.append(frame.info.get("duration", im.info.get("duration", 100)))
    buf = io.BytesIO()
    frames[0].save(
        buf, format="GIF", save_all=True, append_images=frames[1:],
        duration=durations, loop=0, optimize=True, disposal=2,
    )
    return buf.getvalue()


def main() -> int:
    missing: list[str] = []
    total_before = total_after = 0

    for dest_rel, src_rel in GIFS.items():
        src = WS / src_rel
        if not src.exists():
            missing.append(src_rel)
            continue
        dest = SITE / "assets" / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        data = shrink_gif(src)
        dest.write_bytes(data)
        before, after = src.stat().st_size, len(data)
        total_before += before
        total_after += after
        print(f"  {dest_rel:42s} {before/1e6:5.2f}MB -> {after/1e6:5.2f}MB ({after/before*100:3.0f}%)")

    for dest_name, src_name in FINALLQ.items():
        src = WS / FINALLQ_SRC / src_name
        if not src.exists():
            missing.append(f"{FINALLQ_SRC}/{src_name}")
            continue
        dest = SITE / "assets" / "finallq" / dest_name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        size = src.stat().st_size
        total_before += size
        total_after += size
        print(f"  finallq/{dest_name:34s} {size/1e3:5.0f}KB (복사)")

    print(f"\n합계 {total_before/1e6:.1f}MB -> {total_after/1e6:.1f}MB "
          f"({total_after/total_before*100:.0f}%)")

    if missing:
        print("\n원본을 찾지 못했다:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: 실행**

```bash
cd /c/Users/ttogl/workspace/ttogle918.github.io && python tools/optimize_assets.py
```

기대: 26개 줄이 출력되고 마지막에 `합계 26.9MB -> 5.x MB (20%)`, 종료 코드 0.
(검증된 비율: `disposal-precheck` 21% · `alternative-parts` 24% · `grounded-citation` 13% · `request-settlement` 19%)

- [ ] **Step 3: 실패 경로 확인 — 원본이 없으면 죽는가**

```bash
python - <<'PY'
import re, pathlib
p = pathlib.Path('tools/optimize_assets.py')
s = p.read_text(encoding='utf-8')
bad = s.replace('MaintQ/docs/demo-captures/assets/unknown-error-code.gif',
                'MaintQ/docs/demo-captures/assets/NOPE.gif')
pathlib.Path('tools/_tmp_check.py').write_text(bad, encoding='utf-8')
PY
python tools/_tmp_check.py; echo "exit=$?"
rm tools/_tmp_check.py
```

기대: `원본을 찾지 못했다:` 와 `exit=1`.
**이 확인을 건너뛰지 말 것** — 원본 경로가 바뀌어도 조용히 통과하면 자산이 빈 채로 배포된다.

- [ ] **Step 4: 공개 안전성 육안 확인**

```bash
ls -la assets/maintq assets/insuq assets/finallq assets/qmesh
du -sh assets
```

26개 파일이 전부 있는지, 합계가 6MB 이하인지 확인한다.
**그 다음 `assets/finallq/*.jpg` 13장과 GIF 몇 개를 실제로 열어 본다** — 이 레포는 public 이므로
실제 자격증명·실고객 데이터가 찍혀 있지 않은지 눈으로 본다. (문서상으로는 전부 목업·시드다)

- [ ] **Step 5: 커밋**

```bash
git add tools/optimize_assets.py assets
git commit -m "$(cat <<'EOF'
데모 자산 26종을 이 레포로 이관 (26.9MB -> 5.4MB)

MaintQ 7 · InsuQ 4 · QMesh 2 GIF 와 FinAllQ 화면 13장.
네 소스 레포가 전부 private 이라 raw 핫링크도 Pages 리다이렉트도
성립하지 않는다 — 파일 단위로 골라 담는 것이 곧 선택적 공개다.

Pillow 로 폭 900px 제한 + 팔레트 128색. 원본은 각 레포에 그대로 남는다.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0178E3o2o2BuCsyArzc1XSsr
EOF
)"
```

---

## Task 2: 구조 검사 하네스

정적 사이트라 테스트 프레임워크가 없다. 이 프로젝트에서 **실제로 깨질 수 있는 것**을 기계로 잡는 검사를 먼저 만든다. 이후 모든 태스크가 이 스크립트로 자기 작업을 검증한다.

**Files:**
- Create: `tools/check_page.py`

**Interfaces:**
- Produces: `python tools/check_page.py` — 위반 시 종료 코드 1 + 위반 목록.

검사 5종:

| # | 불변식 | 왜 |
|---|---|---|
| C1 | 모든 `data-modal="X"` 에 대응하는 `id="X"` 가 있다 | 모달이 안 열리는 것을 배포 전에 잡는다 |
| C2 | `data-ko` 가 있으면 `data-en` 도 있다 (역도 성립) | 한쪽만 있으면 언어 전환 시 문구가 사라진다 |
| C3 | **`data-ko` 요소 안에 `<img>`·`<svg>` 가 없다** | `applyLang()` 이 `innerHTML` 을 덮어써 지운다 (Global Constraint 1) |
| C4 | 모든 `data-src` 경로의 파일이 실재한다 | 죽은 이미지 경로를 잡는다 |
| C5 | 모달 `<section>` 안에 `data-count` 가 없다 | 숨김 상태에선 카운터가 발화하지 않아 영원히 0 이다 |

- [ ] **Step 1: 검사 스크립트 작성**

`tools/check_page.py`:

```python
"""index.html / print/index.html 의 구조 불변식 검사.

정적 사이트라 테스트 프레임워크가 없다. 여기서 잡는 것은 전부
「브라우저에서 열어보기 전에는 안 보이는데, 열면 조용히 깨져 있는」 종류다.
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
from html.parser import HTMLParser
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
TARGETS = ["index.html", "print/index.html"]


class Collector(HTMLParser):
    """data-* 속성과 요소 중첩 관계를 모은다."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.modal_refs: list[tuple[str, int]] = []   # (id, line)
        self.ids: set[str] = set()
        self.lang_issues: list[tuple[str, int]] = []  # (msg, line)
        self.srcs: list[tuple[str, int]] = []
        self.media_in_lang: list[tuple[str, int]] = []
        self.count_in_modal: list[tuple[str, int]] = []
        self._lang_depth = 0       # data-ko 요소 안에 있는 깊이
        self._section_depth = 0    # 모달 section 안에 있는 깊이
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

        if self._lang_depth > 0 and tag in ("img", "svg", "picture", "video"):
            self.media_in_lang.append((f"data-ko 요소 안의 <{tag}>", line))
        if self._section_depth > 0 and "data-count" in a:
            self.count_in_modal.append((f"모달 안의 data-count", line))

        opens_lang = has_ko
        opens_section = tag == "section" and a.get("id", "").startswith("f-")
        # void 요소는 스택에 쌓지 않는다
        if tag not in ("img", "br", "hr", "input", "meta", "link", "source"):
            self._stack.append((tag, opens_lang, opens_section))
            if opens_lang:
                self._lang_depth += 1
            if opens_section:
                self._section_depth += 1

    def handle_endtag(self, tag: str) -> None:
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                for _, ol, os_ in self._stack[i:]:
                    if ol:
                        self._lang_depth -= 1
                    if os_:
                        self._section_depth -= 1
                del self._stack[i:]
                return


def check(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    c = Collector()
    c.feed(text)
    rel = path.relative_to(SITE).as_posix()
    out: list[str] = []

    for mid, line in c.modal_refs:                                   # C1
        if mid not in c.ids:
            out.append(f"{rel}:{line}  C1 data-modal=\"{mid}\" 에 대응하는 id 가 없다")
    for msg, line in c.lang_issues:                                  # C2
        out.append(f"{rel}:{line}  C2 {msg}")
    for msg, line in c.media_in_lang:                                # C3
        out.append(f"{rel}:{line}  C3 {msg} — applyLang() 이 innerHTML 로 지운다")
    for src, line in c.srcs:                                         # C4
        if not (SITE / src).exists():
            out.append(f"{rel}:{line}  C4 data-src=\"{src}\" 파일이 없다")
    for msg, line in c.count_in_modal:                               # C5
        out.append(f"{rel}:{line}  C5 {msg} — 숨김 상태에선 발화하지 않아 0 으로 남는다")
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
    print(f"통과 — {', '.join(TARGETS)} 구조 불변식 5종 이상 없음")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: 현재 상태로 실행 — 기준선 확보**

```bash
python tools/check_page.py; echo "exit=$?"
```

기대: `통과` + `exit=0`. **여기서 위반이 나오면 기존 파일에 이미 문제가 있는 것**이므로,
그 위반을 먼저 기록하고(고치지는 말 것 — 이번 범위 밖일 수 있다) 진행한다.

- [ ] **Step 3: 검사가 실제로 잡는지 확인 (뮤턴트)**

검사가 눈이 멀었는지 확인한다. 5종 각각에 위반을 일부러 심어 **실제로 빨개지는지** 본다.

```bash
python - <<'PY'
import pathlib, subprocess, sys, shutil
p = pathlib.Path('index.html'); orig = p.read_text(encoding='utf-8')
mutants = {
 'C1': ('<div class="projects">', '<div class="projects"><button data-modal="NOPE-XYZ">x</button>'),
 'C2': ('<div class="projects">', '<div class="projects"><p data-ko="가">가</p>'),
 'C3': ('<div class="projects">', '<div class="projects"><p data-ko="가" data-en="a"><img src="x.png"></p>'),
 'C4': ('<div class="projects">', '<div class="projects"><img data-src="assets/NOPE.gif">'),
 'C5': ('<div class="projects">', '<div class="projects"><section id="f-x"><span data-count="3">0</span></section>'),
}
fail = []
for name, (old, new) in mutants.items():
    p.write_text(orig.replace(old, new, 1), encoding='utf-8')
    r = subprocess.run([sys.executable, 'tools/check_page.py'],
                       capture_output=True, text=True, encoding='utf-8')
    caught = r.returncode != 0 and name in (r.stderr or '')
    if not caught:
        fail.append(name)
    print(f'{name}: {"잡음" if caught else "놓침"}')
p.write_text(orig, encoding='utf-8')
print('\n' + ('전부 잡는다' if not fail else f'못 잡는 검사: {fail}'))
sys.exit(1 if fail else 0)
PY
```

기대: 5종 전부 `잡음`, 마지막 줄 `전부 잡는다`, 종료 코드 0.
마지막에 `index.html` 이 원상복구되므로 `git diff --stat index.html` 이 비어야 한다.

- [ ] **Step 4: 원상복구 확인**

```bash
git checkout -- index.html
git status --short index.html; echo "exit=$?"
python -c "d=open('index.html','rb').read(); print('CRLF:', d.count(b'\r\n'), 'bare LF:', d.count(b'\n')-d.count(b'\r\n'))"
```

기대: `git status` 출력 없음 · `exit=0` · `bare LF: 0`.

> ⚠️ **함정 (계획 작성 중 실제로 걸렸다).** Python 이 `write_text()` 로 `index.html` 을 다시 쓰면
> 내용이 같아도 mtime 이 바뀌어 `git status` 가 `M index.html` 로 뜬다. `git diff` 는 비어 있어서
> "변경 없음"으로 착각하기 쉽다. 이 레포는 작업 트리가 CRLF 이므로 **blob 해시로 확인**하는 것이 확실하다:
>
> ```bash
> test "$(git hash-object index.html)" = "$(git ls-files -s index.html | awk '{print $2}')" \
>   && echo "내용 동일" || echo "내용이 다르다"
> ```
>
> `git diff --stat` 만 보고 넘어가지 말 것 — `git checkout -- index.html` 로 확실히 되돌린다.

- [ ] **Step 5: 커밋**

```bash
git add tools/check_page.py
git commit -m "$(cat <<'EOF'
구조 검사 하네스 추가 — 브라우저를 열기 전엔 안 보이는 5종을 잡는다

C1 data-modal 대응 id · C2 data-ko/en 쌍 · C3 data-ko 안의 <img>/<svg>
(applyLang 이 innerHTML 로 지운다) · C4 죽은 data-src · C5 모달 안 data-count
(숨김 상태에선 발화하지 않아 0 으로 남는다).

뮤턴트 5종으로 검사가 실제로 빨개지는 것을 확인한 뒤 넣었다.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0178E3o2o2BuCsyArzc1XSsr
EOF
)"
```

---

## Task 3: 하위 드롭다운 · 모달 CSS

**Files:**
- Modify: `index.html` — `.pc-actions` 규칙 뒤 (현재 `index.html:1289` 근처), 인쇄 블록 앞

**Interfaces:**
- Produces: 클래스 `.subcard` `.sub-top` `.sub-badge` `.sub-headings` `.sub-code` `.sub-title` `.sub-meta` `.sub-caret` `.sub-body` `.sub-inner` `.featlist` `.feat` `.fmodal` `.fmodal-card` `.fmodal-head` `.fmodal-x` `.fmodal-body` `.fmodal-fig` `.fdiag` `.fsteps`

- [ ] **Step 1: 하위 카드 CSS 삽입**

`.pc-actions { … }` 규칙 **바로 뒤**에 삽입:

```css
    /* ─── 하위 프로젝트 카드 (QMesh 안의 FinAllQ·InsuQ·MaintQ) ───
       기존 .pcard 아코디언과 같은 토글 패턴. 톤만 한 단계 낮춘다. */
    .subcards {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-top: 6px
    }

    .subcard {
      background: var(--panel);
      border: 1px solid var(--line);
      border-left: 3px solid var(--accent-soft);
      border-radius: 10px;
      overflow: hidden;
      transition: border-color .25s
    }

    .subcard:hover {
      border-left-color: var(--accent)
    }

    .subcard.open {
      border-left-color: var(--accent)
    }

    .sub-top {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      padding: 14px 16px;
      cursor: pointer;
      transition: background .2s
    }

    .sub-top:hover {
      background: color-mix(in srgb, var(--accent) 4%, transparent)
    }

    .sub-headings {
      flex: 1;
      min-width: 0
    }

    .sub-code {
      font-family: var(--mono);
      font-size: 11px;
      color: var(--accent);
      letter-spacing: .05em;
      margin-bottom: 3px
    }

    .sub-title {
      font-size: 15px;
      font-weight: 700;
      color: var(--ink);
      margin: 0 0 5px
    }

    .sub-meta {
      font-family: var(--mono);
      font-size: 10.5px;
      color: var(--muted)
    }

    .sub-caret {
      flex: none;
      color: var(--faint);
      font-size: 10px;
      margin-top: 4px;
      transition: transform .3s
    }

    .subcard.open .sub-caret {
      transform: rotate(90deg);
      color: var(--accent)
    }

    .sub-body {
      max-height: 0;
      overflow: hidden;
      transition: max-height .45s cubic-bezier(.22, 1, .36, 1)
    }

    .subcard.open .sub-body {
      max-height: 4000px
    }

    .sub-inner {
      padding: 2px 16px 18px;
      border-top: 1px solid var(--line-2)
    }

    /* 하위 카드를 품은 카드는 상한을 올린다 — 기본 1400px 이면 중첩이 잘린다.
       이 파일은 이미 :has() 를 쓰고 있다(.pc-grid:has(.pc-figure.wide)). */
    .pcard.open .pc-body:has(.subcard) {
      max-height: 14000px
    }
```

- [ ] **Step 2: 기능 목록 + 모달 CSS 삽입**

바로 이어서:

```css
    /* ─── 기능 목록 (누르면 모달) ─── */
    .featlist {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 8px;
      margin-top: 4px
    }

    .feat {
      display: flex;
      align-items: center;
      gap: 8px;
      text-align: left;
      font: inherit;
      font-size: 12.5px;
      color: var(--text);
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px 12px;
      cursor: pointer;
      transition: border-color .2s, background .2s, transform .2s
    }

    .feat:hover {
      border-color: var(--accent);
      background: var(--accent-soft);
      transform: translateY(-1px)
    }

    .feat:focus-visible {
      outline: 2px solid var(--accent);
      outline-offset: 2px
    }

    .feat::after {
      content: "⤢";
      margin-left: auto;
      font-family: var(--mono);
      font-size: 11px;
      color: var(--faint)
    }

    .feat:hover::after {
      color: var(--accent)
    }

    /* ─── 기능 모달 ─── */
    .fmodal {
      position: fixed;
      inset: 0;
      z-index: 200;
      display: grid;
      place-items: center;
      padding: 20px;
      background: rgba(10, 12, 20, .55);
      backdrop-filter: blur(3px)
    }

    .fmodal[hidden] {
      display: none
    }

    .fmodal-card {
      position: relative;
      width: min(820px, 100%);
      max-height: min(88vh, 900px);
      overflow-y: auto;
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow-lg);
      padding: 22px 24px 24px
    }

    .fmodal-x {
      position: absolute;
      top: 12px;
      right: 12px;
      width: 32px;
      height: 32px;
      border-radius: 8px;
      border: 1px solid var(--line);
      background: var(--panel);
      color: var(--muted);
      font-size: 14px;
      cursor: pointer;
      transition: color .2s, border-color .2s
    }

    .fmodal-x:hover {
      color: var(--accent);
      border-color: var(--accent)
    }

    .fmodal-kicker {
      font-family: var(--mono);
      font-size: 11px;
      color: var(--accent);
      letter-spacing: .06em;
      margin-bottom: 4px
    }

    .fmodal-title {
      font-size: 18px;
      font-weight: 700;
      color: var(--ink);
      margin: 0 0 14px;
      padding-right: 40px
    }

    /* 다이어그램 — 인라인 SVG. 색은 전부 CSS 변수를 쓴다(다크 대응). */
    .fdiag {
      background: var(--panel);
      border: 1px solid var(--line-2);
      border-radius: 10px;
      padding: 14px;
      margin-bottom: 14px;
      overflow-x: auto
    }

    .fdiag svg {
      display: block;
      width: 100%;
      height: auto;
      min-width: 420px
    }

    .fsteps {
      counter-reset: fstep;
      margin: 0 0 14px;
      padding: 0;
      list-style: none
    }

    .fsteps li {
      counter-increment: fstep;
      position: relative;
      padding-left: 26px;
      margin-bottom: 7px;
      font-size: 13px;
      line-height: 1.65;
      color: var(--text)
    }

    .fsteps li::before {
      content: counter(fstep);
      position: absolute;
      left: 0;
      top: 1px;
      width: 18px;
      height: 18px;
      border-radius: 5px;
      background: var(--accent-soft);
      color: var(--accent);
      font-family: var(--mono);
      font-size: 10px;
      font-weight: 700;
      display: grid;
      place-items: center
    }

    .fmodal-fig {
      margin: 14px 0 0
    }

    .fmodal-fig img {
      display: block;
      width: 100%;
      height: auto;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: var(--panel)
    }

    .fmodal-fig figcaption {
      font-family: var(--mono);
      font-size: 11px;
      color: var(--faint);
      margin-top: 6px
    }

    @media (max-width:640px) {
      .featlist {
        grid-template-columns: 1fr
      }

      .fmodal {
        padding: 12px
      }

      .fmodal-card {
        padding: 18px 16px 20px
      }
    }
```

- [ ] **Step 3: 인쇄 CSS 갱신**

`index.html` 인쇄 블록의 두 곳을 고친다.

숨김 목록 (현재 `header, .hero-bg, .pc-caret, .tl-caret, .pc-actions, .hero-links, #pdfBtn`) 에 `.sub-caret` 과 `.fmodal` 을 추가:

```css
      header,
      .hero-bg,
      .pc-caret,
      .sub-caret,
      .tl-caret,
      .pc-actions,
      .hero-links,
      .fmodal,
      #pdfBtn {
        display: none !important
      }
```

아코디언 펼침 규칙에 `.sub-body` 를 추가:

```css
      /* 접힌 아코디언 전부 펼치기 */
      .pc-body,
      .pcard.open .pc-body,
      .sub-body,
      .subcard.open .sub-body {
        max-height: none !important;
        overflow: visible !important
      }
```

기능 목록은 인쇄본에 **남긴다**(모달은 안 나오지만 "어떤 기능이 있는지"는 정보다).
다만 `⤢` 표식은 인쇄에서 의미가 없으므로 지운다 — 위 숨김 블록 뒤에 추가:

```css
      .feat::after {
        content: "" !important
      }
```

- [ ] **Step 4: 검사 + 육안 확인**

```bash
python tools/check_page.py && start index.html
```

기대: `통과`. 브라우저에서 **아직 시각적 변화는 없다**(마크업이 없으므로). 기존 카드가
깨지지 않았는지만 본다 — 프로젝트 카드 8개가 평소대로 열리고 닫히면 통과.

- [ ] **Step 5: 커밋**

```bash
git add index.html
git commit -m "$(cat <<'EOF'
하위 카드·기능 모달 CSS 추가 (마크업은 다음 커밋)

.subcard 는 기존 .pcard 토글 패턴을 그대로 쓰고 톤만 낮췄다.
:has(.subcard) 인 카드만 max-height 상한을 올린다 — 기본 1400px 이면
중첩이 잘린다. 인쇄에선 하위 카드를 펼치고 모달과 ⤢ 표식을 숨긴다.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0178E3o2o2BuCsyArzc1XSsr
EOF
)"
```

---

## Task 4: 하위 드롭다운 · 모달 JS

**Files:**
- Modify: `index.html` — `/* 6. 프로젝트 아코디언 */` 블록 (현재 `index.html:3145-3146`) 바로 뒤

**Interfaces:**
- Consumes: Task 3 의 클래스. Task 5~8 이 만들 `.feat[data-modal]` 과 `#fmodal` / `.fmodal-body > section[id^="f-"]`.
- Produces: 전역 부작용만. 새 함수를 외부에 노출하지 않는다.

- [ ] **Step 1: JS 삽입**

`/* 6. 프로젝트 아코디언 */` 의 두 줄 바로 뒤에 삽입:

```js
    /* 6-a. 하위 프로젝트 카드 (QMesh 안의 FinAllQ·InsuQ·MaintQ)
       stopPropagation 이 핵심 — 없으면 하위를 열 때 부모 QMesh 카드가 닫힌다. */
    document.querySelectorAll('.subcard').forEach(sc => {
      const top = sc.querySelector('.sub-top');
      if (!top) return;
      top.addEventListener('click', e => {
        if (e.target.closest('a,button')) return;
        e.stopPropagation();
        sc.classList.toggle('open');
      });
    });

    /* 6-b. 기능 모달
       본문은 처음부터 DOM 에 있고 hidden 만 토글한다 — 복제하면 applyLang() 이
       닿지 않아 모달 안에서 KO/EN 전환이 죽는다. */
    (() => {
      const modal = document.getElementById('fmodal');
      if (!modal) return;
      const panes = [...modal.querySelectorAll('.fmodal-body > section')];
      let lastFocus = null;

      const open = id => {
        const pane = panes.find(p => p.id === id);
        if (!pane) return;
        lastFocus = document.activeElement;
        panes.forEach(p => { p.hidden = p !== pane; });
        /* GIF 는 열 때만 로드한다 — 초기 페이지 로딩에 영향을 주지 않는다. */
        pane.querySelectorAll('img[data-src]').forEach(img => {
          if (!img.getAttribute('src')) img.setAttribute('src', img.dataset.src);
        });
        modal.hidden = false;
        document.body.style.overflow = 'hidden';
        (modal.querySelector('.fmodal-x') || modal).focus();
      };

      const close = () => {
        modal.hidden = true;
        document.body.style.overflow = '';
        if (lastFocus) { lastFocus.focus(); lastFocus = null; }
      };

      document.querySelectorAll('.feat[data-modal]').forEach(btn => {
        btn.addEventListener('click', e => { e.stopPropagation(); open(btn.dataset.modal); });
      });

      modal.addEventListener('click', e => { if (e.target === modal) close(); });
      modal.querySelector('.fmodal-x')?.addEventListener('click', close);
      document.addEventListener('keydown', e => {
        if (modal.hidden) return;
        if (e.key === 'Escape') { close(); return; }
        if (e.key !== 'Tab') return;
        /* 포커스 트랩 */
        const f = [...modal.querySelectorAll('button,[href],img[tabindex],[tabindex]:not([tabindex="-1"])')]
          .filter(el => el.offsetParent !== null);
        if (!f.length) return;
        const first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      });
    })();
```

- [ ] **Step 2: 임시 마크업으로 동작 확인**

아직 실제 모달이 없으므로 임시로 하나 붙여 확인한다.
`<div class="projects">` 바로 뒤에 임시 삽입:

```html
        <button class="feat" data-modal="f-tmp" data-ko="임시 확인" data-en="temp check">임시 확인</button>
```

`</main>` 또는 `<footer` 직전에 임시 삽입:

```html
  <div class="fmodal" id="fmodal" hidden>
    <div class="fmodal-card" role="dialog" aria-modal="true" aria-labelledby="fmodal-t">
      <button class="fmodal-x" aria-label="닫기">&#10005;</button>
      <div class="fmodal-body">
        <section id="f-tmp">
          <div class="fmodal-kicker mono">TMP</div>
          <h4 class="fmodal-title" id="fmodal-t" data-ko="임시" data-en="Temp">임시</h4>
          <p data-ko="열렸다" data-en="opened">열렸다</p>
          <figure class="fmodal-fig">
            <img data-src="assets/maintq/unknown-error-code.gif" alt="">
          </figure>
        </section>
      </div>
    </div>
  </div>
```

- [ ] **Step 3: 브라우저 확인 6항목**

```bash
start index.html
```

개발자 도구 Network 탭을 열어둔 채 확인한다:

1. 초기 로드 시 Network 에 **`.gif` 요청이 0건**
2. "임시 확인" 버튼을 누르면 모달이 뜨고 **그때** GIF 요청이 뜬다
3. ESC 로 닫힌다
4. 배경(어두운 영역)을 누르면 닫힌다
5. ✕ 로 닫힌다
6. **모달을 연 상태에서 우측 상단 KO/EN 버튼을 누르면 "열렸다" → "opened" 로 바뀐다**
   ← 이게 복제 방식이면 깨지는 지점이다. 반드시 확인한다.

- [ ] **Step 4: 임시 마크업 제거**

Step 2 에서 넣은 `<button class="feat" data-modal="f-tmp" …>` 와 `#fmodal` 블록 전체를 지운다.
(`#fmodal` 은 Task 5 에서 실제 내용으로 다시 만든다.)

```bash
grep -n "f-tmp" index.html
```

기대: 출력 없음.

- [ ] **Step 5: 커밋**

```bash
python tools/check_page.py && git add index.html && git commit -m "$(cat <<'EOF'
하위 카드 토글 + 기능 모달 JS 추가

하위 카드 클릭에 stopPropagation 을 건다 — 없으면 하위를 열 때 부모
QMesh 카드가 닫힌다. 모달은 복제하지 않고 hidden 만 토글한다: 복제하면
applyLang() 이 닿지 않아 모달 안에서 언어 전환이 죽는다.
GIF 는 모달을 열 때만 src 를 주입해 초기 로딩에 영향을 주지 않는다.

임시 마크업으로 6항목(지연 로딩·ESC·배경·✕·모달 내 언어 전환) 확인 후 제거.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0178E3o2o2BuCsyArzc1XSsr
EOF
)"
```

---

## Task 5: QMesh 카드 본문 재작성 + 모달 2종

**Files:**
- Modify: `index.html:2311-2439` (PROJECT 01 카드 전체)
- Create: `index.html` 의 `#fmodal` 컨테이너 (`<footer` 직전)

**Interfaces:**
- Consumes: Task 3 CSS, Task 4 JS, Task 1 자산 `assets/qmesh/*.gif`
- Produces:
  - `#fmodal` 컨테이너 — Task 6·7·8 이 `.fmodal-body` 안에 `<section>` 을 추가한다
  - `<div class="subcards">` 컨테이너 — Task 6·7·8 이 `.subcard` 를 추가한다

콘텐츠 사실은 **SPEC §3-A 표**를 그대로 옮긴다.

- [ ] **Step 1: `#fmodal` 컨테이너 생성**

`<footer` 바로 앞에 삽입. `.fmodal-body` 는 지금은 비어 있고 이 태스크에서 2개를 채운다.

```html
  <!-- 기능 모달 — 본문을 복제하지 않고 hidden 만 토글한다(applyLang 이 닿아야 한다) -->
  <div class="fmodal" id="fmodal" hidden>
    <div class="fmodal-card" role="dialog" aria-modal="true">
      <button class="fmodal-x" aria-label="Close">&#10005;</button>
      <div class="fmodal-body">
      </div>
    </div>
  </div>
```

- [ ] **Step 2: QMesh 카드 본문 교체**

`index.html:2311-2439` 의 PROJECT 01 `<article>` 을 교체한다. 유지할 것 / 바꿀 것:

| 유지 | 바꿈 |
|---|---|
| `pc-top` 전체 (배지·제목·배지·해시태그) | `pc-meta` 기간을 `2026.08~` 로 (SPEC §3-A) |
| `pc-figure` 슬라이드 3종 | — |
| `pc-actions` 전체 | — |
| | "해결한 문제" — SPEC §3-A 1행 |
| | "계약 설계 결정" ul 4개 — SPEC §3-A ①②③④ |
| | **"연결 대상" ul 삭제 → `<div class="subcards">` 로 교체** |
| | "구현" 블록 신설 — SPEC §3-A 구현행 |
| | "관통 원칙(HITL)" 블록 신설 — SPEC §3-A HITL행 |
| | `impact` 문단 — SPEC §3-A 성과+아직 안 된 것 |
| | `metricrow` — 13종 / 3종 / **5경로** / 123건 |
| | 기능 모달 2종 `featlist` |

`metricrow` 는 기존 2개에서 4개로 늘린다:

```html
                  <div class="metricrow">
                    <div class="metric">
                      <div class="mv"><span data-count="13">0</span>종</div>
                      <div class="ml" data-ko="표준 Task 스키마" data-en="Task schemas">표준 Task 스키마</div>
                    </div>
                    <div class="metric">
                      <div class="mv"><span data-count="3">0</span>종</div>
                      <div class="ml" data-ko="Agent Card" data-en="Agent Cards">Agent Card</div>
                    </div>
                    <div class="metric">
                      <div class="mv"><span data-count="5">0</span>경로</div>
                      <div class="ml" data-ko="종단 검증" data-en="verified end to end">종단 검증</div>
                    </div>
                    <div class="metric">
                      <div class="mv"><span data-count="123">0</span>건</div>
                      <div class="ml" data-ko="어댑터 테스트" data-en="adapter tests">어댑터 테스트</div>
                    </div>
                  </div>
```

기능 목록 (`impact` 블록 앞):

```html
                  <div class="block">
                    <div class="bh"><span class="star">&#9670;</span> <span data-ko="실동작 — 눌러서 보기" data-en="See it run">실동작 — 눌러서 보기</span></div>
                    <div class="featlist">
                      <button class="feat" data-modal="f-qmesh-settlement" data-ko="상대 응답이 내 상태를 바꾼다 (S12)" data-en="Their reply changes my state (S12)">상대 응답이 내 상태를 바꾼다 (S12)</button>
                      <button class="feat" data-modal="f-qmesh-inbox" data-ko="상대 회사 결재함에 도착 (S5)" data-en="Arriving in their approval inbox (S5)">상대 회사 결재함에 도착 (S5)</button>
                    </div>
                  </div>
```

- [ ] **Step 3: 하위 카드 컨테이너 삽입**

"연결 대상 — 직접 만든 Q 시리즈" `<ul>` 이 있던 자리에:

```html
                  <div class="block">
                    <div class="bh"><span class="star">&#9670;</span> <span data-ko="연결 대상 — 직접 만든 Q 시리즈 3종" data-en="What it connects — the three Q-series agents">연결 대상 — 직접 만든 Q 시리즈 3종</span></div>
                    <p data-ko="세 프로젝트 모두 <b>언어·프레임워크·저장소가 서로 다르다</b> — 그래서 연결에 표준 계약이 필요했다. 각 카드를 펼치면 그 프로젝트의 기능과 설계가 나온다."
                      data-en="All three run on <b>different languages, frameworks and repositories</b> — which is exactly why the link needed a standard contract. Expand a card for that project's features and design.">세 프로젝트 모두 <b>언어·프레임워크·저장소가 서로 다르다</b> — 그래서 연결에 표준 계약이 필요했다. 각 카드를 펼치면 그 프로젝트의 기능과 설계가 나온다.</p>
                    <div class="subcards">
                      <!-- Task 6: FinAllQ · Task 7: InsuQ · Task 8: MaintQ -->
                    </div>
                  </div>
```

- [ ] **Step 4: 모달 2종 작성**

`.fmodal-body` 안에 추가. 두 모달 모두 이 구조를 따른다 —
**`data-ko` 는 텍스트 말단에만** 붙인다(`<figure>`·`<div class="fdiag">` 에는 절대 붙이지 않는다).

```html
        <section id="f-qmesh-settlement" hidden>
          <div class="fmodal-kicker mono">QMESH · S12 request-settlement</div>
          <h4 class="fmodal-title" data-ko="상대 응답이 내 상태를 바꾼다" data-en="Their reply changes my state">상대 응답이 내 상태를 바꾼다</h4>
          <div class="fdiag">
            <svg viewBox="0 0 620 150" role="img" aria-label="MaintQ 처분 사전판정 BLOCKED → A2A 정산 → CONDITIONAL">
              <style>
                .n{fill:var(--paper);stroke:var(--line);stroke-width:1.5;rx:8}
                .t{font:600 12px var(--sans);fill:var(--ink)}
                .s{font:11px var(--mono);fill:var(--muted)}
                .a{stroke:var(--accent);stroke-width:1.5;fill:none;marker-end:url(#ah)}
                .bad{fill:#c0392b;font:600 11px var(--mono)}
                .ok{fill:var(--ok);font:600 11px var(--mono)}
              </style>
              <defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10z" fill="var(--accent)"/></marker></defs>
              <rect class="n" x="4" y="20" width="150" height="46"/><text class="t" x="16" y="40">처분 사전판정</text><text class="bad" x="16" y="57">BLOCKED (409)</text>
              <path class="a" d="M158 43 H232"/>
              <rect class="n" x="236" y="20" width="164" height="46"/><text class="t" x="248" y="40">A2A 정산 요청</text><text class="s" x="248" y="57">→ FinAllQ</text>
              <path class="a" d="M404 43 H462"/>
              <rect class="n" x="466" y="20" width="150" height="46"/><text class="t" x="478" y="40">재판정</text><text class="ok" x="478" y="57">CONDITIONAL (200)</text>
              <path class="a" d="M318 70 V104 H160" /><text class="s" x="170" y="118">lien_released: true → assets.lien_consent_ref</text>
              <text class="s" x="170" y="136" fill="var(--gold-ink)">단, 결정 문서는 여전히 draft — 서명은 사람이</text>
            </svg>
          </div>
          <p data-ko="발신 스킬 6종 중 <b>유일하게 상대 응답이 MaintQ 자신의 상태를 바꾸는</b> 경로다. 나머지는 되받거나(조회) 알리기만(통지) 한다."
            data-en="The only one of the six outbound skills where the reply changes MaintQ's own state. The others only fetch or notify.">발신 스킬 6종 중 <b>유일하게 상대 응답이 MaintQ 자신의 상태를 바꾸는</b> 경로다. 나머지는 되받거나(조회) 알리기만(통지) 한다.</p>
          <ol class="fsteps">
            <li data-ko="자산 처분을 시도하면 유치권 때문에 사전판정이 <b>BLOCKED</b>(409)로 막힌다." data-en="Disposal is pre-checked and comes back <b>BLOCKED</b> (409) because of the lien.">자산 처분을 시도하면 유치권 때문에 사전판정이 <b>BLOCKED</b>(409)로 막힌다.</li>
            <li data-ko="매각대금 정산·대출상환을 FinAllQ에 A2A로 요청한다." data-en="MaintQ asks FinAllQ over A2A to settle the proceeds and repay the loan.">매각대금 정산·대출상환을 FinAllQ에 A2A로 요청한다.</li>
            <li data-ko="응답의 <span class=&quot;mono&quot;>lien_released: true</span>가 <span class=&quot;mono&quot;>assets.lien_consent_ref</span>를 채워 차단을 해소한다." data-en="<span class=&quot;mono&quot;>lien_released: true</span> in the reply fills <span class=&quot;mono&quot;>assets.lien_consent_ref</span> and clears the block.">응답의 <span class="mono">lien_released: true</span>가 <span class="mono">assets.lien_consent_ref</span>를 채워 차단을 해소한다.</li>
            <li data-ko="재판정이 <b>CONDITIONAL</b>(200)로 풀린다. <b>다만 결정 문서는 여전히 draft</b> — 담보만 풀고 서명은 하지 않는다." data-en="The re-check clears to <b>CONDITIONAL</b> (200). <b>The decision document stays a draft</b> — the lien is released, the signature is not.">재판정이 <b>CONDITIONAL</b>(200)로 풀린다. <b>다만 결정 문서는 여전히 draft</b> — 담보만 풀고 서명은 하지 않는다.</li>
          </ol>
          <figure class="fmodal-fig">
            <img data-src="assets/qmesh/request-settlement.gif" alt="request-settlement demo">
            <figcaption data-ko="실 DB · 실 인증으로 촬영한 종단 검증 경로" data-en="Captured end to end against live data and real auth">실 DB · 실 인증으로 촬영한 종단 검증 경로</figcaption>
          </figure>
        </section>
```

두 번째 모달 `f-qmesh-inbox` 는 같은 구조로 작성한다. 내용:
- kicker `QMESH · S5 request-withdrawal`
- 제목: KO `상대 회사 결재함에 요청이 도착한다` / EN `The request lands in their approval inbox`
- 다이어그램: `MaintQ 팀장 승인 → MaintQ 재무 승인(SoD) → [A2A] → FinAllQ 재무결재` 4단 가로 흐름.
  마지막 칸 아래에 `3단 승인 = MaintQ 내부 2단 + FinAllQ 1단` 캡션
- 본문: SPEC §3-A HITL 행 — 요청자가 `a2a-service@finallq.example` 로 뜨고 메모에 MaintQ 진단 근거가 그대로 실린다
- `assets/qmesh/approval-inbox-arrival.gif`

- [ ] **Step 5: 검증 + 커밋**

```bash
python tools/check_page.py && start index.html
```

확인: QMesh 카드가 열리고, 기능 2개가 모달로 뜨고, `.subcards` 자리가 (아직 비어) 있다.
카운터 4개가 13 / 3 / 5 / 123 으로 올라간다.

```bash
git add index.html && git commit -m "$(cat <<'EOF'
QMesh 카드를 A2A 이야기에 집중하도록 재작성 + 모달 2종

계약 설계 결정 4가지(actor/subject 분리 · 인증 위임/인가 보유 ·
rejected 를 계약에 · 인용 정규식 고정)를 본문으로 올리고, 불릿 3줄이던
"연결 대상"을 하위 카드 자리로 바꿨다.

성과 표기를 정정했다 — 종단 검증 3경로 -> 5경로(실측). 오케스트레이터
:9000 미구현과 MaintQ 수신이 "설계상 없음"(미착수 아님)인 것을 명시.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0178E3o2o2BuCsyArzc1XSsr
EOF
)"
```

---

## Task 6: FinAllQ 하위 카드 + 기능 모달 7종

**Files:**
- Modify: `index.html` — Task 5 의 `<div class="subcards">` 안 (첫 번째), `.fmodal-body` 안

**Interfaces:**
- Consumes: `assets/finallq/*.jpg` (13장)
- Produces: `.subcard` 1개, `section#f-finallq-*` 7개

**순서가 핵심이다 — 기능 목록이 먼저, "왜 LLM이 없는가"가 그 아래.** (사용자 확정)

- [ ] **Step 1: 하위 카드 골격**

```html
                      <article class="subcard">
                        <div class="sub-top">
                          <div class="sub-headings">
                            <div class="sub-code mono" data-ko="은행·증권 통합 금융 비서" data-en="Banking &amp; brokerage assistant">은행·증권 통합 금융 비서</div>
                            <h4 class="sub-title">FinAllQ</h4>
                            <div class="sub-meta" data-ko="2025.10~ 진행 중 <span class=&quot;sep&quot;>·</span> 개인 1인 <span class=&quot;sep&quot;>·</span> Spring Boot 3 + FastAPI + React 19 하이브리드 MSA"
                              data-en="Since Oct 2025 <span class=&quot;sep&quot;>·</span> solo <span class=&quot;sep&quot;>·</span> Spring Boot 3 + FastAPI + React 19 hybrid MSA">2025.10~ 진행 중 <span class="sep">·</span> 개인 1인 <span class="sep">·</span> Spring Boot 3 + FastAPI + React 19 하이브리드 MSA</div>
                          </div>
                          <span class="sub-caret">&#9654;</span>
                        </div>
                        <div class="sub-body">
                          <div class="sub-inner">
                            <!-- ① 기능 목록 ② 왜 LLM이 없는가 ③ A2A ④ 계측 -->
                          </div>
                        </div>
                      </article>
```

- [ ] **Step 2: ① 기능 목록 (먼저 온다)**

```html
                            <div class="block">
                              <div class="bh"><span class="star">&#9670;</span> <span data-ko="주요 기능 — 누르면 화면과 흐름이 열립니다" data-en="Features — click for the screen and the flow">주요 기능 — 누르면 화면과 흐름이 열립니다</span></div>
                              <div class="featlist">
                                <button class="feat" data-modal="f-finallq-dashboard" data-ko="통합 대시보드" data-en="Unified dashboard">통합 대시보드</button>
                                <button class="feat" data-modal="f-finallq-assessment" data-ko="여신 심사 근거 카드" data-en="Loan assessment evidence">여신 심사 근거 카드</button>
                                <button class="feat" data-modal="f-finallq-disbursement" data-ko="여신 ↔ 이체 연결" data-en="Loan-to-transfer bridge">여신 ↔ 이체 연결</button>
                                <button class="feat" data-modal="f-finallq-approval" data-ko="기업 이체 결재 (직무 분리)" data-en="Corporate approval (SoD)">기업 이체 결재 (직무 분리)</button>
                                <button class="feat" data-modal="f-finallq-fds" data-ko="FDS 고위험 → 2FA 승격" data-en="FDS high risk → 2FA">FDS 고위험 → 2FA 승격</button>
                                <button class="feat" data-modal="f-finallq-smishing" data-ko="스미싱 탐지" data-en="Smishing detection">스미싱 탐지</button>
                                <button class="feat" data-modal="f-finallq-failsoft" data-ko="AI 비서 — 정직한 실패" data-en="Assistant — honest failure">AI 비서 — 정직한 실패</button>
                              </div>
                            </div>
```

- [ ] **Step 3: ② "AI 비서인데 왜 LLM이 없는가" 블록 (기능 아래)**

`<div class="block">` 안에 `<ul>` 로. 내용은 **SPEC §3-B 하단 불릿 6개**를 그대로 옮긴다.
제목: KO `AI 비서인데 왜 LLM이 없는가` / EN `An AI assistant with no LLM — on purpose`.

마지막 불릿은 반드시 **정직 표기**를 포함한다:
> FDS 필수 게이트는 **구현돼 있으나 현재 미발동** — `_TRANSFER_TOOL_NAMES`가 빈 집합이다.
> 오케스트레이터에 송금 툴이 아직 없어 규칙과 자리만 먼저 만들어 뒀고, 코드 주석과 백로그에 함께 적어 뒀다.

- [ ] **Step 4: ③ A2A + ④ 계측 `impact` 블록**

```html
                            <div class="impact block">
                              <div class="bh"><span class="star">&#9733;</span> <span data-ko="계측 (2026.09.08 전수)" data-en="Measured (full scan, 2026-09-08)">계측 (2026.09.08 전수)</span></div>
                              <p data-ko="LLM·외부 AI API 호출 <b>0건</b>(전수 grep) · MCP 툴 <b>20종</b> · 백엔드 테스트 <b>1,098건</b> 통과 · AI 엔드포인트 <b>12개</b>. A2A는 수신 <b>7스킬</b>이고, <span class=&quot;mono&quot;>assess-loan</span>이 InsuQ의 <span class=&quot;mono&quot;>verify-collateral-insurance</span>를 <b>2차 홉으로 실제 호출</b>한다."
                                data-en="Zero LLM or external AI calls (full grep) · 20 MCP tools · 1,098 backend tests passing · 12 AI endpoints. On A2A it answers 7 skills, and <span class=&quot;mono&quot;>assess-loan</span> really calls InsuQ's <span class=&quot;mono&quot;>verify-collateral-insurance</span> as a second hop.">LLM·외부 AI API 호출 <b>0건</b>(전수 grep) · MCP 툴 <b>20종</b> · 백엔드 테스트 <b>1,098건</b> 통과 · AI 엔드포인트 <b>12개</b>. A2A는 수신 <b>7스킬</b>이고, <span class="mono">assess-loan</span>이 InsuQ의 <span class="mono">verify-collateral-insurance</span>를 <b>2차 홉으로 실제 호출</b>한다.</p>
                            </div>
```

- [ ] **Step 5: 모달 7종 작성**

Task 5 Step 4 의 `<section>` 구조를 그대로 따른다. 각 모달의 확정 내용:

| id | kicker | 제목 KO / EN | 다이어그램 | 본문 근거 | 이미지 |
|---|---|---|---|---|---|
| `f-finallq-dashboard` | `FINALLQ · /` | 통합 대시보드 / Unified dashboard | `은행 계좌 + 증권 보유종목 → 합산 뷰 → FDS 경보·규제 알림(심각도순)` | SPEC §3-B 1행 — 규제 경고는 하드코딩 문구가 아니라 **포트폴리오 비율을 임계값과 비교한 실제 룰 판정** | `02_dashboard.jpg` |
| `f-finallq-assessment` | `FINALLQ · /loan/applications` | 여신 심사 근거 카드 / Loan assessment evidence | `심사 시점 판정 로직 ─┬─ 쓰기(심사) └─ 읽기(근거 카드)` — 한 로직을 둘이 공유 | SPEC §3-B 2행 — 한도·LTV·규칙 판정이 전부 실제 계산값. 신규 API를 만들지 않고 **심사와 같은 로직을 재사용** | `03_loan_list.jpg` · `04_loan_assessment.jpg` |
| `f-finallq-disbursement` | `FINALLQ · 여신 → 이체` | 여신 ↔ 이체 연결 / Loan-to-transfer bridge | `서버 집계(원금·집행액·잔여) → disbursable? → [출금 준비] → 이체 폼 사전채움 → 제출 시 서버가 잔여 한도 재검증` | SPEC §3-B 3행 — **판정은 서버가, 화면은 결과만**. 출금·수취 계좌는 사전채움하지 않는다(사람이 직접 확인) | `05_loan_disbursement.jpg` · `06_transfer_apply_form.jpg` |
| `f-finallq-approval` | `FINALLQ · ApprovalPolicy` | 기업 이체 결재 — 직무 분리 / Corporate approval — separation of duties | `신청자(취소만 가능) → 결재 대기 → MANAGER 결재함(요청자 1일 한도 사용액 표시)` | SPEC §3-B 4행 — 신청자에게 **승인 버튼이 없다**. 기업 고객은 요청자≠결재자가 강제된다 | `07_transfer_pending_approval.jpg` · `08_manager_approval_queue.jpg` |
| `f-finallq-fds` | `FINALLQ · 이중 방어` | FDS 고위험 → 2FA 승격 / FDS high risk → 2FA | `결재 승인(사람) ─통과─→ FDS 재평가(모델) ─고위험─→ TOTP 2FA 필요` — 두 축이 직렬 | SPEC §3-B 5행 — 결재가 끝나도 **자동 완료되지 않는다**. 규칙(한도)→모델(FDS) 이중 방어 | `09_transfer_2fa_required.jpg` |
| `f-finallq-smishing` | `FINALLQ · /security` | 스미싱 탐지 / Smishing detection | `문자 입력 → TF-IDF + LogisticRegression → 위험점수 + 위험 단어 근거 → 이력(JWT 주체로 서버 확정)` | SPEC §3-B 6행 — 요청 본문의 자유 문자열로 **타인 이력을 조회할 수 없다**(IDOR 방지) | `10_smishing_empty.jpg` · `11_smishing_result.jpg` |
| `f-finallq-failsoft` | `FINALLQ · /chat` | AI 비서 — 정직한 실패 / The assistant fails honestly | `질의 → 툴 매칭 ─없음─→ "범위 밖" + 근거 공개` / `─있음·실패─→ Fail-soft 배너` | SPEC §3-B 7행 — 지어내지 않는다. **빠진 기능을 조용히 숨기지 않는다** | `12_ai_chat_out_of_scope.jpg` · `13_ai_chat_fail_soft.jpg` |

이미지가 2장인 모달은 `<figure class="fmodal-fig">` 를 2개 연달아 둔다.

- [ ] **Step 6: 검증 + 커밋**

```bash
python tools/check_page.py && start index.html
```

확인: QMesh 를 연 뒤 FinAllQ 하위 카드를 열어도 **QMesh 가 닫히지 않는다.** 본문이 잘리지 않는다.
기능 7개가 전부 모달로 뜨고, 각 모달의 스크린샷이 보인다.

```bash
git add index.html && git commit -m "$(cat <<'EOF'
FinAllQ 하위 카드 + 기능 모달 7종

기능 목록을 먼저 놓고 그 아래에 "AI 비서인데 왜 LLM이 없는가"를 뒀다.
결정 공간이 닫혀 있었고 금융은 감사 가능성을 요구했다는 판단, 그리고
대신 공을 들인 가드레일 4종.

FDS 필수 게이트는 "구현됨·현재 미발동"으로 정직하게 적었다
(_TRANSFER_TOOL_NAMES 가 빈 집합 — 송금 툴이 아직 없다).

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0178E3o2o2BuCsyArzc1XSsr
EOF
)"
```

---

## Task 7: InsuQ 하위 카드 + LangGraph 흐름도 + 모달 4종

**Files:**
- Modify: `index.html` — `<div class="subcards">` 안 (두 번째), `.fmodal-body` 안

**Interfaces:**
- Consumes: `assets/insuq/*.gif` (4종)
- Produces: `.subcard` 1개, `section#f-insuq-*` 4개

- [ ] **Step 1: 하위 카드 골격 + 한 줄 정의**

`sub-code`: KO `보험 약관 분석·보장 판정 RAG 에이전트` / EN `Policy-clause RAG agent`
`sub-meta`: KO `2026.07~ 진행 중 · 개인 1인 · Spring Boot 4 + FastAPI/LangGraph + Qdrant + Next.js`

본문 첫 블록은 **한 줄 정의**:
> **"AI가 판정하지 않는다. 근거를 모아 원문 그대로 주고, 판단은 사람이 한다."**

바로 이어 SPEC §3-C "설계사 관점의 검색" 2줄 — `product_filter` 로 먼저 좁히고,
조문이 다른 조문을 참조하면 그 `refs` 를 따라 재검색(같은 파트 안에서만, 깊이 제한).

- [ ] **Step 2: LangGraph 흐름도 — 카드 본문에 인라인 SVG (모달 아님)**

**주의 (SPEC §3-C 경고):** 컴파일된 `StateGraph` 의 노드는 `route` 와 `clarify` **둘뿐**이다.
멀티홉·판정은 그래프 노드가 아니라 그 뒤 파이프라인(`answer_question_stream`)에 있다.
**점선 박스로 그래프 경계를 그려 둘을 구분**한다. "LangGraph 노드 4개"라고 쓰면 거짓이다.

```html
                            <div class="block">
                              <div class="bh"><span class="star">&#9670;</span> <span data-ko="LangGraph 파이프라인" data-en="The LangGraph pipeline">LangGraph 파이프라인</span></div>
                              <div class="fdiag">
                                <svg viewBox="0 0 640 320" role="img" aria-label="InsuQ 라우팅·되묻기·검색·생성 파이프라인">
                                  <style>
                                    .n{fill:var(--paper);stroke:var(--line);stroke-width:1.5}
                                    .g{fill:none;stroke:var(--accent);stroke-width:1.2;stroke-dasharray:5 4}
                                    .t{font:600 12px var(--sans);fill:var(--ink)}
                                    .s{font:10.5px var(--mono);fill:var(--muted)}
                                    .k{font:600 10px var(--mono);fill:var(--accent)}
                                    .a{stroke:var(--accent);stroke-width:1.4;fill:none;marker-end:url(#ih)}
                                  </style>
                                  <defs><marker id="ih" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10z" fill="var(--accent)"/></marker></defs>
                                  <!-- StateGraph 경계 -->
                                  <rect class="g" x="8" y="34" width="300" height="118" rx="10"/>
                                  <text class="k" x="18" y="28">StateGraph — 노드는 이 둘뿐</text>
                                  <rect class="n" x="26" y="48" width="130" height="42" rx="8"/><text class="t" x="38" y="66">route</text><text class="s" x="38" y="81">키워드 → LLM 1회</text>
                                  <rect class="n" x="26" y="102" width="130" height="42" rx="8"/><text class="t" x="38" y="120">clarify</text><text class="s" x="38" y="135">슬롯 검사</text>
                                  <path class="a" d="M91 92 V100"/>
                                  <!-- 되묻기 -->
                                  <rect class="n" x="330" y="48" width="180" height="42" rx="8"/><text class="t" x="342" y="66">되묻기 질문</text><text class="s" x="342" y="81">LLM 0회 — 순수 조회</text>
                                  <path class="a" d="M160 123 H330 V92"/><text class="k" x="196" y="118">CLARIFY</text>
                                  <!-- 본 파이프라인 -->
                                  <rect class="n" x="26" y="186" width="118" height="40" rx="8"/><text class="t" x="38" y="211">검색</text>
                                  <rect class="n" x="164" y="186" width="150" height="40" rx="8"/><text class="t" x="176" y="205">멀티홉</text><text class="s" x="176" y="219">refs 따라 재검색</text>
                                  <rect class="n" x="334" y="186" width="118" height="40" rx="8"/><text class="t" x="346" y="211">생성</text>
                                  <path class="a" d="M91 146 V184"/><text class="k" x="100" y="170">그 외</text>
                                  <path class="a" d="M148 206 H162"/><path class="a" d="M318 206 H332"/>
                                  <rect class="n" x="26" y="252" width="200" height="52" rx="8"/><text class="t" x="38" y="271">방어선 ① 근거 한정</text><text class="s" x="38" y="288">인용 필수 · 없으면 거부</text>
                                  <rect class="n" x="244" y="252" width="200" height="52" rx="8"/><text class="t" x="256" y="271">방어선 ② 단정 감지</text><text class="s" x="256" y="288">유보(HOLD)로 강등</text>
                                  <rect class="n" x="462" y="252" width="170" height="52" rx="8"/><text class="t" x="474" y="271">판정 3단계</text><text class="s" x="474" y="288">+ 확인 필요 사항</text>
                                  <path class="a" d="M393 228 V250"/>
                                </svg>
                              </div>
                              <p data-ko="컴파일된 그래프의 노드는 <span class=&quot;mono&quot;>route</span>·<span class=&quot;mono&quot;>clarify</span> <b>둘뿐</b>이고, 멀티홉·판정은 그 뒤 파이프라인에 있다 — 점선이 그 경계다. 되묻기로 빠지면 <b>LLM을 한 번도 부르지 않는다</b>(슬롯에서 문구를 만드는 건 순수 조회다)."
                                data-en="The compiled graph has exactly two nodes — <span class=&quot;mono&quot;>route</span> and <span class=&quot;mono&quot;>clarify</span>; multi-hop and verdict live in the pipeline behind it, and the dashed box marks that boundary. On the clarify branch it never calls the LLM at all — turning slots into questions is a pure lookup.">컴파일된 그래프의 노드는 <span class="mono">route</span>·<span class="mono">clarify</span> <b>둘뿐</b>이고, 멀티홉·판정은 그 뒤 파이프라인에 있다 — 점선이 그 경계다. 되묻기로 빠지면 <b>LLM을 한 번도 부르지 않는다</b>(슬롯에서 문구를 만드는 건 순수 조회다).</p>
                            </div>
```

- [ ] **Step 3: 설계 포인트 · 신경 쓴 점 블록**

SPEC §3-C 의 "설계 포인트" 5개와 "신경 쓴 점" 4개를 각각 `<ul>` 두 블록으로 옮긴다.

- [ ] **Step 4: 기능 모달 4종**

| id | kicker | 제목 KO / EN | 다이어그램 | 근거 | GIF |
|---|---|---|---|---|---|
| `f-insuq-citation` | `INSUQ · 근거 인용` | 조항 원문과 함께 답한다 / Answering with the clause itself | `질문 → 검색 → 인용 대조 키 (policy_part, article_no) → 답변 + 조항 원문` | 파트를 빼면 다른 파트의 같은 조 번호를 지어내도 탐지를 통과한다 — 한 상품 안에 `제1조`가 3곳 존재(실측) | `grounded-citation.gif` |
| `f-insuq-refusal` | `INSUQ · 거부 게이트` | 모르면 거부한다 / It refuses when it cannot cite | `근거 검색 → 없음 → "약관에서 확인 불가"` (거부 1.0000 / **과잉거부 0.0000**) | 거부 정확도는 반드시 과잉거부와 쌍으로 본다 — 한쪽만 보면 아무것도 안 답하는 게 최적이 된다 | `refusal-gate.gif` |
| `f-insuq-clarify` | `INSUQ · 되묻기` | 정보가 빠지면 되묻는다 / It asks back when slots are missing | `질문 → 슬롯(상품·특약·가입시기) 검사 → 미충족 → 확인 질문 (LLM 0회)` | 실제 질문은 상품·특약·가입시기가 생략된 채 들어온다. 되묻기 정확도 **1.0000**(27문항) | `ambiguous-domain-merge.gif` |
| `f-insuq-claim` | `INSUQ · claim-insurance` | 사람 앞에서 멈췄다 재개된다 / It stops for a human, then resumes | `산정(결정론적 산술) → status=input-required → 심사역 로그인 → 전자서명 승인 → completed → 재폴링 수령` | 계약 13종 중 **유일하게 `input-required`를 쓰는 스킬**. `requires_human_approval: true`는 계산 경로 없이 **리터럴로만 존재해 우회할 수 없다** | `claim-approval.gif` |

- [ ] **Step 5: `impact` 블록 — 실측**

**⚠️ 트랙1과 트랙4를 나란히 놓지 않는다.** 두 문장으로 분리하고 각각 분모를 함께 적는다.
judge 공란을 반드시 포함한다. SPEC §3-C "실측" 4줄 그대로.

`metricrow` 는 트랙1 기준 3개만 — `0.81`(Hit@5, 실손 27문항) · `0.00`(과잉거부) · `67`(실험 건수).
소수 값은 `data-count` 가 정수만 다루므로 **정적 텍스트로 적는다**(Global Constraint 4 와 별개로,
카운터는 정수 전용이다).

- [ ] **Step 6: 검증 + 커밋**

```bash
python tools/check_page.py && start index.html
```

라이트/다크 양쪽에서 **SVG 흐름도가 읽히는지** 확인한다(테마 버튼으로 전환).

```bash
git add index.html && git commit -m "$(cat <<'EOF'
InsuQ 하위 카드 + LangGraph 흐름도 + 기능 모달 4종

RAG 에 집중했다 — AI 가 판정하지 않고 근거를 모아 원문 그대로 주며,
판단은 사람이 한다. 가입 상품으로 먼저 좁히고 조문의 refs 를 따라 재검색.

흐름도는 그래프 경계를 점선으로 그렸다. 컴파일된 StateGraph 의 노드는
route·clarify 둘뿐이고 멀티홉·판정은 그 뒤 파이프라인에 있다 —
"LangGraph 노드 4개"로 쓰면 사실이 아니다.

트랙1(27문항)과 트랙4(52문항)를 나란히 놓지 않았고, 답변 정확도는
채점 모델 소실로 공란임을 명시했다.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0178E3o2o2BuCsyArzc1XSsr
EOF
)"
```

---

## Task 8: MaintQ 하위 카드 + 기능 모달 7종

**Files:**
- Modify: `index.html` — `<div class="subcards">` 안 (세 번째), `.fmodal-body` 안

**Interfaces:**
- Consumes: `assets/maintq/*.gif` (7종)
- Produces: `.subcard` 1개, `section#f-maintq-*` 7개

**순서: 기능 목록 먼저, 그 아래 MCP.** (사용자 확정)

- [ ] **Step 1: 하위 카드 골격**

`sub-code`: KO `제조 설비 진단·부품 발주 에이전트` / EN `Plant maintenance & procurement agent`
`sub-meta`: KO `2026.07~ 진행 중 · 개인 1인 · Python FastAPI + MCP + PostgreSQL(pgvector) + Next.js`

- [ ] **Step 2: ① 기능 목록 (먼저)**

```html
                              <div class="featlist">
                                <button class="feat" data-modal="f-maintq-unknown" data-ko="미지 에러코드 — 추측하지 않는다" data-en="Unknown code — no guessing">미지 에러코드 — 추측하지 않는다</button>
                                <button class="feat" data-modal="f-maintq-alt" data-ko="호환 대체품 분기" data-en="Compatible alternatives">호환 대체품 분기</button>
                                <button class="feat" data-modal="f-maintq-repeat" data-ko="반복 고장 감지 → 발주 보류" data-en="Repeat failure → hold the order">반복 고장 감지 → 발주 보류</button>
                                <button class="feat" data-modal="f-maintq-disposal" data-ko="처분 사전판정" data-en="Disposal pre-check">처분 사전판정</button>
                                <button class="feat" data-modal="f-maintq-bundle" data-ko="처분 근거 번들" data-en="Evidence bundle">처분 근거 번들</button>
                                <button class="feat" data-modal="f-maintq-deadline" data-ko="법정 기한 · 위험등급" data-en="Deadlines &amp; risk grade">법정 기한 · 위험등급</button>
                                <button class="feat" data-modal="f-maintq-expenditure" data-ko="지출 성격 분류" data-en="Expenditure classification">지출 성격 분류</button>
                              </div>
```

- [ ] **Step 3: ② "집중한 것 — MCP 도구 설계" 블록 (기능 아래)**

SPEC §3-D 의 MCP 불릿 6개를 `<ul>` 로. 제목 KO `집중한 것 — MCP 도구 설계` / EN `The focus — MCP tool design`.

- [ ] **Step 4: ③ 신경 쓴 점 블록**

SPEC §3-D "신경 쓴 점" 3개.

- [ ] **Step 5: 모달 7종**

| id | kicker | 제목 KO | 다이어그램 | GIF |
|---|---|---|---|---|
| `f-maintq-unknown` | `MAINTQ · S4` | 미지 에러코드 — 추측하지 않는다 | `lookup_error_code → not_found → A/S 안내` (환각률 **0.0%**) | `unknown-error-code.gif` |
| `f-maintq-alt` | `MAINTQ · S2` | 재고 0 → 호환 대체품 | `search_inventory(qty=0) → find_alternative_parts → get_supplier_quotes → create_po_draft` | `alternative-parts.gif` |
| `f-maintq-repeat` | `MAINTQ · S3` | 반복 고장 감지 → 발주 보류 | `lookup → get_error_history(repeated=true, 30일 3회) → rag_search_manual(안전 근거) → 발주 HOLD` | `repeat-failure-hold.gif` |
| `f-maintq-disposal` | `MAINTQ · 자산 생애주기` | 처분 사전판정 | `처분일 미입력 → INSUFFICIENT_FACTS` / `입력 → CLEAR + 근거 조문 + "고려하지 않은 것" 고지` | `disposal-precheck.gif` |
| `f-maintq-bundle` | `MAINTQ · bundle_hash` | 처분 근거 번들 | `laws · rules · evaluated · contracts · facts 5종 → bundle_hash 로 고정 → 룰별 TRIGGERED/CLEAR/INSUFFICIENT_FACTS` | `disposal-evidence-bundle.gif` |
| `f-maintq-deadline` | `MAINTQ · 보전팀장 콘솔` | 법정 기한 · 건물 위험등급 | `track_deadlines(180~730일) → 임박 항목` / `assess_risk_grade → 산출식 + "자동 반영 안 됨" 고지` | `deadline-risk-grade.gif` |
| `f-maintq-expenditure` | `MAINTQ · 재무담당 콘솔` | 지출 성격 분류 | `경계 사례 → 자본적/수익적 단정 금지 → "판단 유보 — 전문가 검토 필요"` | `expenditure-classification.gif` |

모든 모달의 `figcaption` 에 공통으로 넣는다:
KO `시드 데이터 그대로, 실제 API 응답으로 촬영 (연출 없음)` / EN `Captured against seed data and real API responses — nothing staged`

- [ ] **Step 6: `impact` 블록 + A2A**

SPEC §3-D "실측" 줄 + A2A 2줄(발신 6종 전건 실 E2E / 수신은 **설계상 없음**).
`metricrow` 3개: `22`(MCP 도구) · `1559`(회귀 검사) · `141`(설계 결정 D1~D141).

- [ ] **Step 7: 검증 + 커밋**

```bash
python tools/check_page.py && start index.html
```

확인: 하위 카드 3개가 모두 있고, 하나를 열어도 나머지·부모가 닫히지 않는다.
MaintQ 모달 7개가 전부 뜨고 GIF 가 재생된다.

```bash
git add index.html && git commit -m "$(cat <<'EOF'
MaintQ 하위 카드 + 기능 모달 7종

기능 목록을 먼저 놓고 그 아래에 집중한 것(MCP 도구 설계)을 뒀다.
description 이 오케스트레이션의 절반 · 실패도 status 로 반환 ·
쓰기 3종 전부 INSERT 전용 · 신원은 서버 주입 · 확장 도구는 기본 비활성 ·
권한을 문서가 아니라 DB 트리거로 강제.

평가 축 이야기를 넣었다 — 합계 71.1->88.9 가 아니라 오특정 16.7%->1.1%
가 실제로 고친 것이다. 수신 어댑터는 "설계상 없음"(미착수 아님).

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0178E3o2o2BuCsyArzc1XSsr
EOF
)"
```

---

## Task 9: SpendQ 카드 전면 교체 + AS_OF 갱신

**Files:**
- Modify: `index.html:2542-2625` (PROJECT 03 카드)
- Modify: `index.html` — `AS_OF` 상수 (현재 `index.html:3172`)

- [ ] **Step 1: `pc-meta` 기간 교체**

현재 `2026.08 · 개인 1인 · 개인 설계 프로젝트 · 프로토타입` →
KO `2026.08~09 · 개인 1인 · 실작업 7일 · 커밋 99건` / EN `Aug–Sep 2026 · solo · 7 working days · 99 commits`

- [ ] **Step 2: "문제 정의" 유지, "설계 포인트" 4개 유지**

현재 내용이 정확하므로 그대로 둔다. 단 4번째 불릿의 "호환이 아니라 확장"은 유지.

- [ ] **Step 3: 기능 목록 블록 신설 (모달 없음 — GIF 미촬영)**

GIF 가 없으므로 **모달 대신 정적 목록**으로 둔다. `.feat` 대신 일반 `<ul>` 을 쓴다
(누를 수 없는 것을 누를 수 있게 보이면 안 된다).

내용: SPEC §3-E "넣을 것" 중 검증 하네스·F-13·S3 3개를 `<ul>` 로.

- [ ] **Step 4: `impact` 블록 전면 교체**

현재 문단(*"온체인 프로그램과 에이전트 루프는 착수 단계에서 멈춰 있다"*)을 지우고:

```html
                <div class="impact block">
                  <div class="bh"><span class="star">&#9733;</span> <span data-ko="현재 상태 (2026.09.10 실측)" data-en="Status (measured 2026-09-10)">현재 상태 (2026.09.10 실측)</span></div>
                  <p data-ko="백엔드·온체인·프론트·배포까지 게이트를 두고 전건 통과했고, <b>Cloud Run 6서비스가 devnet 에 라이브</b>로 떠 있다. 오프체인 테스트 <b>297건 전건 통과</b> · 온체인 22건. 검증 하네스에서 불량 검출이 기저 <b>15/18</b>에서 Gemini 카탈로그를 포함해 <b>18/18</b>로 올라갔고, 오탐은 <b>0/3</b>, 100회 반복 재현율은 <b>100%</b>다. <b>다만 대회 제출물 4종 중 영상과 PPT는 미착수</b>이고 devnet 전용이다."
                    data-en="Backend, on-chain, frontend and deployment all passed their gates, and <b>six Cloud Run services are live on devnet</b>. 297 off-chain tests pass (plus 22 on-chain). In the verification harness the defect catch rate goes from <b>15/18</b> on base checks to <b>18/18</b> with the Gemini-selected catalogue, with <b>0/3</b> false positives and <b>100%</b> reproducibility over 100 runs. <b>The demo video and deck are not made</b>, and it is devnet only.">백엔드·온체인·프론트·배포까지 게이트를 두고 전건 통과했고, <b>Cloud Run 6서비스가 devnet 에 라이브</b>로 떠 있다. 오프체인 테스트 <b>297건 전건 통과</b> · 온체인 22건. 검증 하네스에서 불량 검출이 기저 <b>15/18</b>에서 Gemini 카탈로그를 포함해 <b>18/18</b>로 올라갔고, 오탐은 <b>0/3</b>, 100회 반복 재현율은 <b>100%</b>다. <b>다만 대회 제출물 4종 중 영상과 PPT는 미착수</b>이고 devnet 전용이다.</p>
                  <p class="mono" style="font-size:11px;color:var(--muted);margin-top:8px" data-ko="※ 즉시정산 할인 −6.0%는 우리가 600bps로 설정한 값이 그대로 적용된 결과이지 시장 실측이 아니다."
                    data-en="Note: the −6.0% early-settlement discount is our own 600bps setting applied as-is, not a market measurement.">※ 즉시정산 할인 −6.0%는 우리가 600bps로 설정한 값이 그대로 적용된 결과이지 시장 실측이 아니다.</p>
                  <div class="metricrow">
                    <div class="metric">
                      <div class="mv"><span data-count="297">0</span>건</div>
                      <div class="ml" data-ko="오프체인 테스트" data-en="off-chain tests">오프체인 테스트</div>
                    </div>
                    <div class="metric">
                      <div class="mv"><span data-count="6">0</span>서비스</div>
                      <div class="ml" data-ko="devnet 라이브" data-en="live on devnet">devnet 라이브</div>
                    </div>
                    <div class="metric">
                      <div class="mv"><span data-count="100">0</span>%</div>
                      <div class="ml" data-ko="판정 재현율 (100회)" data-en="verdict reproducibility">판정 재현율 (100회)</div>
                    </div>
                  </div>
                </div>
```

- [ ] **Step 5: 영상 자리 주석**

`pc-actions` 앞에:

```html
                <!-- 데모 영상 촬영 완료되면 아래를 featlist 로 바꾸고 모달을 추가하세요 (assets/spendq/).
                     리허설은 통과했고 촬영 절차·큐시트가 확정돼 있습니다 — 설계서 §3-E 참고. -->
```

- [ ] **Step 6: `AS_OF` 갱신**

```js
    const AS_OF = { y: 2026, m: 9, d: 11 };
```

`.sec-asof` 의 하드코딩된 `2026.09.04` 도 함께 고친다 (JS 가 덮어쓰지만 JS 실패 시 대비):

```html
        <p class="sec-asof mono" data-ko="진행 상황 기준일 · 2026.09.11" data-en="Status as of 2026-09-11">진행 상황 기준일 · 2026.09.11</p>
```

- [ ] **Step 7: 검증 + 커밋**

```bash
python tools/check_page.py && start index.html
grep -n "2026.09.04\|2026-09-04" index.html
```

두 번째 명령 기대: 출력 없음(전부 갱신됨).

```bash
git add index.html && git commit -m "$(cat <<'EOF'
SpendQ 카드를 실측 상태로 교체 + 기준일 2026-09-11

"착수 단계에서 멈춰 있다"는 사실과 달랐다. 백엔드·온체인·프론트·배포가
전부 완성됐고 Cloud Run 6서비스가 devnet 라이브다. 검증 하네스 수치와
프롬프트 인젝션 케이스(F-13), 앱을 지워도 체인이 막는다는 S3 증명을 넣었다.

영상·PPT 미착수와 devnet 전용은 그대로 남겼고, -6.0% 가 설정값이지
시장 실측이 아니라는 것을 함께 적었다.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0178E3o2o2BuCsyArzc1XSsr
EOF
)"
```

---

## Task 10: 인쇄본 동기화

**Files:**
- Modify: `print/index.html`

인쇄본은 **중첩 드롭다운도 모달도 쓰지 않는다.** 같은 사실을 전부 펼친 형태로 싣는다.

- [ ] **Step 1: 현재 Q 시리즈 블록 확인**

```bash
grep -n "qn\|FinAllQ\|InsuQ\|MaintQ\|SpendQ" print/index.html | head -30
```

`print/index.html:1054-1082` 근처의 `<div class="qn">` 3개가 대상이다.

- [ ] **Step 2: Q 시리즈 3종 본문 교체**

각 `<div class="qn">` 블록을 SPEC §3-B/C/D 의 **기능 목록 + 집중한 것 + 실측** 요약으로 교체한다.
인쇄본이므로 GIF·SVG 없이 **텍스트만**. 각 프로젝트당 대략:

- 한 줄 정의 + 기간
- 주요 기능 (FinAllQ 7 / InsuQ 4 / MaintQ 7) — 한 줄씩
- 집중한 것 (FinAllQ: 왜 LLM이 없는가 / InsuQ: RAG 측정 / MaintQ: MCP 설계) — 2~3줄
- 실측 수치 한 줄

- [ ] **Step 3: QMesh 성과 문단 정정**

`print/index.html:1082` 근처의 *"제조(MaintQ)는 호출자 측 A2A 도구까지 구현했고, 수신 어댑터가 다음 단계다"* 를
SPEC §3-A 에 맞춰 고친다 — 수신 어댑터는 **설계상 없음**(하지 않기로 한 일)이지 다음 단계가 아니다.
"3경로"도 **5경로**로 정정한다.

- [ ] **Step 4: SpendQ 블록 교체**

`print/index.html` 의 SpendQ 상태 문단을 Task 9 Step 4 와 같은 사실로 교체한다.

- [ ] **Step 5: 기준일 갱신**

```bash
grep -n "2026.09.04\|2026-09-04" print/index.html
```

나오는 곳을 전부 `2026.09.11` / `2026-09-11` 로 고친다.

- [ ] **Step 6: 검증 + 커밋**

```bash
python tools/check_page.py && start print/index.html
grep -c "2026.09.04" print/index.html
```

브라우저에서 Ctrl+P 미리보기로 확인: 잘리는 문단이 없고, 페이지 나눔이 카드 중간을 자르지 않는다.

```bash
git add print/index.html && git commit -m "$(cat <<'EOF'
인쇄본을 index.html 과 같은 사실로 동기화

Q 시리즈 3종을 기능 목록 + 집중한 것 + 실측으로 펼쳐 실었다
(인쇄본은 중첩 드롭다운도 모달도 쓰지 않는다).

QMesh 성과를 정정했다 — 3경로 -> 5경로, 그리고 MaintQ 수신 어댑터는
"다음 단계"가 아니라 설계상 하지 않기로 한 일이다. SpendQ 도 실측 상태로.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0178E3o2o2BuCsyArzc1XSsr
EOF
)"
```

---

## Task 11: 종단 검증

**Files:** 없음 (검증만). 결함을 찾으면 해당 태스크로 돌아가 고친다.

- [ ] **Step 1: 기계 검사**

```bash
python tools/check_page.py && python tools/optimize_assets.py && git status --short
```

기대: `통과`, 자산 재생성 후 `git status` 가 비어 있다(멱등성 확인).

- [ ] **Step 2: 모달 20개 전수**

```bash
python - <<'PY'
import re, pathlib
s = pathlib.Path('index.html').read_text(encoding='utf-8')
refs = set(re.findall(r'data-modal="([^"]+)"', s))
ids  = set(re.findall(r'<section id="(f-[^"]+)"', s))
print(f'버튼 {len(refs)}개 / 모달 {len(ids)}개')
print('버튼만 있음:', sorted(refs - ids) or '없음')
print('모달만 있음:', sorted(ids - refs) or '없음')
PY
```

기대: `버튼 20개 / 모달 20개`, 양쪽 차집합 모두 `없음`.
(QMesh 2 + FinAllQ 7 + InsuQ 4 + MaintQ 7 = 20)

- [ ] **Step 3: 브라우저 전수 확인**

`start index.html` 후 SPEC §6 표를 그대로 밟는다:

1. **중첩 토글** — QMesh 를 열고 하위 3개를 각각 열었다 닫는다. **부모가 닫히지 않고 본문이 잘리지 않는다**
2. **모달 20개** — 전부 열리고 ESC·배경·✕ 3경로로 닫힌다
3. **모달 언어** — 모달을 **연 상태에서** KO/EN 전환 → 문구가 바뀐다
4. **GIF 지연 로딩** — Network 탭에서 초기 `.gif` 요청 **0건**, 모달을 열면 그때 뜬다
5. **테마** — 다크로 전환해 SVG 다이어그램 4종(QMesh 2 · InsuQ 1 · FinAllQ 7 · MaintQ 7)이 전부 읽힌다
6. **모바일** — 개발자 도구를 400px 폭으로 놓고 가로 스크롤이 생기지 않는지 본다
7. **인쇄** — Ctrl+P 미리보기에서 하위 카드가 펼쳐지고 모달이 안 나온다

- [ ] **Step 4: 사실 대조**

SPEC §3 의 각 수치를 `resume/` 원본과 1:1 로 다시 맞춘다. 특히:

```bash
grep -n "0.8148\|0.6346\|1,098\|1,771\|1,559\|297\|123\|D1~D141\|15/18\|18/18" index.html
```

각 수치 옆의 **분모·조건이 함께 적혀 있는지** 확인한다 (Global Constraint 7).

- [ ] **Step 5: README 갱신**

`README.md` 의 `AS_OF` 설명 예시를 `2026, m: 9, d: 11` 로 맞추고,
자산 디렉터리(`assets/`)와 두 도구(`tools/optimize_assets.py` · `tools/check_page.py`)를 한 줄씩 추가한다.

- [ ] **Step 6: 최종 커밋 + 배포**

```bash
git add README.md && git commit -m "$(cat <<'EOF'
README: assets/ 와 tools/ 규약 추가, AS_OF 예시 갱신

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0178E3o2o2BuCsyArzc1XSsr
EOF
)"
git push origin master
```

push 후 1~3분 뒤 `https://ttogle918.github.io` 에서 Step 3 의 1·2·4 를 **배포본으로 다시 확인**한다
(로컬 `file://` 과 달리 경로 대소문자·MIME 이 엄격하다).

---

## Self-Review

**Spec coverage**

| SPEC § | 태스크 |
|---|---|
| §2 자산 정책 | Task 1 |
| §3-A QMesh | Task 5 |
| §3-B FinAllQ | Task 6 |
| §3-C InsuQ | Task 7 |
| §3-D MaintQ | Task 8 |
| §3-E SpendQ | Task 9 |
| §4-1 하위 드롭다운 | Task 3 (CSS) · Task 4 (JS) |
| §4-2 모달 | Task 3 (CSS) · Task 4 (JS) · Task 5~8 (마크업) |
| §4-3 인쇄 | Task 3 Step 3 (CSS) · Task 10 (본문) |
| §4-4 언어 | Global Constraint 2 · Task 2 C2/C3 |
| §4-5 기준일 | Task 9 Step 6 |
| §5 표기 규약 | Global Constraints 6·7·8 |
| §6 검증 | Task 11 |
| §7 후속 | 범위 밖 — 계획에 없음 (의도) |

**빠진 것 없음.**

**타입·이름 일관성** — 클래스명은 Task 3 에서 정의하고 Task 4~8 이 그대로 쓴다:
`.subcards` `.subcard` `.sub-top` `.sub-headings` `.sub-code` `.sub-title` `.sub-meta` `.sub-caret`
`.sub-body` `.sub-inner` `.featlist` `.feat` `.fmodal` `.fmodal-card` `.fmodal-x` `.fmodal-kicker`
`.fmodal-title` `.fmodal-body` `.fmodal-fig` `.fdiag` `.fsteps`.
모달 id 규약: `f-<project>-<feature>` — Task 2 의 C5 검사가 `id^="f-"` 를 전제하므로 이 접두사는 필수다.
