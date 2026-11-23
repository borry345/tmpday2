# miku_chibi_sprite See-through 단계별 검토

- 만든 도구: `tools/review_seethrough.py --run seethrough_test/miku_grow_seed6` (모델 실행 없음, 기존 파일만 읽음)
- 원본: `miku_chibi_sprite.png` (1312x1199)
- 중간 파일: `C:\Users\SSAFY\Desktop\borry\seethrough_work_2026-11-23\i2l\seethrough_test\miku_grow_seed6\miku_chibi_sprite`

## step20_preprocess.png (2-0 전처리)
- 긴 변 1312에 맞춰 정사각형 패딩(좌우 0px, 위아래 56px) → 1024로 축소 (0.78배)

## step21_body_tags.png (2-1 LayerDiff 몸 단계)
| 태그 | 픽셀 |
|---|---|
| front hair | 47,322 |
| back hair | 235,015 |
| head | 40,545 |
| neck | 0 |
| neckwear | 0 |
| topwear | 18,192 |
| handwear | 26,229 |
| bottomwear | 12,132 |
| legwear | 34,527 |
| footwear | 0 |
| tail | 0 |
| wings | 0 |
| objects | 26,967 |

- 빈 레이어 5개: neck, neckwear, footwear, tail, wings

## step22_head_crop.png (2-2 머리 자르기)
- 초록: head.png 범위 / 빨강: 실제 자르기 상자(여백 1/5, 코드 계산 재현) / 보라: headwear.png
- head 범위(1024): (432, 231, 649, 459), 자르기 상자(1024): [334, 128, 691, 503]
- headwear가 상자 경계에 닿은 쪽(잘림 의심): 없음

- head_grow 2회 (주황=이전 회차 상자): 0:[388, 184, 691, 502] 닿음=['left', 'top'] 확장=['left', 'top'] → 1:[334, 128, 691, 503] 닿음=[] 확장=[]

## step23_head_tags.png (2-3 LayerDiff 머리 단계)
| 태그 | 픽셀 |
|---|---|
| headwear | 19,878 |
| face | 38,245 |
| irides | 3,462 |
| eyebrow | 460 |
| eyewhite | 4,702 |
| eyelash | 2,347 |
| eyewear | 0 |
| ears | 0 |
| earwear | 0 |
| nose | 0 |
| mouth | 117 |

- 빈 레이어 4개: eyewear, ears, earwear, nose

## step24_depth.png (2-4 Marigold 깊이)
- PSD 레이어를 깊이 중앙값(psd.json) 순서로 배치, 레이어 안은 <태그>_depth.png를 색으로 표시
| 순서 | 레이어 | 깊이 중앙값 |
|---|---|---|
| 1 | front hair | 0.043 |
| 2 | eyelash-r | 0.094 |
| 3 | irides-r | 0.153 |
| 4 | eyelash-l | 0.218 |
| 5 | irides-l | 0.239 |
| 6 | eyewhite-r | 0.286 |
| 7 | eyewhite-l | 0.286 |
| 8 | eyebrow-l | 0.298 |
| 9 | eyebrow-r | 0.345 |
| 10 | handwear-r | 0.412 |
| 11 | mouth | 0.426 |
| 12 | face | 0.427 |
| 13 | topwear | 0.569 |
| 14 | headwear | 0.584 |
| 15 | bottomwear | 0.608 |
| 16 | legwear | 0.686 |
| 17 | handwear-l | 0.729 |
| 18 | objects | 0.773 |
| 19 | back hair | 0.914 |

- reconstruction.png vs src_img.png PSNR(흰 배경): 24.6 dB

## step25_psd_stack.png (2-5 PSD 조립)
- PSD 레이어 19개를 아래(먼 쪽)부터 하나씩 쌓아 가는 모습, 빨간 상자 = 방금 추가한 레이어 범위
- 생성PNG차이/원본차이: 레이어 픽셀 RGB 평균 차이 (0이면 그 파일 그대로)
| PSD 순서(아래→위) | 레이어 | bbox | 픽셀 | 생성PNG 차이 | 원본 차이 | 픽셀 출처 |
|---|---|---|---|---|---|---|
| 0 | back hair | (157, 161, 868, 815) | 235,015 | 0.0 | 32.4 | 생성 PNG |
| 1 | objects | (363, 146, 686, 423) | 26,967 | 0.0 | 64.8 | 생성 PNG |
| 2 | handwear-l | (548, 463, 700, 678) | 13,274 | 0.0 | 46.1 | 생성 PNG |
| 3 | legwear | (411, 604, 672, 864) | 34,527 | 0.0 | 29.9 | 생성 PNG |
| 4 | bottomwear | (451, 588, 648, 670) | 12,132 | 0.0 | 44.4 | 생성 PNG |
| 5 | headwear | (367, 145, 685, 419) | 19,878 | 0.0 | 42.4 | 생성 PNG |
| 6 | topwear | (470, 445, 621, 639) | 18,192 | 0.0 | 20.9 | 생성 PNG |
| 7 | face | (440, 230, 649, 455) | 38,245 | 0.0 | 65.6 | 생성 PNG |
| 8 | mouth | (545, 433, 558, 444) | 117 | 49.0 | 0.0 | 원본 픽셀 |
| 9 | handwear-r | (373, 462, 508, 674) | 12,955 | 0.0 | 11.7 | 생성 PNG |
| 10 | eyebrow-r | (476, 321, 539, 334) | 268 | 0.0 | 96.9 | 생성 PNG |
| 11 | eyebrow-l | (591, 328, 634, 339) | 192 | 0.0 | 96.4 | 생성 PNG |
| 12 | eyewhite-r | (465, 359, 529, 416) | 2,946 | 0.0 | 131.8 | 생성 PNG |
| 13 | eyewhite-l | (586, 364, 629, 420) | 1,756 | 0.0 | 131.2 | 생성 PNG |
| 14 | irides-l | (588, 366, 620, 420) | 1,331 | 0.0 | 29.1 | 생성 PNG |
| 15 | eyelash-l | (585, 356, 637, 405) | 890 | 0.0 | 52.9 | 생성 PNG |
| 16 | irides-r | (480, 359, 524, 415) | 2,131 | 0.0 | 23.2 | 생성 PNG |
| 17 | eyelash-r | (455, 352, 538, 402) | 1,343 | 0.0 | 32.4 | 생성 PNG |
| 18 | front hair | (404, 180, 704, 471) | 47,322 | 0.0 | 11.2 | 생성 PNG |

- PSD 전체 합성 vs src_img.png PSNR(흰 배경): 26.2 dB

## step26_coverage.png (2-6 품질: 어디가 빠졌나)
- 원본에만 있음(빠짐, 빨강): 1,843px / PSD에만 있음(파랑): 50px / 둘 다: 300,656px
- 둘 다 있는 곳 중 색 차이 > 40: 9,493px
- 빠진 덩어리 큰 순서 (x, y, w, h, 픽셀): (554, 445, 52, 14, 108), (393, 575, 35, 41, 55), (471, 456, 23, 15, 54), (486, 451, 13, 7, 48), (365, 338, 6, 26, 45)
- 초록 상자 = 2-2 머리 자르기 상자 (상자 밖의 머리 장식은 생성되지 않음)

## step27_hidden_parts.png (8⑤ 가려진 부분 확인)
- 각 레이어를 혼자 띄움, 초록 = 그 위 레이어들에 가려지는 부분(앞 레이어를 움직이면 드러날 곳)
| 레이어(앞→뒤) | 픽셀 | 가려지는 픽셀 | 비율 |
|---|---|---|---|
| front hair | 47,322 | 0 | 0% |
| eyelash-r | 1,343 | 169 | 13% |
| irides-r | 2,131 | 365 | 17% |
| eyelash-l | 890 | 63 | 7% |
| irides-l | 1,331 | 207 | 16% |
| eyewhite-l | 1,756 | 1,560 | 89% |
| eyewhite-r | 2,946 | 2,485 | 84% |
| eyebrow-l | 192 | 83 | 43% |
| eyebrow-r | 268 | 111 | 41% |
| handwear-r | 12,955 | 0 | 0% |
| mouth | 117 | 0 | 0% |
| face | 38,245 | 27,527 | 72% |
| topwear | 18,192 | 1,742 | 10% |
| headwear | 19,878 | 4,269 | 21% |
| bottomwear | 12,132 | 4,781 | 39% |
| legwear | 34,527 | 8,010 | 23% |
| handwear-l | 13,274 | 6,047 | 46% |
| objects | 26,967 | 24,692 | 92% |
| back hair | 235,015 | 82,497 | 35% |

## stages_strip.png
- src_img.png · head.png · src_head.png · face_depth.png · back hair_depth.png · reconstruction.png
