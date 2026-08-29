# 프로젝트 랜딩 페이지 규약

이 문서는 **포트폴리오 사이트(`ttogle918.github.io`)와 각 프로젝트 레포를 연결하는 규칙**입니다.
다른 레포에서 이 문서만 읽어도 자기 랜딩 페이지를 어디에 어떻게 두면 되는지 알 수 있도록 썼습니다.

- 포트폴리오 본문: <https://ttogle918.github.io> (레포 `ttogle918/ttogle918.github.io`, `index.html` 단일 파일)
- 이 디렉터리: `project/` — 외부 레포 Pages로 보내는 **리다이렉트 스텁**들이 사는 곳

---

## 1. 두 가지 형태 중 하나를 고른다

| | **A. 직접 호스팅** | **B. 리다이렉트 스텁** |
|---|---|---|
| 경로 | `/<slug>/` | `/project/<slug>/` |
| 파일 위치 | 포트폴리오 레포의 `<slug>/index.html` | 포트폴리오 레포의 `project/<slug>/index.html` |
| 실제 내용 | 포트폴리오 레포 안에 있음 | **프로젝트 자기 레포**의 GitHub Pages에 있음 |
| 예시 | `qmesh/` → <https://ttogle918.github.io/qmesh/> | `project/key-manager/home/` → <https://ttogle918.github.io/key-manager/> |
| 언제 쓰나 | 프로젝트 레포가 비공개거나, Pages를 따로 안 띄울 때 | 프로젝트 레포가 **자기 Pages를 이미 띄우고 있을 때** |

> **판단 기준 한 줄**: 프로젝트 레포에서 `gh-pages`나 `Settings → Pages`를 켤 생각이면 **B**,
> 아니면 **A**를 쓰세요.

### slug 규칙

- 소문자 + 하이픈만. 레포 이름을 그대로 쓰는 것을 원칙으로 합니다 (`key-manager`, `k-bridge`).
- 레포 이름과 제품 이름이 다르면 **레포 이름**을 따릅니다.
  (레포 `key-manager` / 제품 "키지기(KeyLens)" → slug는 `key-manager`)

---

## 2. 현황

| # | 프로젝트 | slug | 형태 | 랜딩 URL | 상태 |
|---|---|---|---|---|---|
| 01 | QMesh | `qmesh` | A | <https://ttogle918.github.io/qmesh/> | ✅ |
| 02 | KeyLens (키지기) | `key-manager` | B | <https://ttogle918.github.io/key-manager/> | ✅ |
| 03 | SpendQ | `spendq` | 미정 | — | ⬜ |
| 04 | SecureAI Engine | `secureai` | 미정 | — | ⬜ |
| 05 | K-Bridge | `k-bridge` | 미정 | — | ⬜ |
| 06 | KOCRUIT | `kocruit` | 미정 | — | ⬜ |
| 07 | 질문-답변 검색 (비상교육) | `visang-qa` | 미정 | — | ⬜ |
| 08 | 이탈 고객 예측 (비상교육) | `visang-churn` | 미정 | — | ⬜ |

번호는 포트폴리오 `index.html`의 프로젝트 카드 번호와 같습니다 (최신순).

---

## 3. 연결하는 법 — 2단계

### 1단계. 랜딩을 배치한다

**A(직접 호스팅)를 고른 경우** — 포트폴리오 레포에 `<slug>/index.html`을 만듭니다.
`qmesh/index.html`을 복사해서 내용만 바꾸는 게 가장 빠릅니다. 작성 규칙은 아래 4장 참고.

**B(리다이렉트 스텁)를 고른 경우** — `project/<slug>/index.html`에 아래를 넣습니다.
`project/key-manager/home/index.html`을 복사해 **3군데(URL 2번, 표시 문구)** 만 바꾸면 됩니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>프로젝트명 — 프로젝트 페이지로 이동 중</title>
<meta name="description" content="한 줄 소개." />
<link rel="canonical" href="https://ttogle918.github.io/<slug>/" />
<meta http-equiv="refresh" content="0; url=https://ttogle918.github.io/<slug>/" />
<!-- 스타일은 project/key-manager/home/index.html에서 그대로 복사 -->
</head>
<body>
  <div class="card">
    <div class="mono">project / &lt;slug&gt;</div>
    <h1>프로젝트명 페이지로 이동합니다…</h1>
    <p>자동으로 넘어가지 않으면 아래 버튼을 눌러주세요.</p>
    <a class="btn" href="https://ttogle918.github.io/&lt;slug&gt;/">프로젝트명 바로가기 →</a>
  </div>
</body>
</html>
```

> `<meta http-equiv="refresh">`만으로 즉시 넘어가지만, 자바스크립트·리프레시가 막힌 환경을 위해
> 버튼을 반드시 함께 둡니다.

### 2단계. 포트폴리오 카드에서 주석을 푼다

포트폴리오 `index.html`의 각 프로젝트 카드에는 **붙여넣을 자리가 주석으로 미리 적혀 있습니다.**

```
<!-- 랜딩 준비되면 아래 줄을 pc-actions 안에 붙여넣으세요 (slug: secureai)
     <a class="gobtn" href="project/secureai/"><span class="ic" data-ic="link"></span><span data-ko="상세 설명" data-en="Details">상세 설명</span></a> -->
```

`index.html`에서 **`랜딩 준비되면`** 으로 검색하면 남은 자리가 전부 나옵니다.

- A(직접 호스팅)를 골랐다면 `href`를 `project/<slug>/`가 아니라 `<slug>/`로 바꿔주세요.
- 주석을 풀고 나면 이 문서의 **2. 현황** 표도 ✅로 갱신합니다.

> 링크가 없는 동안에는 **버튼을 두지 않습니다.** 죽은 `href="#"`는 클릭 시 페이지 맨 위로 튀어
> 미완성으로 보이기 때문에, 주석으로만 남겨둡니다.

---

## 4. 랜딩 페이지 작성 규칙 (A를 고른 경우)

포트폴리오 본문과 동일한 방식을 따릅니다. 기준 파일은 `qmesh/index.html`입니다.

- **단일 HTML 파일.** CSS·JS를 전부 인라인으로 넣어 빌드·의존성 설치가 없게 합니다. (폰트만 CDN)
- **KO/EN 전환**: 모든 문구를 `data-ko` / `data-en` 두 속성에 넣습니다.
  페이지 로드 시 스크립트가 `data-ko` 값으로 덮어쓰므로, 문구를 바꿀 때는
  **두 속성과 태그 안쪽 내용을 함께** 고쳐야 합니다.
- **라이트/다크**: 루트의 `data-theme` 속성으로 전환하고, 색은 전부 CSS 변수로 뺍니다.
- **무거운 자산은 지연 로딩**: 데모 GIF처럼 큰 파일은 클릭해야 내려받도록 합니다
  (`qmesh/assets/`가 이 방식입니다).

### 자산 두는 위치

| 종류 | 위치 | 비고 |
|---|---|---|
| 데모 GIF·스크린샷 | `<slug>/assets/` | 원본은 각 프로젝트 레포에 두고 복사해 옵니다 |
| 발표자료 PDF·PPTX | `uploads/` | 파일명은 `<프로젝트>_presentation.pdf` 형식 |

---

## 5. 프로젝트 레포 쪽에서 할 일

자기 레포에서 Pages를 띄우는 경우(형태 B), 레포 README에 아래 두 줄을 넣어두면
양방향으로 찾아가기 쉬워집니다.

```markdown
- 랜딩 페이지: https://ttogle918.github.io/<slug>/
- 포트폴리오: https://ttogle918.github.io (프로젝트 카드 NN번)
```

`key-manager` 레포가 이 형태의 예시입니다.
