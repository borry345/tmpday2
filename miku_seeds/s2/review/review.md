# miku_chibi_sprite See-through 단계별 검토

- 만든 도구: `tools/review_seethrough.py --run seethrough_test/miku_grow_seed2` (모델 실행 없음, 기존 파일만 읽음)
- 원본: `miku_chibi_sprite.png` (1312x1199)
- 중간 파일: `C:\Users\SSAFY\Desktop\borry\seethrough_work_2026-11-23\i2l\seethrough_test\miku_grow_seed2\miku_chibi_sprite`

## step20_preprocess.png (2-0 전처리)
- 긴 변 1312에 맞춰 정사각형 패딩(좌우 0px, 위아래 56px) → 1024로 축소 (0.78배)

## step21_body_tags.png (2-1 LayerDiff 몸 단계)
| 태그 | 픽셀 |
|---|---|
| front hair | 47,282 |
| back hair | 187,514 |
| head | 39,294 |
| neck | 3,494 |
| neckwear | 0 |
| topwear | 18,100 |
| handwear | 26,713 |
| bottomwear | 12,006 |
| legwear | 32,574 |
| footwear | 0 |
| tail | 0 |
| wings | 0 |
| objects | 0 |

- 빈 레이어 5개: neckwear, footwear, tail, wings, objects

## step22_head_crop.png (2-2 머리 자르기)
- 초록: head.png 범위 / 빨강: 실제 자르기 상자(여백 1/5, 코드 계산 재현) / 보라: headwear.png
- head 범위(1024): (430, 236, 645, 459), 자르기 상자(1024): [333, 135, 686, 501]
- headwear가 상자 경계에 닿은 쪽(잘림 의심): right

- head_grow 2회 (주황=이전 회차 상자): 0:[386, 191, 686, 502] 닿음=['left', 'top'] 확장=['left', 'top'] → 1:[333, 135, 686, 501] 닿음=[] 확장=[]

## step23_head_tags.png (2-3 LayerDiff 머리 단계)
| 태그 | 픽셀 |
|---|---|
| headwear | 14,539 |
| face | 42,667 |
| irides | 3,427 |
| eyebrow | 428 |
| eyewhite | 4,583 |
| eyelash | 2,382 |
| eyewear | 0 |
| ears | 0 |
| earwear | 0 |
| nose | 0 |
| mouth | 81 |

- 빈 레이어 4개: eyewear, ears, earwear, nose

## step24_depth.png (2-4 Marigold 깊이)
- PSD 레이어를 깊이 중앙값(psd.json) 순서로 배치, 레이어 안은 <태그>_depth.png를 색으로 표시
| 순서 | 레이어 | 깊이 중앙값 |
|---|---|---|
| 1 | front hair | 0.047 |
| 2 | eyelash-r | 0.114 |
| 3 | irides-r | 0.169 |
| 4 | eyelash-l | 0.227 |
| 5 | irides-l | 0.251 |
| 6 | eyewhite-r | 0.275 |
| 7 | eyewhite-l | 0.275 |
| 8 | eyebrow-l | 0.280 |
| 9 | eyebrow-r | 0.314 |
| 10 | mouth | 0.423 |
| 11 | face | 0.424 |
| 12 | handwear-r | 0.478 |
| 13 | neck | 0.482 |
| 14 | topwear | 0.561 |
| 15 | bottomwear | 0.608 |
| 16 | legwear | 0.710 |
| 17 | handwear-l | 0.725 |
| 18 | headwear | 0.749 |
| 19 | back hair | 0.906 |

- reconstruction.png vs src_img.png PSNR(흰 배경): 23.2 dB

## step25_psd_stack.png (2-5 PSD 조립)
- PSD 레이어 19개를 아래(먼 쪽)부터 하나씩 쌓아 가는 모습, 빨간 상자 = 방금 추가한 레이어 범위
- 생성PNG차이/원본차이: 레이어 픽셀 RGB 평균 차이 (0이면 그 파일 그대로)
| PSD 순서(아래→위) | 레이어 | bbox | 픽셀 | 생성PNG 차이 | 원본 차이 | 픽셀 출처 |
|---|---|---|---|---|---|---|
| 0 | back hair | (157, 161, 868, 815) | 187,514 | 0.0 | 20.8 | 생성 PNG |
| 1 | headwear | (370, 144, 685, 306) | 14,539 | 0.0 | 34.7 | 생성 PNG |
| 2 | handwear-l | (544, 460, 700, 678) | 13,812 | 0.0 | 48.5 | 생성 PNG |
| 3 | legwear | (412, 616, 672, 864) | 32,574 | 0.0 | 24.0 | 생성 PNG |
| 4 | bottomwear | (454, 587, 648, 670) | 12,006 | 0.0 | 43.3 | 생성 PNG |
| 5 | topwear | (469, 445, 621, 639) | 18,100 | 0.0 | 19.5 | 생성 PNG |
| 6 | neck | (503, 386, 558, 454) | 3,494 | 0.0 | 94.5 | 생성 PNG |
| 7 | handwear-r | (374, 461, 509, 674) | 12,901 | 0.0 | 11.7 | 생성 PNG |
| 8 | face | (427, 224, 648, 458) | 42,667 | 0.0 | 69.8 | 생성 PNG |
| 9 | mouth | (545, 433, 558, 441) | 81 | 98.7 | 0.0 | 원본 픽셀 |
| 10 | eyebrow-r | (483, 320, 539, 333) | 232 | 0.0 | 101.0 | 생성 PNG |
| 11 | eyebrow-l | (591, 327, 638, 338) | 196 | 0.0 | 115.1 | 생성 PNG |
| 12 | eyewhite-r | (467, 358, 530, 414) | 2,846 | 0.0 | 132.5 | 생성 PNG |
| 13 | eyewhite-l | (586, 363, 628, 419) | 1,737 | 0.0 | 131.6 | 생성 PNG |
| 14 | irides-l | (588, 365, 620, 419) | 1,305 | 0.0 | 32.2 | 생성 PNG |
| 15 | eyelash-l | (585, 355, 637, 403) | 909 | 0.0 | 65.5 | 생성 PNG |
| 16 | irides-r | (480, 358, 524, 414) | 2,122 | 0.0 | 26.5 | 생성 PNG |
| 17 | eyelash-r | (456, 349, 538, 401) | 1,473 | 0.0 | 49.3 | 생성 PNG |
| 18 | front hair | (404, 181, 704, 471) | 47,282 | 0.0 | 11.7 | 생성 PNG |

- PSD 전체 합성 vs src_img.png PSNR(흰 배경): 25.3 dB

## step26_coverage.png (2-6 품질: 어디가 빠졌나)
- 원본에만 있음(빠짐, 빨강): 2,987px / PSD에만 있음(파랑): 92px / 둘 다: 299,512px
- 둘 다 있는 곳 중 색 차이 > 40: 10,590px
- 빠진 덩어리 큰 순서 (x, y, w, h, 픽셀): (555, 378, 82, 91, 1240), (473, 440, 30, 22, 186), (375, 386, 26, 29, 72), (416, 266, 11, 28, 71), (612, 536, 26, 32, 43)
- 초록 상자 = 2-2 머리 자르기 상자 (상자 밖의 머리 장식은 생성되지 않음)

## step27_hidden_parts.png (8⑤ 가려진 부분 확인)
- 각 레이어를 혼자 띄움, 초록 = 그 위 레이어들에 가려지는 부분(앞 레이어를 움직이면 드러날 곳)
| 레이어(앞→뒤) | 픽셀 | 가려지는 픽셀 | 비율 |
|---|---|---|---|
| front hair | 47,282 | 0 | 0% |
| eyelash-r | 1,473 | 184 | 12% |
| irides-r | 2,122 | 363 | 17% |
| eyelash-l | 909 | 74 | 8% |
| irides-l | 1,305 | 193 | 15% |
| eyewhite-l | 1,737 | 1,529 | 88% |
| eyewhite-r | 2,846 | 2,398 | 84% |
| eyebrow-l | 196 | 91 | 46% |
| eyebrow-r | 232 | 85 | 37% |
| mouth | 81 | 0 | 0% |
| face | 42,667 | 31,320 | 73% |
| handwear-r | 12,901 | 0 | 0% |
| neck | 3,494 | 3,487 | 100% |
| topwear | 18,100 | 1,859 | 10% |
| bottomwear | 12,006 | 4,601 | 38% |
| legwear | 32,574 | 6,057 | 19% |
| handwear-l | 13,812 | 6,602 | 48% |
| headwear | 14,539 | 1,799 | 12% |
| back hair | 187,514 | 31,219 | 17% |

## stages_strip.png
- src_img.png · head.png · src_head.png · face_depth.png · back hair_depth.png · reconstruction.png
