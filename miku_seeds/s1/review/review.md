# miku_chibi_sprite See-through 단계별 검토

- 만든 도구: `tools/review_seethrough.py --run seethrough_test/miku_grow_seed1` (모델 실행 없음, 기존 파일만 읽음)
- 원본: `miku_chibi_sprite.png` (1312x1199)
- 중간 파일: `C:\Users\SSAFY\Desktop\borry\seethrough_work_2026-11-23\i2l\seethrough_test\miku_grow_seed1\miku_chibi_sprite`

## step20_preprocess.png (2-0 전처리)
- 긴 변 1312에 맞춰 정사각형 패딩(좌우 0px, 위아래 56px) → 1024로 축소 (0.78배)

## step21_body_tags.png (2-1 LayerDiff 몸 단계)
| 태그 | 픽셀 |
|---|---|
| front hair | 47,383 |
| back hair | 191,036 |
| head | 41,299 |
| neck | 0 |
| neckwear | 0 |
| topwear | 18,115 |
| handwear | 27,029 |
| bottomwear | 12,697 |
| legwear | 33,275 |
| footwear | 24,605 |
| tail | 0 |
| wings | 0 |
| objects | 0 |

- 빈 레이어 5개: neck, neckwear, tail, wings, objects

## step22_head_crop.png (2-2 머리 자르기)
- 초록: head.png 범위 / 빨강: 실제 자르기 상자(여백 1/5, 코드 계산 재현) / 보라: headwear.png
- head 범위(1024): (404, 235, 647, 458), 자르기 상자(1024): [355, 190, 694, 501]
- headwear가 상자 경계에 닿은 쪽(잘림 의심): 없음

- head_grow 1회 (주황=이전 회차 상자): 0:[355, 190, 694, 501] 닿음=[] 확장=[]

## step23_head_tags.png (2-3 LayerDiff 머리 단계)
| 태그 | 픽셀 |
|---|---|
| headwear | 0 |
| face | 33,590 |
| irides | 3,379 |
| eyebrow | 453 |
| eyewhite | 4,525 |
| eyelash | 2,393 |
| eyewear | 0 |
| ears | 0 |
| earwear | 0 |
| nose | 0 |
| mouth | 114 |

- 빈 레이어 5개: headwear, eyewear, ears, earwear, nose

## step24_depth.png (2-4 Marigold 깊이)
- PSD 레이어를 깊이 중앙값(psd.json) 순서로 배치, 레이어 안은 <태그>_depth.png를 색으로 표시
| 순서 | 레이어 | 깊이 중앙값 |
|---|---|---|
| 1 | front hair | 0.035 |
| 2 | eyelash-r | 0.102 |
| 3 | irides-r | 0.153 |
| 4 | eyelash-l | 0.216 |
| 5 | irides-l | 0.235 |
| 6 | eyewhite-r | 0.294 |
| 7 | eyewhite-l | 0.294 |
| 8 | eyebrow-l | 0.322 |
| 9 | eyebrow-r | 0.349 |
| 10 | mouth | 0.430 |
| 11 | face | 0.431 |
| 12 | handwear-r | 0.490 |
| 13 | topwear | 0.553 |
| 14 | bottomwear | 0.596 |
| 15 | legwear | 0.706 |
| 16 | handwear-l | 0.749 |
| 17 | footwear | 0.812 |
| 18 | back hair | 0.914 |

- reconstruction.png vs src_img.png PSNR(흰 배경): 24.4 dB

## step25_psd_stack.png (2-5 PSD 조립)
- PSD 레이어 18개를 아래(먼 쪽)부터 하나씩 쌓아 가는 모습, 빨간 상자 = 방금 추가한 레이어 범위
- 생성PNG차이/원본차이: 레이어 픽셀 RGB 평균 차이 (0이면 그 파일 그대로)
| PSD 순서(아래→위) | 레이어 | bbox | 픽셀 | 생성PNG 차이 | 원본 차이 | 픽셀 출처 |
|---|---|---|---|---|---|---|
| 0 | back hair | (157, 161, 868, 815) | 191,036 | 0.0 | 21.3 | 생성 PNG |
| 1 | footwear | (366, 146, 686, 417) | 24,605 | 0.0 | 61.9 | 생성 PNG |
| 2 | handwear-l | (546, 463, 700, 677) | 14,100 | 0.0 | 48.4 | 생성 PNG |
| 3 | legwear | (411, 610, 672, 864) | 33,275 | 0.0 | 26.8 | 생성 PNG |
| 4 | bottomwear | (448, 583, 648, 670) | 12,697 | 0.0 | 47.5 | 생성 PNG |
| 5 | topwear | (469, 446, 621, 640) | 18,115 | 0.0 | 19.2 | 생성 PNG |
| 6 | handwear-r | (373, 462, 508, 674) | 12,929 | 0.0 | 11.4 | 생성 PNG |
| 7 | face | (448, 250, 641, 459) | 33,590 | 0.0 | 65.6 | 생성 PNG |
| 8 | mouth | (545, 433, 558, 443) | 114 | 68.5 | 0.0 | 원본 픽셀 |
| 9 | eyebrow-r | (477, 320, 540, 334) | 256 | 0.0 | 98.4 | 생성 PNG |
| 10 | eyebrow-l | (591, 328, 638, 339) | 197 | 0.0 | 107.3 | 생성 PNG |
| 11 | eyewhite-r | (467, 360, 530, 415) | 2,837 | 0.0 | 125.6 | 생성 PNG |
| 12 | eyewhite-l | (586, 366, 629, 420) | 1,688 | 0.0 | 125.9 | 생성 PNG |
| 13 | irides-l | (588, 367, 620, 419) | 1,275 | 0.0 | 26.7 | 생성 PNG |
| 14 | eyelash-l | (585, 356, 639, 404) | 917 | 0.0 | 59.3 | 생성 PNG |
| 15 | irides-r | (480, 358, 524, 415) | 2,104 | 0.0 | 23.0 | 생성 PNG |
| 16 | eyelash-r | (458, 350, 538, 402) | 1,476 | 0.0 | 44.2 | 생성 PNG |
| 17 | front hair | (404, 179, 703, 470) | 47,383 | 0.0 | 11.7 | 생성 PNG |

- PSD 전체 합성 vs src_img.png PSNR(흰 배경): 26.1 dB

## step26_coverage.png (2-6 품질: 어디가 빠졌나)
- 원본에만 있음(빠짐, 빨강): 2,144px / PSD에만 있음(파랑): 7px / 둘 다: 300,355px
- 둘 다 있는 곳 중 색 차이 > 40: 8,679px
- 빠진 덩어리 큰 순서 (x, y, w, h, 픽셀): (437, 147, 21, 29, 221), (475, 440, 27, 24, 198), (555, 444, 52, 17, 80), (406, 295, 10, 28, 59), (435, 429, 18, 12, 50)
- 초록 상자 = 2-2 머리 자르기 상자 (상자 밖의 머리 장식은 생성되지 않음)

## step27_hidden_parts.png (8⑤ 가려진 부분 확인)
- 각 레이어를 혼자 띄움, 초록 = 그 위 레이어들에 가려지는 부분(앞 레이어를 움직이면 드러날 곳)
| 레이어(앞→뒤) | 픽셀 | 가려지는 픽셀 | 비율 |
|---|---|---|---|
| front hair | 47,383 | 0 | 0% |
| eyelash-r | 1,476 | 179 | 12% |
| irides-r | 2,104 | 340 | 16% |
| eyelash-l | 917 | 83 | 9% |
| irides-l | 1,275 | 159 | 12% |
| eyewhite-l | 1,688 | 1,485 | 88% |
| eyewhite-r | 2,837 | 2,375 | 84% |
| eyebrow-l | 197 | 89 | 45% |
| eyebrow-r | 256 | 104 | 41% |
| mouth | 114 | 0 | 0% |
| face | 33,590 | 22,200 | 66% |
| handwear-r | 12,929 | 0 | 0% |
| topwear | 18,115 | 1,906 | 11% |
| bottomwear | 12,697 | 5,342 | 42% |
| legwear | 33,275 | 6,783 | 20% |
| handwear-l | 14,100 | 6,857 | 49% |
| footwear | 24,605 | 7,672 | 31% |
| back hair | 191,036 | 38,369 | 20% |

## stages_strip.png
- src_img.png · head.png · src_head.png · face_depth.png · back hair_depth.png · reconstruction.png
