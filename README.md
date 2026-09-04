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
const AS_OF = { y: 2026, m: 9, d: 4 };
```

여기서 히어로 배지(`.as-of` — `26.09 기준`)와 프로젝트 섹션(`.sec-asof` — `2026.09.04`)을
**함께** 렌더합니다. 카드 수치를 갱신했다면 **이 한 줄만 고치면 두 곳이 따라옵니다.**
두 곳을 따로 고치지 마세요 — 갈라집니다.

> ⚠️ **스프린트 번호처럼 주 단위로 변하는 값은 카드 본문에 직접 쓰지 마세요.**
> 2026-08-29 기준으로 적은 "FinAllQ Sprint 4"가 **6일 만에 Sprint 21**이 됐습니다.
> "A2A 수신 어댑터·FDS·감사 로그 운영"처럼 **한동안 변하지 않는 사실**로 쓰세요.

감사 이력과 판단 근거: [`docs/superpowers/specs/2026-09-04-portfolio-content-audit-design.md`](docs/superpowers/specs/2026-09-04-portfolio-content-audit-design.md)

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
