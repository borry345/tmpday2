# miku_chibi_sprite See-through 단계별 검토

- 만든 도구: `tools/review_seethrough.py --run seethrough_test/miku_grow_seed9` (모델 실행 없음, 기존 파일만 읽음)
- 원본: `miku_chibi_sprite.png` (1312x1199)
- 중간 파일: `C:\Users\SSAFY\Desktop\borry\seethrough_work_2026-11-23\i2l\seethrough_test\miku_grow_seed9\miku_chibi_sprite`

## step20_preprocess.png (2-0 전처리)
- 긴 변 1312에 맞춰 정사각형 패딩(좌우 0px, 위아래 56px) → 1024로 축소 (0.78배)

## step21_body_tags.png (2-1 LayerDiff 몸 단계)
| 태그 | 픽셀 |
|---|---|
| front hair | 47,325 |
| back hair | 237,374 |
| head | 39,952 |
| neck | 0 |
| neckwear | 0 |
| topwear | 18,057 |
| handwear | 25,539 |
| bottomwear | 12,079 |
| legwear | 31,303 |
| footwear | 0 |
| tail | 0 |
| wings | 0 |
| objects | 0 |

- 빈 레이어 6개: neck, neckwear, footwear, tail, wings, objects

## step22_head_crop.png (2-2 머리 자르기)
- 초록: head.png 범위 / 빨강: 실제 자르기 상자(여백 1/5, 코드 계산 재현) / 보라: headwear.png
- head 범위(1024): (435, 228, 645, 459), 자르기 상자(1024): [341, 124, 686, 503]
- headwear가 상자 경계에 닿은 쪽(잘림 의심): right

- head_grow 2회 (주황=이전 회차 상자): 0:[393, 181, 686, 503] 닿음=['left', 'top'] 확장=['left', 'top'] → 1:[341, 124, 686, 503] 닿음=[] 확장=[]

## step23_head_tags.png (2-3 LayerDiff 머리 단계)
| 태그 | 픽셀 |
|---|---|
| headwear | 23,910 |
| face | 39,379 |
| irides | 3,445 |
| eyebrow | 479 |
| eyewhite | 4,405 |
| eyelash | 2,495 |
| eyewear | 0 |
| ears | 0 |
| earwear | 0 |
| nose | 0 |
| mouth | 127 |

- 빈 레이어 4개: eyewear, ears, earwear, nose

## step24_depth.png (2-4 Marigold 깊이)
- PSD 레이어를 깊이 중앙값(psd.json) 순서로 배치, 레이어 안은 <태그>_depth.png를 색으로 표시
| 순서 | 레이어 | 깊이 중앙값 |
|---|---|---|
| 1 | front hair | 0.051 |
| 2 | eyelash-r | 0.098 |
| 3 | irides-r | 0.176 |
| 4 | eyelash-l | 0.200 |
| 5 | irides-l | 0.227 |
| 6 | eyewhite-r | 0.239 |
| 7 | eyewhite-l | 0.239 |
| 8 | eyebrow-l | 0.294 |
| 9 | eyebrow-r | 0.361 |
| 10 | mouth | 0.434 |
| 11 | face | 0.435 |
| 12 | handwear-r | 0.467 |
| 13 | topwear | 0.569 |
| 14 | bottomwear | 0.624 |
| 15 | headwear | 0.659 |
| 16 | legwear | 0.710 |
| 17 | handwear-l | 0.737 |
| 18 | back hair | 0.906 |

- reconstruction.png vs src_img.png PSNR(흰 배경): 25.5 dB

## step25_psd_stack.png (2-5 PSD 조립)
- PSD 레이어 18개를 아래(먼 쪽)부터 하나씩 쌓아 가는 모습, 빨간 상자 = 방금 추가한 레이어 범위
- 생성PNG차이/원본차이: 레이어 픽셀 RGB 평균 차이 (0이면 그 파일 그대로)
| PSD 순서(아래→위) | 레이어 | bbox | 픽셀 | 생성PNG 차이 | 원본 차이 | 픽셀 출처 |
|---|---|---|---|---|---|---|
| 0 | back hair | (157, 161, 868, 815) | 237,374 | 0.0 | 26.9 | 생성 PNG |
| 1 | handwear-l | (549, 463, 700, 678) | 12,575 | 0.0 | 42.4 | 생성 PNG |
| 2 | legwear | (412, 625, 672, 864) | 31,303 | 0.0 | 20.4 | 생성 PNG |
| 3 | headwear | (367, 144, 685, 431) | 23,910 | 0.0 | 52.3 | 생성 PNG |
| 4 | bottomwear | (453, 588, 648, 670) | 12,079 | 0.0 | 43.5 | 생성 PNG |
| 5 | topwear | (470, 446, 621, 640) | 18,057 | 0.0 | 19.2 | 생성 PNG |
| 6 | handwear-r | (374, 462, 508, 675) | 12,964 | 0.0 | 12.1 | 생성 PNG |
| 7 | face | (438, 225, 642, 458) | 39,379 | 0.0 | 70.0 | 생성 PNG |
| 8 | mouth | (546, 432, 559, 444) | 127 | 59.6 | 0.0 | 원본 픽셀 |
| 9 | eyebrow-r | (475, 320, 540, 333) | 277 | 0.0 | 103.5 | 생성 PNG |
| 10 | eyebrow-l | (591, 327, 637, 338) | 202 | 0.0 | 108.6 | 생성 PNG |
| 11 | eyewhite-r | (467, 361, 530, 415) | 2,757 | 0.0 | 129.9 | 생성 PNG |
| 12 | eyewhite-l | (586, 366, 627, 419) | 1,648 | 0.0 | 132.2 | 생성 PNG |
| 13 | irides-l | (589, 365, 621, 419) | 1,313 | 0.0 | 26.5 | 생성 PNG |
| 14 | eyelash-l | (585, 355, 638, 404) | 899 | 0.0 | 56.6 | 생성 PNG |
| 15 | irides-r | (480, 358, 525, 414) | 2,132 | 0.0 | 24.0 | 생성 PNG |
| 16 | eyelash-r | (455, 352, 538, 402) | 1,351 | 0.0 | 39.1 | 생성 PNG |
| 17 | front hair | (404, 181, 704, 470) | 47,325 | 0.0 | 11.0 | 생성 PNG |

- PSD 전체 합성 vs src_img.png PSNR(흰 배경): 26.9 dB

## step26_coverage.png (2-6 품질: 어디가 빠졌나)
- 원본에만 있음(빠짐, 빨강): 1,256px / PSD에만 있음(파랑): 85px / 둘 다: 301,243px
- 둘 다 있는 곳 중 색 차이 > 40: 8,776px
- 빠진 덩어리 큰 순서 (x, y, w, h, 픽셀): (611, 175, 14, 19, 90), (624, 673, 30, 7, 63), (612, 536, 27, 33, 42), (377, 399, 24, 16, 39), (632, 453, 18, 17, 29)
- 초록 상자 = 2-2 머리 자르기 상자 (상자 밖의 머리 장식은 생성되지 않음)

## step27_hidden_parts.png (8⑤ 가려진 부분 확인)
- 각 레이어를 혼자 띄움, 초록 = 그 위 레이어들에 가려지는 부분(앞 레이어를 움직이면 드러날 곳)
| 레이어(앞→뒤) | 픽셀 | 가려지는 픽셀 | 비율 |
|---|---|---|---|
| front hair | 47,325 | 0 | 0% |
| eyelash-r | 1,351 | 185 | 14% |
| irides-r | 2,132 | 357 | 17% |
| eyelash-l | 899 | 79 | 9% |
| irides-l | 1,313 | 199 | 15% |
| eyewhite-l | 1,648 | 1,446 | 88% |
| eyewhite-r | 2,757 | 2,304 | 84% |
| eyebrow-l | 202 | 95 | 47% |
| eyebrow-r | 277 | 126 | 45% |
| mouth | 127 | 0 | 0% |
| face | 39,379 | 28,021 | 71% |
| handwear-r | 12,964 | 0 | 0% |
| topwear | 18,057 | 1,823 | 10% |
| bottomwear | 12,079 | 4,672 | 39% |
| headwear | 23,910 | 7,113 | 30% |
| legwear | 31,303 | 4,811 | 15% |
| handwear-l | 12,575 | 5,414 | 43% |
| back hair | 237,374 | 83,456 | 35% |

## stages_strip.png
- src_img.png · head.png · src_head.png · face_depth.png · back hair_depth.png · reconstruction.png
