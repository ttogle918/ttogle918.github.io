# ttogle918.github.io

최지현 · AI Agent / 백엔드 엔지니어 포트폴리오 사이트.

**🔗 배포 주소: https://ttogle918.github.io**

`index.html` 한 파일로 이루어진 정적 페이지입니다. CSS·JS가 모두 인라인으로 들어있어 별도 빌드나 의존성 설치가 필요 없습니다. (폰트만 CDN 사용)

## 로컬에서 확인하기

브라우저로 `index.html`을 바로 열면 됩니다.

```bash
# Windows
start index.html

# macOS
open index.html
```

또는 로컬 서버로 띄우려면:

```bash
# Python 3
python -m http.server 8000
# → http://localhost:8000 접속
```

## 수정하기

- 모든 내용·스타일·스크립트는 `index.html` 안에 있습니다.
- 텍스트는 한/영 전환을 위해 `data-ko` / `data-en` 속성에 각각 들어있습니다. 문구를 바꿀 때는 **두 속성과 태그 안쪽 내용을 함께** 수정하세요.
- 우측 상단 버튼으로 **KO/EN 언어**, **라이트/다크 테마**를 전환할 수 있습니다.

### 진행 상황 기준일 (`AS_OF`)

프로젝트 카드에는 진행 중인 값(버전·커밋 수·측정치)이 들어갑니다. 이 값들이 **언제 것인지**
밝히는 기준일은 스크립트 10번의 상수 한 곳에 있습니다.

```js
const AS_OF = { y: 2026, m: 9, d: 11 };
```

여기서 히어로 배지(`.as-of` — `26.09 기준`)와 프로젝트 섹션(`.sec-asof` — `2026.09.11`)을
**함께** 렌더합니다. 카드 수치를 갱신했다면 **이 한 줄만 고치면 두 곳이 따라옵니다.**
두 곳을 따로 고치지 마세요 — 갈라집니다.

> ⚠️ **스프린트 번호처럼 주 단위로 변하는 값은 카드 본문에 직접 쓰지 마세요.**
> 2026-08-29 기준으로 적은 "FinAllQ Sprint 4"가 **6일 만에 Sprint 21**이 됐습니다.
> "A2A 수신 어댑터·FDS·감사 로그 운영"처럼 **한동안 변하지 않는 사실**로 쓰세요.

감사 이력과 판단 근거: [`docs/superpowers/specs/2026-09-04-portfolio-content-audit-design.md`](docs/superpowers/specs/2026-09-04-portfolio-content-audit-design.md)

### 데모 자산 (`assets/`)

프로젝트 카드의 **기능 모달**에 들어가는 실제 화면 캡처·GIF 26종이 `assets/<프로젝트>/`에 있습니다.
원본은 각 프로젝트 레포(전부 private)에 그대로 있고, 그중 **골라 담은 것만** 이 public 레포에
들어옵니다 — 파일 단위 선택적 공개입니다.

```bash
python tools/optimize_assets.py   # 원본 → assets/ 재생성 (26.9MB → 5.7MB)
```

`assets/`를 직접 손대지 마세요. 자산을 바꿀 때는 **원본 레포를 고친 뒤 이 스크립트를 다시**
돌립니다. 멱등하므로 내용이 같으면 실행 후 `git status`가 비어 있습니다. 원본을 못 찾으면
조용히 넘어가지 않고 그 자리에서 실패합니다.

모달 이미지는 **모달을 열 때** `data-src` → `src`로 바꿔 받아옵니다. 첫 화면에서는 한 건도
내려받지 않습니다 (마크업에 `src`를 직접 쓰면 이 규약이 깨집니다).

### 구조 검사 (`tools/check_page.py`)

브라우저를 열기 전에는 보이지 않는 결함 5종을 잡습니다. **본문을 고쳤으면 커밋 전에 돌리세요.**

```bash
python tools/check_page.py        # index.html · print/index.html
```

| | 검사 | 놓치면 |
|---|---|---|
| C1 | `data-modal="X"` 에 대응하는 `id="X"` | 모달이 안 열린다 |
| C2 | `data-ko` / `data-en` 이 쌍인가 | 전환할 때 문구가 사라진다 |
| C3 | `data-ko` 안에 `<img>`·`<svg>` 가 없는가 | `applyLang()` 이 `innerHTML` 로 지운다 |
| C4 | `data-src` 경로의 파일이 실재하는가 | 죽은 이미지 |
| C5 | 모달 `section` 안에 `data-count` 가 없는가 | 숨김 상태에선 발화하지 않아 `0` 으로 남는다 |

## 배포

`master` 브랜치에 push하면 GitHub Pages가 자동으로 빌드·배포합니다. (보통 1~3분 소요)

```bash
git add .
git commit -m "메시지"
git push origin master
```

## 프로젝트 랜딩 페이지

포트폴리오 본문(`index.html`)과 별개로, 개별 프로젝트는 자체 랜딩 페이지를 가집니다.

**📘 규약·현황·연결 절차는 [`project/README.md`](project/README.md)에 정리되어 있습니다.**
다른 레포에서 읽어도 되도록 그쪽에 몰아뒀으니, 새 랜딩을 만들 때는 그 문서를 보세요.

요약하면 두 가지 형태만 씁니다.

| 형태 | 경로 | 예시 |
|---|---|---|
| **직접 호스팅** | `/<slug>/` → `<slug>/index.html` | `qmesh/` |
| **리다이렉트 스텁** | `/project/<slug>/` → 외부 레포의 GitHub Pages | `project/key-manager/home/` |

현재 연결된 것은 **QMesh · KeyLens** 2개이고, 나머지 6개는 `index.html`에 붙여넣을 자리만
주석으로 남아 있습니다 (`랜딩 준비되면`으로 검색).

- 데모 GIF: `qmesh/assets/` (원본은 QMesh 레포 `docs/presentation/assets/`). 용량이 커서 클릭해야
  내려받도록 지연 로딩합니다.
- 발표자료: `uploads/QMesh_presentation.pdf` · `.pptx`

## 대표작 표시

`★ AI AGENT 대표작` 배지는 AI 에이전트를 직접 설계한 프로젝트에 붙입니다. 현재 **QMesh · SecureAI
Engine · K-Bridge** 3개입니다. 추가하려면 카드의 `<article>`에 `featured` 클래스를 넣고 제목 옆에
`<span class="pc-featured">`를 붙이면 됩니다.

## 남은 작업

- [ ] 프로젝트 카드 다이어그램 이미지 추가 (`.pc-slide`는 아직 캡션 플레이스홀더 15개)
- [ ] 03~08번 랜딩 페이지 제작 후 위 표와 `index.html` 주석 해제
- [ ] 🔴 **`uploads/최지현_portfolio.pdf` 갱신** (현재 2026-07-09판) — 헤더 PDF 버튼이 이 파일을
  그대로 내려줍니다. 2026-09-04 감사로 사이트 본문은 최신인데 **PDF만 2개월 전 내용이라
  둘이 서로 다른 말을 합니다.** NIPA 수료·QMesh·KeyLens v0.5.1·SecureAI Sprint 0~30 미반영
- [ ] `uploads/QMesh_presentation.pdf` 재출력 (현재 8/24판, `.pptx`는 8/25 최종판)
- [ ] KOCRUIT 기여도 40% 근거 확인 (커밋 수 기준으로는 789건 중 289건 = 36.6%)
- [ ] 오픈소스 개발자대회 결과 나오면 KeyLens 카드의 "결과 대기" 갱신
