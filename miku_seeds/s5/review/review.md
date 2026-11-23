# miku_chibi_sprite See-through 단계별 검토

- 만든 도구: `tools/review_seethrough.py --run seethrough_test/miku_grow_seed5` (모델 실행 없음, 기존 파일만 읽음)
- 원본: `miku_chibi_sprite.png` (1312x1199)
- 중간 파일: `C:\Users\SSAFY\Desktop\borry\seethrough_work_2026-11-23\i2l\seethrough_test\miku_grow_seed5\miku_chibi_sprite`

## step20_preprocess.png (2-0 전처리)
- 긴 변 1312에 맞춰 정사각형 패딩(좌우 0px, 위아래 56px) → 1024로 축소 (0.78배)

## step21_body_tags.png (2-1 LayerDiff 몸 단계)
| 태그 | 픽셀 |
|---|---|
| front hair | 47,496 |
| back hair | 226,433 |
| head | 40,190 |
| neck | 0 |
| neckwear | 0 |
| topwear | 17,907 |
| handwear | 25,887 |
| bottomwear | 11,099 |
| legwear | 32,169 |
| footwear | 0 |
| tail | 0 |
| wings | 0 |
| objects | 0 |

- 빈 레이어 6개: neck, neckwear, footwear, tail, wings, objects

## step22_head_crop.png (2-2 머리 자르기)
- 초록: head.png 범위 / 빨강: 실제 자르기 상자(여백 1/5, 코드 계산 재현) / 보라: headwear.png
- head 범위(1024): (429, 233, 646, 459), 자르기 상자(1024): [385, 188, 688, 502]
- headwear가 상자 경계에 닿은 쪽(잘림 의심): 없음

- head_grow 1회 (주황=이전 회차 상자): 0:[385, 188, 688, 502] 닿음=[] 확장=[]

## step23_head_tags.png (2-3 LayerDiff 머리 단계)
| 태그 | 픽셀 |
|---|---|
| headwear | 0 |
| face | 30,984 |
| irides | 3,383 |
| eyebrow | 435 |
| eyewhite | 4,538 |
| eyelash | 2,389 |
| eyewear | 0 |
| ears | 3,297 |
| earwear | 0 |
| nose | 0 |
| mouth | 598 |

- 빈 레이어 4개: headwear, eyewear, earwear, nose

## step24_depth.png (2-4 Marigold 깊이)
- PSD 레이어를 깊이 중앙값(psd.json) 순서로 배치, 레이어 안은 <태그>_depth.png를 색으로 표시
| 순서 | 레이어 | 깊이 중앙값 |
|---|---|---|
| 1 | front hair | 0.047 |
| 2 | eyelash-r | 0.102 |
| 3 | irides-r | 0.169 |
| 4 | eyelash-l | 0.196 |
| 5 | irides-l | 0.239 |
| 6 | eyewhite-r | 0.251 |
| 7 | eyewhite-l | 0.251 |
| 8 | eyebrow-l | 0.259 |
| 9 | eyebrow-r | 0.263 |
| 10 | mouth | 0.345 |
| 11 | handwear-r | 0.439 |
| 12 | face | 0.451 |
| 13 | ears-r | 0.494 |
| 14 | ears-l | 0.494 |
| 15 | topwear | 0.541 |
| 16 | bottomwear | 0.608 |
| 17 | legwear | 0.667 |
| 18 | handwear-l | 0.729 |
| 19 | back hair | 0.906 |

- reconstruction.png vs src_img.png PSNR(흰 배경): 21.0 dB

## step25_psd_stack.png (2-5 PSD 조립)
- PSD 레이어 19개를 아래(먼 쪽)부터 하나씩 쌓아 가는 모습, 빨간 상자 = 방금 추가한 레이어 범위
- 생성PNG차이/원본차이: 레이어 픽셀 RGB 평균 차이 (0이면 그 파일 그대로)
| PSD 순서(아래→위) | 레이어 | bbox | 픽셀 | 생성PNG 차이 | 원본 차이 | 픽셀 출처 |
|---|---|---|---|---|---|---|
| 0 | back hair | (157, 161, 868, 815) | 226,433 | 0.0 | 31.1 | 생성 PNG |
| 1 | handwear-l | (546, 461, 700, 677) | 13,005 | 0.0 | 42.3 | 생성 PNG |
| 2 | legwear | (411, 619, 672, 864) | 32,169 | 0.0 | 22.4 | 생성 PNG |
| 3 | bottomwear | (460, 592, 648, 670) | 11,099 | 0.0 | 40.5 | 생성 PNG |
| 4 | topwear | (470, 447, 621, 639) | 17,907 | 0.0 | 19.3 | 생성 PNG |
| 5 | ears-r | (412, 357, 456, 419) | 1,834 | 0.0 | 77.8 | 생성 PNG |
| 6 | ears-l | (590, 363, 629, 420) | 1,463 | 0.0 | 100.6 | 생성 PNG |
| 7 | face | (449, 255, 635, 453) | 30,984 | 0.0 | 71.7 | 생성 PNG |
| 8 | handwear-r | (374, 461, 506, 675) | 12,882 | 0.0 | 11.5 | 생성 PNG |
| 9 | mouth | (533, 428, 563, 454) | 598 | 26.7 | 0.0 | 원본 픽셀 |
| 10 | eyebrow-r | (479, 321, 539, 334) | 248 | 0.0 | 93.9 | 생성 PNG |
| 11 | eyebrow-l | (591, 328, 634, 339) | 187 | 0.0 | 96.8 | 생성 PNG |
| 12 | eyewhite-r | (466, 360, 530, 415) | 2,855 | 0.0 | 129.3 | 생성 PNG |
| 13 | eyewhite-l | (586, 366, 628, 419) | 1,683 | 0.0 | 129.0 | 생성 PNG |
| 14 | irides-l | (588, 366, 620, 419) | 1,306 | 0.0 | 26.4 | 생성 PNG |
| 15 | eyelash-l | (585, 356, 637, 404) | 866 | 0.0 | 50.3 | 생성 PNG |
| 16 | irides-r | (480, 360, 524, 415) | 2,077 | 0.0 | 21.0 | 생성 PNG |
| 17 | eyelash-r | (461, 350, 538, 402) | 1,407 | 0.0 | 39.4 | 생성 PNG |
| 18 | front hair | (404, 179, 704, 471) | 47,496 | 0.0 | 11.4 | 생성 PNG |

- PSD 전체 합성 vs src_img.png PSNR(흰 배경): 21.9 dB

## step26_coverage.png (2-6 품질: 어디가 빠졌나)
- 원본에만 있음(빠짐, 빨강): 6,983px / PSD에만 있음(파랑): 3px / 둘 다: 295,516px
- 둘 다 있는 곳 중 색 차이 > 40: 23,424px
- 빠진 덩어리 큰 순서 (x, y, w, h, 픽셀): (579, 150, 83, 52, 2336), (391, 146, 67, 52, 2216), (403, 249, 33, 66, 1029), (476, 450, 25, 12, 163), (478, 602, 8, 14, 54)
- 초록 상자 = 2-2 머리 자르기 상자 (상자 밖의 머리 장식은 생성되지 않음)

## step27_hidden_parts.png (8⑤ 가려진 부분 확인)
- 각 레이어를 혼자 띄움, 초록 = 그 위 레이어들에 가려지는 부분(앞 레이어를 움직이면 드러날 곳)
| 레이어(앞→뒤) | 픽셀 | 가려지는 픽셀 | 비율 |
|---|---|---|---|
| front hair | 47,496 | 0 | 0% |
| eyelash-r | 1,407 | 122 | 9% |
| irides-r | 2,077 | 315 | 15% |
| eyelash-l | 866 | 61 | 7% |
| irides-l | 1,306 | 194 | 15% |
| eyewhite-l | 1,683 | 1,482 | 88% |
| eyewhite-r | 2,855 | 2,405 | 84% |
| eyebrow-l | 187 | 80 | 43% |
| eyebrow-r | 248 | 95 | 38% |
| mouth | 598 | 0 | 0% |
| handwear-r | 12,882 | 0 | 0% |
| face | 30,984 | 21,083 | 68% |
| ears-l | 1,463 | 1,421 | 97% |
| ears-r | 1,834 | 1,834 | 100% |
| topwear | 17,907 | 1,518 | 8% |
| bottomwear | 11,099 | 3,746 | 34% |
| legwear | 32,169 | 5,635 | 18% |
| handwear-l | 13,005 | 5,707 | 44% |
| back hair | 226,433 | 60,907 | 27% |

## stages_strip.png
- src_img.png · head.png · src_head.png · face_depth.png · back hair_depth.png · reconstruction.png
