# miku 레이어 조합 1 (miku_pick1)

선택(사용자, 2026-11-24) → 스펙 [miku_pick1.json](miku_pick1.json), 도구 `tools/mix_layers.py`

| 레이어 | seed | 처리 |
|---|---|---|
| front hair | s9 | Claude 선택 (seed 간 차이 거의 없음) |
| tail_left / tail_right | s0 back hair | 연결 조각 좌우 분리 (이미지 기준 왼/오) |
| back_center | oldPC42 back hair | **시도**: s0 트윈테일(4px 넓혀) 빼고 가장 큰 조각 |
| face · irides · eyebrow · eyewhite · eyelash · mouth | s1 | mouth: 깊이 0.43 고정(얼굴 앞) + 색은 원본 픽셀 (생성 가장자리 회색 테두리 제거) |
| neck | s2 | PSD에 넣되 꺼둠 |
| topwear | s8 | |
| handwear-l / -r | s8 | 좌우 분리 |
| bottomwear | s4 | |
| legwear | s1 | |
| headwear | s6 | 분리 안 함 (나중에 트윈테일 앞/뒤로 나눌 예정) |

- 순서 = 레이어마다 자기 seed의 깊이 중앙값 (가까운 → 먼): `miku_pick1/sheet.png`
- 확인: `miku_pick1/check.png` (원본 | 조합 | 빨강=빠짐 2,014px · 파랑=넘침 26px · 노랑=색 차이) · PSNR 32.3dB
- 색: 보이는 픽셀은 모두 원본 색 (반투명 가장자리는 불투명 레이어가 나올 때까지 밑 레이어도 원본 색), 가려진 부분만 생성 색 → 레이어 가장자리 선·테두리 제거
- PSD: `miku_pick1/mix.psd` (17레이어, neck 꺼짐) · 레이어 PNG: `miku_pick1/layers/NN_이름.png` (00 = 맨 앞)

---
# 조합 2 (miku_pick2): back_center를 로컬 모델로 다시 만듦

pick1과 같고 **back_center만 교체** → 스펙 [miku_pick2.json](miku_pick2.json)

1. **분리 (text_layers.py)**: oldPC42 `back hair.png` → Grounding DINO("twin tail" 좌/우 박스) + SAM2(마스크) + LaMa(트윈테일 밑 48px 띠) → `back_center_process/debug_labels.png`, `02_back_center.png`
2. **가려진 부분 생성 (amodal_complete.py, SDXL 인페인팅)**: 트윈테일(oldPC42 + s0)에 가려진 자리를 SDXL이 그림 → 후보 `back_center_process/candidates.png`
   - hull: 둥근 외곽을 잇지만 오른쪽이 직선으로 잘린 채 남음
   - key seed0: 분홍 조각 · key seed2: 얼굴 옆모습이 그려짐 → 탈락
   - **key seed1 채택** (색 오차 2.8, 둥근 뒤통수 + 양옆 윤곽선)
3. 머리카락 3장(tail_left · tail_right · back_center)은 원본 색 복사 제외(`keep_rgb`) — seed가 달라 모양이 원본과 어긋나서, 복사하면 다른 부위 선이 찍힘
- 확인: `miku_pick2/back_hair_check.png` (뒤통수만 · 뒷머리 3장 · 전체 합성), PSNR 30.0dB
- 남은 점: back_center 오른쪽 가장자리에 얇은 보라색 테두리(key 모드 마젠타 잔여)

## pick2 마무리 (7·8단계)
- 빠진 윤곽선 1,846px(762조각, 모두 레이어에서 3.7px 이내) → 가장 가까운 레이어에 원본 픽셀로 (`fill_missing`) → **빠짐 0px**, PSNR 30.9dB
- back_center 보라 테두리 488px → 가장 가까운 깨끗한 색(검은 윤곽선)으로 (`despill`)
- **`miku_pick2/hidden.png`**: 레이어마다 혼자 놓고, 앞 레이어에 가려지는 부분을 초록으로 표시 (앞 레이어를 옮기면 드러나는 곳). 윤곽 안에 체커보드(구멍)가 없으면 통과

## pick2 두 버전 (레이어 검은 선 문제)
- 원인: "보이는 픽셀은 원본 색"(visible_rgb) 처리가 레이어에 **다른 부위의 선**을 찍음. seed가 달라 레이어 모양이 원본과 1~3px 어긋나는 자리 + 앞 레이어 반투명 가장자리 밑 → 원본의 그 자리 선(앞머리 윤곽·눈 테두리·치마 밑단)이 복사됨
- **`miku_pick2_srccolor/`** (A, 이전 pick2): 합성이 원본에 가장 가까움(PSNR 30.9) · 레이어 face·legwear·handwear 등에 남의 선
- **`miku_pick2_clean/`** (B): 모든 레이어 생성 색 그대로(See-through 기본과 같음), mouth만 원본 색 · 레이어 깨끗 · 합성은 생성 색(PSNR 27.8, "01" 글자 등 세부가 생성된 모양)
- 비교: **[variants_compare.png](variants_compare.png)** (위 A · 아래 B / 레이어 5장 + 얼굴·몸 합성 확대)
