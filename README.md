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

## 배포

`master` 브랜치에 push하면 GitHub Pages가 자동으로 빌드·배포합니다. (보통 1~3분 소요)

```bash
git add .
git commit -m "메시지"
git push origin master
```

## 프로젝트 랜딩 페이지

포트폴리오 본문(`index.html`)과 별개로, 개별 프로젝트는 자체 랜딩 페이지를 가집니다.

| 프로젝트 | 경로 | 소스 |
|---|---|---|
| **QMesh** (A2A 멀티 에이전트 오케스트레이션) | https://ttogle918.github.io/qmesh/ | `qmesh/index.html` |
| KeyLens (자격증명 관리) | https://ttogle918.github.io/key-manager/ | 별도 레포 (`key-manager`), `project/key-manager/home/`은 리다이렉트 스텁 |

`qmesh/index.html`도 `index.html`과 같은 방식입니다 — 단일 파일, CSS·JS 인라인, `data-ko`/`data-en`
속성으로 KO/EN 전환, `data-theme`으로 라이트/다크 전환. 문구를 바꿀 때는 **두 속성과 태그 안쪽 내용을
함께** 수정하세요.

- 데모 GIF: `qmesh/assets/` (원본은 QMesh 레포 `docs/presentation/assets/`). 용량이 커서 클릭해야
  내려받도록 지연 로딩합니다.
- 발표자료: `uploads/QMesh_presentation.pdf` · `.pptx`

## 남은 작업

- [ ] 프로젝트 카드 다이어그램 이미지 추가 (`.pc-slide`는 아직 캡션 플레이스홀더)
- [ ] 02~07번 카드의 `#` 링크 채우기 (PPT / 상세 설명 / 영상)
- [ ] `og-image.png` 및 파비콘 추가
