"""각 프로젝트 레포의 데모 자산을 이 레포의 assets/ 로 최적화 복사한다.

왜 이 레포에 담는가: MaintQ·InsuQ·FinAllQ·SpendQ 레포가 전부 private 이라
raw 핫링크도 Pages 리다이렉트도 성립하지 않는다. 파일 단위로 고른 것만
public 인 이 레포에 담는 것이 곧 선택적 공개다. (설계서 §2)

원본은 각 프로젝트 레포에 그대로 남는다 — 화질이 아쉬우면 MAXW 를 올려
다시 돌리면 된다. 멱등하다.

필요 패키지: Pillow, opencv-python(cv2). ffmpeg 는 쓰지 않는다.
"""
from __future__ import annotations

import sys as _sys
for _stream in (_sys.stdout, _sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")  # Windows cp949 콘솔에서 한국어 출력이 죽는다
    except Exception:
        pass

import io
import shutil
import sys
from pathlib import Path

import cv2
from PIL import Image, ImageSequence

# 모달 표시 폭은 최대 ~760px 다. 900px 면 고해상도 화면에서도 충분하고,
# 1280~1568px 원본 대비 용량이 약 1/5 로 떨어진다(실측).
MAXW = 900
COLORS = 128

WS = Path(__file__).resolve().parents[2]    # .../workspace
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
    "qmesh/multihop-assess-loan.gif": "A2A_Q/docs/presentation/assets/03-maintq-finallq-insuq-assess-loan.gif",
    # KeyLens 는 레포에 데모 GIF 가 이미 있다 — 값은 전부 더미다(docs/demo/README.md).
    "keylens/classify.gif": "key-manager/docs/demo/demo.gif",
    "keylens/env-import.gif": "key-manager/docs/demo/env-import-walkthrough.gif",
    "keylens/features.gif": "key-manager/docs/demo/feature-walkthrough.gif",
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


# 아키텍처·흐름도 PNG 는 열어서 읽는 그림이라 GIF 보다 넉넉히 남긴다.
# 카드에서는 max-height:180px 썸네일이지만, 새 탭으로 열면 글자가 읽혀야 한다.
MAXW_DIAG = 1600
DIAG_COLORS = 256

SPENDQ_SHOTS = "//wsl.localhost/Ubuntu/home/hyun/spendq/docs/cuecard/shots/"

DIAGRAMS: dict[str, str] = {
    "kbridge/workflow.png": "LawGenie/meeting-notes/architecture/workflow.png",
    "kbridge/system_architecture.png": "LawGenie/meeting-notes/architecture/system_architecture.png",
    "kbridge/product_registration_flow.png":
        "LawGenie/meeting-notes/architecture/product_registration_requirement_workflowflow.png",
    # 도식이 아니라 Docker Desktop 컨테이너 목록이다 — 실제로 뜬 스택을 보여준다.
    "secureai/stack.png": "secureai-editor/docs/demo/architecture_layers_docker.png",
    # SpendQ 는 WSL 안에 산다. UNC 경로는 절대경로라 WS / rel 이 그대로 받는다.
    # docs/cuecard/ 의 촬영 큐카드가 각 장이 무슨 장면인지 적어 둔 «테이크 실물»이다.
    "spendq/auction.png": SPENDQ_SHOTS + "console.png",
    "spendq/refund.png": SPENDQ_SHOTS + "learn.png",
    "spendq/chain-blocks.png": SPENDQ_SHOTS + "explorer-fail.png",
}

SECUREAI_DEMO = "secureai-editor/docs/demo/01_Kkebi_SAST-PATCH-PR_녹음 2026-06-28 115918.mp4"

# 영상에서 뽑은 정지 프레임. 이 데모는 내레이션이라 대부분 멈춰 있어 GIF 로 만들면
# 움직임 없이 용량만 커진다(실측 1.5~3.9MB). 한 장씩 PNG 로 뽑으면 170KB 안쪽이다.
SHOTS: dict[str, tuple[str, float]] = {
    # 대상 파일: (원본 영상, 초)
    "secureai/vulnerabilities.png": (SECUREAI_DEMO, 110.0),
    "secureai/auto-pr.png": (SECUREAI_DEMO, 228.0),
}


def frame_to_png(src: Path, sec: float,
                 maxw: int = MAXW_DIAG, colors: int = DIAG_COLORS) -> bytes:
    """영상의 sec 지점 한 프레임을 PNG 로 굽는다."""
    cap = cv2.VideoCapture(str(src))
    if not cap.isOpened():
        raise RuntimeError(f"영상을 열 수 없다: {src}")
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(sec * cap.get(cv2.CAP_PROP_FPS)))
    ok, img = cap.read()
    cap.release()
    if not ok:
        raise RuntimeError(f"프레임을 못 읽었다: {src} @{sec}s")
    im = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.quantize(colors=colors, method=Image.MEDIANCUT).save(buf, format="PNG", optimize=True)
    return buf.getvalue()


# 시연 영상에서 잘라낸 GIF. GIF 원본이 없고 mp4 밖에 없는 프로젝트용.
# 화면이 2748x1530 으로 조밀해서 기존 GIF 규칙(900px/128색)으로는 4MB 를 넘는다.
# 800px/64색/5fps 로 낮춰 기존 최대치(request-settlement 1.17MB) 수준에 맞췄다.
CLIP_MAXW = 800
CLIP_COLORS = 64
CLIP_FPS = 5

KBRIDGE_DEMO = "LawGenie/K-Bridge Ecommerce/시연영상—2025-10-13 150029.mp4"

CLIPS: dict[str, tuple[str, float, float]] = {
    # 대상 파일: (원본 영상, 시작초, 끝초)
    "kbridge/requirement-verdict.gif": (KBRIDGE_DEMO, 96.0, 101.0),
    "kbridge/precedent-cross.gif": (KBRIDGE_DEMO, 106.0, 111.0),
}


def clip_to_gif(src: Path, start: float, end: float,
                fps_out: int = CLIP_FPS, maxw: int = CLIP_MAXW,
                colors: int = CLIP_COLORS) -> bytes:
    """영상의 [start, end) 구간을 GIF 로 굽는다 (OpenCV 로 읽고 Pillow 로 씀).

    ffmpeg 를 쓰지 않는다 — 이 환경에 없다. cv2 만으로 프레임을 뽑는다.
    """
    cap = cv2.VideoCapture(str(src))
    if not cap.isOpened():
        raise RuntimeError(f"영상을 열 수 없다: {src}")
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames: list[Image.Image] = []
    t = start
    while t < end:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * fps)))
        ok, img = cap.read()
        if not ok:
            break
        im = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if im.width > maxw:
            im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
        frames.append(im.convert("P", palette=Image.ADAPTIVE, colors=colors))
        t += 1 / fps_out
    cap.release()
    if not frames:
        raise RuntimeError(f"프레임을 못 읽었다: {src} [{start}~{end}]")
    buf = io.BytesIO()
    frames[0].save(
        buf, format="GIF", save_all=True, append_images=frames[1:],
        duration=int(1000 / fps_out), loop=0, optimize=True, disposal=2,
    )
    return buf.getvalue()


def shrink_png(src: Path, maxw: int = MAXW_DIAG, colors: int = DIAG_COLORS) -> bytes:
    """다이어그램 PNG 를 흰 배경에 합성 → 축소 → 팔레트화.

    투명 배경을 그대로 두면 다크 테마에서 검은 글씨가 검은 배경에 얹혀 안 보인다.
    다이어그램은 색 수가 적어 팔레트화 손실이 눈에 띄지 않는다(실측 540KB -> 83KB).
    """
    im = Image.open(src).convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    im = Image.alpha_composite(bg, im).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.quantize(colors=colors, method=Image.MEDIANCUT).save(buf, format="PNG", optimize=True)
    return buf.getvalue()


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

    for dest_rel, (src_rel, sec) in SHOTS.items():
        src = WS / src_rel
        if not src.exists():
            missing.append(src_rel)
            continue
        dest = SITE / "assets" / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        data = frame_to_png(src, sec)
        dest.write_bytes(data)
        total_before += src.stat().st_size
        total_after += len(data)
        print(f"  {dest_rel:42s} 영상 {sec:.0f}초 -> {len(data)/1e3:5.0f}KB")

    for dest_rel, (src_rel, a, b) in CLIPS.items():
        src = WS / src_rel
        if not src.exists():
            missing.append(src_rel)
            continue
        dest = SITE / "assets" / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        data = clip_to_gif(src, a, b)
        dest.write_bytes(data)
        before, after = src.stat().st_size, len(data)
        total_before += before
        total_after += after
        print(f"  {dest_rel:42s} {before/1e6:5.1f}MB 영상 -> {after/1e6:5.2f}MB ({a:.0f}~{b:.0f}초)")

    for dest_rel, src_rel in DIAGRAMS.items():
        src = WS / src_rel
        if not src.exists():
            missing.append(src_rel)
            continue
        dest = SITE / "assets" / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        data = shrink_png(src)
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
