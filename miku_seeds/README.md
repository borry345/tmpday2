# miku_chibi_sprite See-through seed 비교 (2026-11-23)

- 원본: `miku_chibi_sprite.png` (1312x1199) → 1024 정사각형으로 생성
- 설정: NF4 · 1024 · 30 steps · `--tblr_split` · **머리 자르기 반복(HeadGrow 3)** · seed 0~9
- `oldPC42/` = 이전 PC(RTX 3070) seed 42 결과(머리 자르기 반복 없음), 참고용

## 먼저 볼 것
1. **[seed_compare_grow.png](seed_compare_grow.png)**: 행 = 레이어, 열 = oldPC42 · s0~s9 (빈 레이어는 빨간 0px)
2. 고른 seed의 `sN/review/`: 단계별 검토 이미지

## seed 요약
| seed | headwear | face | 뒤통수(back hair) | PSD PSNR | 메모 |
|---|---|---|---|---|---|
| s0 | ✔ 4조각 | ✖ 빔 | ✖ 트윈테일만 | 22.9 | |
| s1 | ✖ (footwear 칸으로 감) | ✔ | △ 띠 | 26.1 | |
| s2 | ✔ 위 2조각 | ✔ | △ 띠 | 25.3 | neck 있음 |
| s3 | ✖ (확장 후 사라짐) | ✔ | △ 띠 | 20.6 | ears 한쪽 |
| s4 | ✔ 4조각 | ✔ | ✔ | 26.7 | 상자 3회 |
| s5 | ✖ | △ 회색 얼룩 | ✖ 구멍 | 21.9 | mouth 번짐, ears 양쪽 |
| s6 | ✔ (objects에도 중복) | ✔ | ✔ | 26.2 | |
| s7 | ✖ | ✖ 빔 | ✔ | 20.3 | ears 한쪽 |
| s8 | ✔ 4조각 | ✖ 빔 | △ 띠 | 24.7 | |
| s9 | ✔ 4조각 | ✔ | ✔ | **26.9** | **추천** |
| oldPC42 | △ 위쪽 잘림 | ✔ | ✔ | 23.3 | 참고 |

## 폴더 구조 (seed마다 같음)
- `layers/`: 비어 있지 않은 태그 레이어 PNG (1024, 투명 배경). `head.png`는 자르기 기준용이라 PSD에는 안 들어감
- `review/`: 검토 이미지 (`tools/review_seethrough.py`)
  - `step21_body_tags.png` 몸 단계 13태그 · `step23_head_tags.png` 머리 단계 11태그
  - `step22_head_crop.png` 머리 자르기 상자 (주황 = 이전 회차, 빨강 = 최종, 보라 = headwear)
  - `step24_depth.png` 깊이 순서 · `step25_psd_stack.png` PSD 쌓는 과정
  - `step26_coverage.png` 빠진 곳(빨강) · `step27_hidden_parts.png` 가려지는 부분(초록)
  - `review.md` 수치 표
- `head_grow.json`: 회차별 머리 자르기 상자와 닿은 쪽 · `miku_chibi_sprite.psd.json`: PSD 레이어 깊이 · `summary.txt`: 시간·GPU 메모리

## 고르는 방법
레이어마다 쓸 seed를 정해서 알려 주세요 (예: "전부 s9", "전부 s9 + mouth는 s4").
