# miku_chibi_sprite See-through 단계별 검토

- 만든 도구: `tools/review_seethrough.py --run seethrough_test/miku_grow_seed8` (모델 실행 없음, 기존 파일만 읽음)
- 원본: `miku_chibi_sprite.png` (1312x1199)
- 중간 파일: `C:\Users\SSAFY\Desktop\borry\seethrough_work_2026-11-23\i2l\seethrough_test\miku_grow_seed8\miku_chibi_sprite`

## step20_preprocess.png (2-0 전처리)
- 긴 변 1312에 맞춰 정사각형 패딩(좌우 0px, 위아래 56px) → 1024로 축소 (0.78배)

## step21_body_tags.png (2-1 LayerDiff 몸 단계)
| 태그 | 픽셀 |
|---|---|
| front hair | 47,296 |
| back hair | 183,894 |
| head | 41,928 |
| neck | 0 |
| neckwear | 0 |
| topwear | 18,216 |
| handwear | 26,353 |
| bottomwear | 12,061 |
| legwear | 33,228 |
| footwear | 0 |
| tail | 0 |
| wings | 0 |
| objects | 0 |

- 빈 레이어 6개: neck, neckwear, footwear, tail, wings, objects

## step22_head_crop.png (2-2 머리 자르기)
- 초록: head.png 범위 / 빨강: 실제 자르기 상자(여백 1/5, 코드 계산 재현) / 보라: headwear.png
- head 범위(1024): (427, 227, 649, 459), 자르기 상자(1024): [327, 122, 692, 503]
- headwear가 상자 경계에 닿은 쪽(잘림 의심): 없음

- head_grow 2회 (주황=이전 회차 상자): 0:[383, 180, 692, 503] 닿음=['left', 'top'] 확장=['left', 'top'] → 1:[327, 122, 692, 503] 닿음=[] 확장=[]

## step23_head_tags.png (2-3 LayerDiff 머리 단계)
| 태그 | 픽셀 |
|---|---|
| headwear | 24,891 |
| face | 0 |
| irides | 3,412 |
| eyebrow | 523 |
| eyewhite | 4,504 |
| eyelash | 2,372 |
| eyewear | 0 |
| ears | 0 |
| earwear | 0 |
| nose | 0 |
| mouth | 120 |

- 빈 레이어 5개: face, eyewear, ears, earwear, nose

## step24_depth.png (2-4 Marigold 깊이)
- PSD 레이어를 깊이 중앙값(psd.json) 순서로 배치, 레이어 안은 <태그>_depth.png를 색으로 표시
| 순서 | 레이어 | 깊이 중앙값 |
|---|---|---|
| 1 | front hair | 0.043 |
| 2 | eyelash-r | 0.098 |
| 3 | irides-r | 0.165 |
| 4 | eyelash-l | 0.251 |
| 5 | irides-l | 0.282 |
| 6 | eyewhite-r | 0.290 |
| 7 | eyewhite-l | 0.290 |
| 8 | eyebrow-r | 0.329 |
| 9 | eyebrow-l | 0.329 |
| 10 | handwear-r | 0.357 |
| 11 | topwear | 0.569 |
| 12 | bottomwear | 0.624 |
| 13 | mouth | 0.694 |
| 14 | legwear | 0.718 |
| 15 | handwear-l | 0.741 |
| 16 | headwear | 0.745 |
| 17 | back hair | 0.898 |

- reconstruction.png vs src_img.png PSNR(흰 배경): 23.1 dB

## step25_psd_stack.png (2-5 PSD 조립)
- PSD 레이어 17개를 아래(먼 쪽)부터 하나씩 쌓아 가는 모습, 빨간 상자 = 방금 추가한 레이어 범위
- 생성PNG차이/원본차이: 레이어 픽셀 RGB 평균 차이 (0이면 그 파일 그대로)
| PSD 순서(아래→위) | 레이어 | bbox | 픽셀 | 생성PNG 차이 | 원본 차이 | 픽셀 출처 |
|---|---|---|---|---|---|---|
| 0 | back hair | (157, 162, 868, 815) | 183,894 | 0.0 | 19.8 | 생성 PNG |
| 1 | headwear | (368, 145, 685, 422) | 24,891 | 0.0 | 58.8 | 생성 PNG |
| 2 | handwear-l | (544, 461, 700, 678) | 13,257 | 0.0 | 46.0 | 생성 PNG |
| 3 | legwear | (411, 611, 672, 864) | 33,228 | 0.0 | 27.1 | 생성 PNG |
| 4 | mouth | (545, 432, 559, 443) | 120 | 62.4 | 0.0 | 원본 픽셀 |
| 5 | bottomwear | (446, 592, 649, 670) | 12,061 | 0.0 | 41.5 | 생성 PNG |
| 6 | topwear | (469, 443, 621, 639) | 18,216 | 0.0 | 18.5 | 생성 PNG |
| 7 | handwear-r | (373, 461, 509, 674) | 13,096 | 0.0 | 12.3 | 생성 PNG |
| 8 | eyebrow-r | (465, 320, 541, 334) | 307 | 0.0 | 100.3 | 생성 PNG |
| 9 | eyebrow-l | (590, 327, 641, 339) | 216 | 0.0 | 111.5 | 생성 PNG |
| 10 | eyewhite-r | (467, 359, 530, 415) | 2,824 | 0.0 | 138.0 | 생성 PNG |
| 11 | eyewhite-l | (586, 365, 628, 420) | 1,680 | 0.0 | 136.5 | 생성 PNG |
| 12 | irides-l | (588, 365, 620, 419) | 1,315 | 0.0 | 29.1 | 생성 PNG |
| 13 | eyelash-l | (585, 356, 638, 404) | 913 | 0.0 | 62.8 | 생성 PNG |
| 14 | irides-r | (480, 359, 524, 414) | 2,097 | 0.0 | 23.1 | 생성 PNG |
| 15 | eyelash-r | (456, 352, 538, 402) | 1,336 | 0.0 | 37.1 | 생성 PNG |
| 16 | front hair | (404, 179, 703, 471) | 47,296 | 0.0 | 11.4 | 생성 PNG |

- PSD 전체 합성 vs src_img.png PSNR(흰 배경): 24.7 dB

## step26_coverage.png (2-6 품질: 어디가 빠졌나)
- 원본에만 있음(빠짐, 빨강): 14,675px / PSD에만 있음(파랑): 62px / 둘 다: 287,824px
- 둘 다 있는 곳 중 색 차이 > 40: 10,010px
- 빠진 덩어리 큰 순서 (x, y, w, h, 픽셀): (459, 287, 169, 175, 11417), (593, 295, 22, 40, 418), (406, 267, 21, 56, 295), (377, 400, 59, 44, 126), (363, 334, 10, 37, 122)
- 초록 상자 = 2-2 머리 자르기 상자 (상자 밖의 머리 장식은 생성되지 않음)

## step27_hidden_parts.png (8⑤ 가려진 부분 확인)
- 각 레이어를 혼자 띄움, 초록 = 그 위 레이어들에 가려지는 부분(앞 레이어를 움직이면 드러날 곳)
| 레이어(앞→뒤) | 픽셀 | 가려지는 픽셀 | 비율 |
|---|---|---|---|
| front hair | 47,296 | 0 | 0% |
| eyelash-r | 1,336 | 173 | 13% |
| irides-r | 2,097 | 336 | 16% |
| eyelash-l | 913 | 74 | 8% |
| irides-l | 1,315 | 195 | 15% |
| eyewhite-l | 1,680 | 1,474 | 88% |
| eyewhite-r | 2,824 | 2,379 | 84% |
| eyebrow-l | 216 | 112 | 52% |
| eyebrow-r | 307 | 155 | 50% |
| handwear-r | 13,096 | 0 | 0% |
| topwear | 18,216 | 1,775 | 10% |
| bottomwear | 12,061 | 4,672 | 39% |
| mouth | 120 | 0 | 0% |
| legwear | 33,228 | 6,706 | 20% |
| handwear-l | 13,257 | 6,019 | 45% |
| headwear | 24,891 | 7,667 | 31% |
| back hair | 183,894 | 31,771 | 17% |

## stages_strip.png
- src_img.png · head.png · src_head.png · face_depth.png · back hair_depth.png · reconstruction.png
