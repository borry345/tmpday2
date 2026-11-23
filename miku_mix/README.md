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
- 확인: `miku_pick1/check.png` (원본 | 조합 | 빨강=빠짐 2,014px · 파랑=넘침 26px · 노랑=색 차이) · PSNR 27.2dB
- PSD: `miku_pick1/mix.psd` (17레이어, neck 꺼짐) · 레이어 PNG: `miku_pick1/layers/NN_이름.png` (00 = 맨 앞)
