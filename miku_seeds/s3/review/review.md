# miku_chibi_sprite See-through 단계별 검토

- 만든 도구: `tools/review_seethrough.py --run seethrough_test/miku_grow_seed3` (모델 실행 없음, 기존 파일만 읽음)
- 원본: `miku_chibi_sprite.png` (1312x1199)
- 중간 파일: `C:\Users\SSAFY\Desktop\borry\seethrough_work_2026-11-23\i2l\seethrough_test\miku_grow_seed3\miku_chibi_sprite`

## step20_preprocess.png (2-0 전처리)
- 긴 변 1312에 맞춰 정사각형 패딩(좌우 0px, 위아래 56px) → 1024로 축소 (0.78배)

## step21_body_tags.png (2-1 LayerDiff 몸 단계)
| 태그 | 픽셀 |
|---|---|
| front hair | 47,245 |
| back hair | 180,277 |
| head | 42,989 |
| neck | 0 |
| neckwear | 0 |
| topwear | 17,963 |
| handwear | 26,195 |
| bottomwear | 12,549 |
| legwear | 31,857 |
| footwear | 0 |
| tail | 0 |
| wings | 0 |
| objects | 0 |

- 빈 레이어 6개: neck, neckwear, footwear, tail, wings, objects

## step22_head_crop.png (2-2 머리 자르기)
- 초록: head.png 범위 / 빨강: 실제 자르기 상자(여백 1/5, 코드 계산 재현) / 보라: headwear.png
- head 범위(1024): (426, 222, 648, 459), 자르기 상자(1024): [326, 116, 691, 504]
- headwear가 상자 경계에 닿은 쪽(잘림 의심): 없음

- head_grow 2회 (주황=이전 회차 상자): 0:[381, 174, 690, 504] 닿음=['left', 'top'] 확장=['left', 'top'] → 1:[326, 116, 691, 504] 닿음=[] 확장=[]

## step23_head_tags.png (2-3 LayerDiff 머리 단계)
| 태그 | 픽셀 |
|---|---|
| headwear | 0 |
| face | 35,588 |
| irides | 3,521 |
| eyebrow | 507 |
| eyewhite | 4,508 |
| eyelash | 2,362 |
| eyewear | 0 |
| ears | 1,403 |
| earwear | 0 |
| nose | 0 |
| mouth | 121 |

- 빈 레이어 4개: headwear, eyewear, earwear, nose

## step24_depth.png (2-4 Marigold 깊이)
- PSD 레이어를 깊이 중앙값(psd.json) 순서로 배치, 레이어 안은 <태그>_depth.png를 색으로 표시
| 순서 | 레이어 | 깊이 중앙값 |
|---|---|---|
| 1 | front hair | 0.055 |
| 2 | eyelash-r | 0.118 |
| 3 | irides-r | 0.169 |
| 4 | eyelash-l | 0.227 |
| 5 | irides-l | 0.255 |
| 6 | eyewhite-r | 0.267 |
| 7 | eyewhite-l | 0.267 |
| 8 | eyebrow-l | 0.324 |
| 9 | eyebrow-r | 0.341 |
| 10 | handwear-r | 0.361 |
| 11 | mouth | 0.423 |
| 12 | face | 0.424 |
| 13 | ears | 0.425 |
| 14 | topwear | 0.565 |
| 15 | bottomwear | 0.616 |
| 16 | legwear | 0.671 |
| 17 | handwear-l | 0.706 |
| 18 | back hair | 0.902 |

- reconstruction.png vs src_img.png PSNR(흰 배경): 19.7 dB

## step25_psd_stack.png (2-5 PSD 조립)
- PSD 레이어 18개를 아래(먼 쪽)부터 하나씩 쌓아 가는 모습, 빨간 상자 = 방금 추가한 레이어 범위
- 생성PNG차이/원본차이: 레이어 픽셀 RGB 평균 차이 (0이면 그 파일 그대로)
| PSD 순서(아래→위) | 레이어 | bbox | 픽셀 | 생성PNG 차이 | 원본 차이 | 픽셀 출처 |
|---|---|---|---|---|---|---|
| 0 | back hair | (157, 161, 868, 815) | 180,277 | 0.0 | 18.8 | 생성 PNG |
| 1 | handwear-l | (543, 461, 700, 678) | 13,297 | 0.0 | 45.8 | 생성 PNG |
| 2 | legwear | (411, 622, 672, 864) | 31,857 | 0.0 | 20.4 | 생성 PNG |
| 3 | bottomwear | (450, 585, 649, 670) | 12,549 | 0.0 | 47.4 | 생성 PNG |
| 4 | topwear | (470, 446, 621, 639) | 17,963 | 0.0 | 19.2 | 생성 PNG |
| 5 | ears | (604, 359, 643, 418) | 1,403 | 0.0 | 123.3 | 생성 PNG |
| 6 | face | (435, 248, 640, 458) | 35,588 | 0.0 | 67.0 | 생성 PNG |
| 7 | mouth | (545, 432, 560, 443) | 121 | 58.9 | 0.0 | 원본 픽셀 |
| 8 | handwear-r | (373, 462, 507, 674) | 12,898 | 0.0 | 11.7 | 생성 PNG |
| 9 | eyebrow-r | (470, 320, 541, 334) | 296 | 0.0 | 97.8 | 생성 PNG |
| 10 | eyebrow-l | (590, 327, 639, 339) | 211 | 0.0 | 105.9 | 생성 PNG |
| 11 | eyewhite-r | (468, 359, 531, 415) | 2,811 | 0.0 | 131.7 | 생성 PNG |
| 12 | eyewhite-l | (586, 366, 628, 419) | 1,697 | 0.0 | 132.6 | 생성 PNG |
| 13 | irides-l | (588, 363, 621, 419) | 1,357 | 0.0 | 25.4 | 생성 PNG |
| 14 | eyelash-l | (585, 356, 637, 404) | 899 | 0.0 | 56.3 | 생성 PNG |
| 15 | irides-r | (480, 357, 525, 414) | 2,164 | 0.0 | 22.8 | 생성 PNG |
| 16 | eyelash-r | (461, 350, 539, 402) | 1,463 | 0.0 | 46.6 | 생성 PNG |
| 17 | front hair | (404, 181, 703, 471) | 47,245 | 0.0 | 11.4 | 생성 PNG |

- PSD 전체 합성 vs src_img.png PSNR(흰 배경): 20.6 dB

## step26_coverage.png (2-6 품질: 어디가 빠졌나)
- 원본에만 있음(빠짐, 빨강): 12,341px / PSD에만 있음(파랑): 2px / 둘 다: 290,158px
- 둘 다 있는 곳 중 색 차이 > 40: 10,153px
- 빠진 덩어리 큰 순서 (x, y, w, h, 픽셀): (367, 217, 96, 209, 6298), (580, 150, 82, 52, 2359), (391, 146, 67, 55, 2289), (435, 429, 68, 42, 347), (554, 444, 54, 17, 82)
- 초록 상자 = 2-2 머리 자르기 상자 (상자 밖의 머리 장식은 생성되지 않음)

## step27_hidden_parts.png (8⑤ 가려진 부분 확인)
- 각 레이어를 혼자 띄움, 초록 = 그 위 레이어들에 가려지는 부분(앞 레이어를 움직이면 드러날 곳)
| 레이어(앞→뒤) | 픽셀 | 가려지는 픽셀 | 비율 |
|---|---|---|---|
| front hair | 47,245 | 0 | 0% |
| eyelash-r | 1,463 | 141 | 10% |
| irides-r | 2,164 | 411 | 19% |
| eyelash-l | 899 | 63 | 7% |
| irides-l | 1,357 | 245 | 18% |
| eyewhite-l | 1,697 | 1,483 | 87% |
| eyewhite-r | 2,811 | 2,376 | 85% |
| eyebrow-l | 211 | 102 | 48% |
| eyebrow-r | 296 | 139 | 47% |
| handwear-r | 12,898 | 0 | 0% |
| mouth | 121 | 0 | 0% |
| face | 35,588 | 24,270 | 68% |
| ears | 1,403 | 1,193 | 85% |
| topwear | 17,963 | 1,774 | 10% |
| bottomwear | 12,549 | 5,119 | 41% |
| legwear | 31,857 | 5,281 | 17% |
| handwear-l | 13,297 | 6,078 | 46% |
| back hair | 180,277 | 20,709 | 11% |

## stages_strip.png
- src_img.png · head.png · src_head.png · face_depth.png · back hair_depth.png · reconstruction.png
