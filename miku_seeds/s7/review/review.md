# miku_chibi_sprite See-through 단계별 검토

- 만든 도구: `tools/review_seethrough.py --run seethrough_test/miku_grow_seed7` (모델 실행 없음, 기존 파일만 읽음)
- 원본: `miku_chibi_sprite.png` (1312x1199)
- 중간 파일: `C:\Users\SSAFY\Desktop\borry\seethrough_work_2026-11-23\i2l\seethrough_test\miku_grow_seed7\miku_chibi_sprite`

## step20_preprocess.png (2-0 전처리)
- 긴 변 1312에 맞춰 정사각형 패딩(좌우 0px, 위아래 56px) → 1024로 축소 (0.78배)

## step21_body_tags.png (2-1 LayerDiff 몸 단계)
| 태그 | 픽셀 |
|---|---|
| front hair | 47,533 |
| back hair | 235,877 |
| head | 42,431 |
| neck | 0 |
| neckwear | 0 |
| topwear | 18,073 |
| handwear | 25,762 |
| bottomwear | 11,644 |
| legwear | 32,570 |
| footwear | 0 |
| tail | 0 |
| wings | 0 |
| objects | 0 |

- 빈 레이어 6개: neck, neckwear, footwear, tail, wings, objects

## step22_head_crop.png (2-2 머리 자르기)
- 초록: head.png 범위 / 빨강: 실제 자르기 상자(여백 1/5, 코드 계산 재현) / 보라: headwear.png
- head 범위(1024): (427, 223, 649, 459), 자르기 상자(1024): [383, 175, 692, 504]
- headwear가 상자 경계에 닿은 쪽(잘림 의심): 없음

- head_grow 1회 (주황=이전 회차 상자): 0:[383, 175, 692, 504] 닿음=[] 확장=[]

## step23_head_tags.png (2-3 LayerDiff 머리 단계)
| 태그 | 픽셀 |
|---|---|
| headwear | 0 |
| face | 0 |
| irides | 3,429 |
| eyebrow | 503 |
| eyewhite | 4,604 |
| eyelash | 2,390 |
| eyewear | 0 |
| ears | 1,303 |
| earwear | 0 |
| nose | 0 |
| mouth | 103 |

- 빈 레이어 5개: headwear, face, eyewear, earwear, nose

## step24_depth.png (2-4 Marigold 깊이)
- PSD 레이어를 깊이 중앙값(psd.json) 순서로 배치, 레이어 안은 <태그>_depth.png를 색으로 표시
| 순서 | 레이어 | 깊이 중앙값 |
|---|---|---|
| 1 | front hair | 0.031 |
| 2 | eyelash-r | 0.098 |
| 3 | irides-r | 0.176 |
| 4 | eyelash-l | 0.216 |
| 5 | eyewhite-r | 0.259 |
| 6 | eyewhite-l | 0.259 |
| 7 | irides-l | 0.259 |
| 8 | eyebrow-r | 0.302 |
| 9 | eyebrow-l | 0.302 |
| 10 | handwear-r | 0.435 |
| 11 | ears | 0.455 |
| 12 | topwear | 0.580 |
| 13 | mouth | 0.598 |
| 14 | bottomwear | 0.624 |
| 15 | legwear | 0.682 |
| 16 | handwear-l | 0.706 |
| 17 | back hair | 0.898 |

- reconstruction.png vs src_img.png PSNR(흰 배경): 19.7 dB

## step25_psd_stack.png (2-5 PSD 조립)
- PSD 레이어 17개를 아래(먼 쪽)부터 하나씩 쌓아 가는 모습, 빨간 상자 = 방금 추가한 레이어 범위
- 생성PNG차이/원본차이: 레이어 픽셀 RGB 평균 차이 (0이면 그 파일 그대로)
| PSD 순서(아래→위) | 레이어 | bbox | 픽셀 | 생성PNG 차이 | 원본 차이 | 픽셀 출처 |
|---|---|---|---|---|---|---|
| 0 | back hair | (157, 161, 868, 815) | 235,877 | 0.0 | 35.0 | 생성 PNG |
| 1 | handwear-l | (548, 463, 700, 676) | 12,814 | 0.0 | 43.2 | 생성 PNG |
| 2 | legwear | (412, 616, 672, 864) | 32,570 | 0.0 | 23.8 | 생성 PNG |
| 3 | bottomwear | (457, 587, 648, 670) | 11,644 | 0.0 | 44.8 | 생성 PNG |
| 4 | mouth | (545, 433, 559, 442) | 103 | 63.1 | 0.0 | 원본 픽셀 |
| 5 | topwear | (469, 445, 621, 639) | 18,073 | 0.0 | 20.7 | 생성 PNG |
| 6 | ears | (598, 357, 632, 413) | 1,303 | 0.0 | 116.4 | 생성 PNG |
| 7 | handwear-r | (374, 461, 507, 674) | 12,948 | 0.0 | 11.1 | 생성 PNG |
| 8 | eyebrow-r | (470, 320, 539, 333) | 294 | 0.0 | 98.2 | 생성 PNG |
| 9 | eyebrow-l | (591, 327, 641, 339) | 209 | 0.0 | 110.1 | 생성 PNG |
| 10 | eyewhite-r | (466, 359, 530, 415) | 2,857 | 0.0 | 131.6 | 생성 PNG |
| 11 | eyewhite-l | (586, 364, 629, 419) | 1,747 | 0.0 | 133.5 | 생성 PNG |
| 12 | irides-l | (588, 366, 620, 419) | 1,298 | 0.0 | 26.9 | 생성 PNG |
| 13 | eyelash-l | (585, 356, 638, 405) | 902 | 0.0 | 55.8 | 생성 PNG |
| 14 | irides-r | (480, 358, 524, 414) | 2,131 | 0.0 | 23.2 | 생성 PNG |
| 15 | eyelash-r | (457, 352, 538, 402) | 1,364 | 0.0 | 37.1 | 생성 PNG |
| 16 | front hair | (404, 179, 704, 471) | 47,533 | 0.0 | 11.2 | 생성 PNG |

- PSD 전체 합성 vs src_img.png PSNR(흰 배경): 20.3 dB

## step26_coverage.png (2-6 품질: 어디가 빠졌나)
- 원본에만 있음(빠짐, 빨강): 6,977px / PSD에만 있음(파랑): 3px / 둘 다: 295,522px
- 둘 다 있는 곳 중 색 차이 > 40: 25,738px
- 빠진 덩어리 큰 순서 (x, y, w, h, 픽셀): (579, 150, 83, 48, 2282), (391, 146, 67, 52, 2242), (366, 340, 64, 97, 788), (623, 672, 32, 10, 80), (487, 539, 14, 33, 57)
- 초록 상자 = 2-2 머리 자르기 상자 (상자 밖의 머리 장식은 생성되지 않음)

## step27_hidden_parts.png (8⑤ 가려진 부분 확인)
- 각 레이어를 혼자 띄움, 초록 = 그 위 레이어들에 가려지는 부분(앞 레이어를 움직이면 드러날 곳)
| 레이어(앞→뒤) | 픽셀 | 가려지는 픽셀 | 비율 |
|---|---|---|---|
| front hair | 47,533 | 0 | 0% |
| eyelash-r | 1,364 | 183 | 13% |
| irides-r | 2,131 | 382 | 18% |
| eyelash-l | 902 | 84 | 9% |
| irides-l | 1,298 | 183 | 14% |
| eyewhite-l | 1,747 | 1,545 | 88% |
| eyewhite-r | 2,857 | 2,400 | 84% |
| eyebrow-l | 209 | 102 | 49% |
| eyebrow-r | 294 | 141 | 48% |
| handwear-r | 12,948 | 0 | 0% |
| ears | 1,303 | 1,196 | 92% |
| topwear | 18,073 | 1,631 | 9% |
| mouth | 103 | 0 | 0% |
| bottomwear | 11,644 | 4,289 | 37% |
| legwear | 32,570 | 6,022 | 18% |
| handwear-l | 12,814 | 5,613 | 44% |
| back hair | 235,877 | 60,156 | 26% |

## stages_strip.png
- src_img.png · head.png · src_head.png · face_depth.png · back hair_depth.png · reconstruction.png
