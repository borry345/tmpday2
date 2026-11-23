# miku_chibi_sprite See-through 단계별 검토

- 만든 도구: `tools/review_seethrough.py --run seethrough_test/miku_grow_seed4` (모델 실행 없음, 기존 파일만 읽음)
- 원본: `miku_chibi_sprite.png` (1312x1199)
- 중간 파일: `C:\Users\SSAFY\Desktop\borry\seethrough_work_2026-11-23\i2l\seethrough_test\miku_grow_seed4\miku_chibi_sprite`

## step20_preprocess.png (2-0 전처리)
- 긴 변 1312에 맞춰 정사각형 패딩(좌우 0px, 위아래 56px) → 1024로 축소 (0.78배)

## step21_body_tags.png (2-1 LayerDiff 몸 단계)
| 태그 | 픽셀 |
|---|---|
| front hair | 47,268 |
| back hair | 237,137 |
| head | 38,669 |
| neck | 0 |
| neckwear | 0 |
| topwear | 17,873 |
| handwear | 25,988 |
| bottomwear | 13,184 |
| legwear | 33,213 |
| footwear | 0 |
| tail | 0 |
| wings | 0 |
| objects | 0 |

- 빈 레이어 6개: neck, neckwear, footwear, tail, wings, objects

## step22_head_crop.png (2-2 머리 자르기)
- 초록: head.png 범위 / 빨강: 실제 자르기 상자(여백 1/5, 코드 계산 재현) / 보라: headwear.png
- head 범위(1024): (438, 233, 645, 459), 자르기 상자(1024): [344, 131, 736, 502]
- headwear가 상자 경계에 닿은 쪽(잘림 의심): 없음

- head_grow 3회 (주황=이전 회차 상자): 0:[396, 188, 686, 502] 닿음=['left', 'top'] 확장=['left', 'top'] → 1:[344, 131, 685, 501] 닿음=['right'] 확장=['right'] → 2:[344, 131, 736, 502] 닿음=[] 확장=[]

## step23_head_tags.png (2-3 LayerDiff 머리 단계)
| 태그 | 픽셀 |
|---|---|
| headwear | 22,581 |
| face | 36,477 |
| irides | 3,511 |
| eyebrow | 433 |
| eyewhite | 4,463 |
| eyelash | 2,391 |
| eyewear | 0 |
| ears | 0 |
| earwear | 0 |
| nose | 0 |
| mouth | 159 |

- 빈 레이어 4개: eyewear, ears, earwear, nose

## step24_depth.png (2-4 Marigold 깊이)
- PSD 레이어를 깊이 중앙값(psd.json) 순서로 배치, 레이어 안은 <태그>_depth.png를 색으로 표시
| 순서 | 레이어 | 깊이 중앙값 |
|---|---|---|
| 1 | front hair | 0.039 |
| 2 | eyelash-r | 0.122 |
| 3 | irides-r | 0.173 |
| 4 | eyelash-l | 0.212 |
| 5 | eyebrow-l | 0.259 |
| 6 | irides-l | 0.275 |
| 7 | eyewhite-r | 0.278 |
| 8 | eyewhite-l | 0.278 |
| 9 | eyebrow-r | 0.341 |
| 10 | handwear-r | 0.388 |
| 11 | mouth | 0.430 |
| 12 | face | 0.431 |
| 13 | topwear | 0.561 |
| 14 | bottomwear | 0.624 |
| 15 | headwear | 0.667 |
| 16 | legwear | 0.698 |
| 17 | handwear-l | 0.718 |
| 18 | back hair | 0.902 |

- reconstruction.png vs src_img.png PSNR(흰 배경): 24.7 dB

## step25_psd_stack.png (2-5 PSD 조립)
- PSD 레이어 18개를 아래(먼 쪽)부터 하나씩 쌓아 가는 모습, 빨간 상자 = 방금 추가한 레이어 범위
- 생성PNG차이/원본차이: 레이어 픽셀 RGB 평균 차이 (0이면 그 파일 그대로)
| PSD 순서(아래→위) | 레이어 | bbox | 픽셀 | 생성PNG 차이 | 원본 차이 | 픽셀 출처 |
|---|---|---|---|---|---|---|
| 0 | back hair | (157, 161, 868, 815) | 237,137 | 0.0 | 29.1 | 생성 PNG |
| 1 | handwear-l | (549, 463, 700, 677) | 13,107 | 0.0 | 44.7 | 생성 PNG |
| 2 | legwear | (411, 610, 672, 864) | 33,213 | 0.0 | 26.9 | 생성 PNG |
| 3 | headwear | (364, 145, 684, 424) | 22,581 | 0.0 | 51.0 | 생성 PNG |
| 4 | bottomwear | (447, 578, 649, 670) | 13,184 | 0.0 | 51.3 | 생성 PNG |
| 5 | topwear | (470, 445, 621, 639) | 17,873 | 0.0 | 19.0 | 생성 PNG |
| 6 | face | (441, 239, 642, 459) | 36,477 | 0.0 | 69.7 | 생성 PNG |
| 7 | mouth | (543, 432, 561, 444) | 159 | 47.6 | 0.0 | 원본 픽셀 |
| 8 | handwear-r | (373, 462, 507, 675) | 12,881 | 0.0 | 11.4 | 생성 PNG |
| 9 | eyebrow-r | (482, 320, 538, 334) | 250 | 0.0 | 92.3 | 생성 PNG |
| 10 | eyewhite-r | (467, 360, 529, 415) | 2,787 | 0.0 | 128.1 | 생성 PNG |
| 11 | eyewhite-l | (585, 365, 628, 419) | 1,676 | 0.0 | 127.3 | 생성 PNG |
| 12 | irides-l | (588, 365, 619, 420) | 1,320 | 0.0 | 33.8 | 생성 PNG |
| 13 | eyebrow-l | (590, 328, 631, 339) | 183 | 0.0 | 94.3 | 생성 PNG |
| 14 | eyelash-l | (584, 356, 636, 404) | 905 | 0.0 | 64.1 | 생성 PNG |
| 15 | irides-r | (479, 357, 523, 415) | 2,191 | 0.0 | 27.3 | 생성 PNG |
| 16 | eyelash-r | (456, 350, 537, 402) | 1,486 | 0.0 | 43.7 | 생성 PNG |
| 17 | front hair | (404, 181, 703, 470) | 47,268 | 0.0 | 10.9 | 생성 PNG |

- PSD 전체 합성 vs src_img.png PSNR(흰 배경): 26.7 dB

## step26_coverage.png (2-6 품질: 어디가 빠졌나)
- 원본에만 있음(빠짐, 빨강): 1,520px / PSD에만 있음(파랑): 101px / 둘 다: 300,979px
- 둘 다 있는 곳 중 색 차이 > 40: 9,020px
- 빠진 덩어리 큰 순서 (x, y, w, h, 픽셀): (480, 451, 19, 13, 121), (611, 176, 12, 19, 93), (639, 150, 23, 39, 67), (487, 539, 14, 34, 65), (554, 450, 38, 14, 55)
- 초록 상자 = 2-2 머리 자르기 상자 (상자 밖의 머리 장식은 생성되지 않음)

## step27_hidden_parts.png (8⑤ 가려진 부분 확인)
- 각 레이어를 혼자 띄움, 초록 = 그 위 레이어들에 가려지는 부분(앞 레이어를 움직이면 드러날 곳)
| 레이어(앞→뒤) | 픽셀 | 가려지는 픽셀 | 비율 |
|---|---|---|---|
| front hair | 47,268 | 0 | 0% |
| eyelash-r | 1,486 | 186 | 13% |
| irides-r | 2,191 | 427 | 19% |
| eyelash-l | 905 | 61 | 7% |
| eyebrow-l | 183 | 71 | 39% |
| irides-l | 1,320 | 204 | 15% |
| eyewhite-l | 1,676 | 1,488 | 89% |
| eyewhite-r | 2,787 | 2,335 | 84% |
| eyebrow-r | 250 | 100 | 40% |
| handwear-r | 12,881 | 0 | 0% |
| mouth | 159 | 0 | 0% |
| face | 36,477 | 25,132 | 69% |
| topwear | 17,873 | 1,696 | 9% |
| bottomwear | 13,184 | 5,730 | 43% |
| headwear | 22,581 | 6,420 | 28% |
| legwear | 33,213 | 6,654 | 20% |
| handwear-l | 13,107 | 5,913 | 45% |
| back hair | 237,137 | 82,976 | 35% |

## stages_strip.png
- src_img.png · head.png · src_head.png · face_depth.png · back hair_depth.png · reconstruction.png
