# miku_chibi_sprite See-through 단계별 검토

- 만든 도구: `tools/review_seethrough.py --run seethrough_test/miku_grow_seed0` (모델 실행 없음, 기존 파일만 읽음)
- 원본: `miku_chibi_sprite.png` (1312x1199)
- 중간 파일: `C:\Users\SSAFY\Desktop\borry\seethrough_work_2026-11-23\i2l\seethrough_test\miku_grow_seed0\miku_chibi_sprite`

## step20_preprocess.png (2-0 전처리)
- 긴 변 1312에 맞춰 정사각형 패딩(좌우 0px, 위아래 56px) → 1024로 축소 (0.78배)

## step21_body_tags.png (2-1 LayerDiff 몸 단계)
| 태그 | 픽셀 |
|---|---|
| front hair | 47,468 |
| back hair | 168,800 |
| head | 43,298 |
| neck | 0 |
| neckwear | 0 |
| topwear | 18,124 |
| handwear | 25,650 |
| bottomwear | 12,334 |
| legwear | 32,486 |
| footwear | 0 |
| tail | 0 |
| wings | 0 |
| objects | 0 |

- 빈 레이어 6개: neck, neckwear, footwear, tail, wings, objects

## step22_head_crop.png (2-2 머리 자르기)
- 초록: head.png 범위 / 빨강: 실제 자르기 상자(여백 1/5, 코드 계산 재현) / 보라: headwear.png
- head 범위(1024): (424, 220, 646, 459), 자르기 상자(1024): [324, 112, 688, 505]
- headwear가 상자 경계에 닿은 쪽(잘림 의심): 없음

- head_grow 2회 (주황=이전 회차 상자): 0:[380, 171, 689, 505] 닿음=['left', 'top'] 확장=['left', 'top'] → 1:[324, 112, 688, 505] 닿음=[] 확장=[]

## step23_head_tags.png (2-3 LayerDiff 머리 단계)
| 태그 | 픽셀 |
|---|---|
| headwear | 26,080 |
| face | 0 |
| irides | 3,426 |
| eyebrow | 529 |
| eyewhite | 4,639 |
| eyelash | 2,454 |
| eyewear | 0 |
| ears | 0 |
| earwear | 0 |
| nose | 0 |
| mouth | 118 |

- 빈 레이어 5개: face, eyewear, ears, earwear, nose

## step24_depth.png (2-4 Marigold 깊이)
- PSD 레이어를 깊이 중앙값(psd.json) 순서로 배치, 레이어 안은 <태그>_depth.png를 색으로 표시
| 순서 | 레이어 | 깊이 중앙값 |
|---|---|---|
| 1 | front hair | 0.035 |
| 2 | eyelash-r | 0.098 |
| 3 | irides-r | 0.149 |
| 4 | eyelash-l | 0.220 |
| 5 | eyewhite-r | 0.247 |
| 6 | eyewhite-l | 0.247 |
| 7 | irides-l | 0.271 |
| 8 | eyebrow-r | 0.318 |
| 9 | eyebrow-l | 0.322 |
| 10 | handwear-r | 0.408 |
| 11 | mouth | 0.576 |
| 12 | topwear | 0.576 |
| 13 | bottomwear | 0.620 |
| 14 | legwear | 0.710 |
| 15 | handwear-l | 0.733 |
| 16 | headwear | 0.820 |
| 17 | back hair | 0.898 |

- reconstruction.png vs src_img.png PSNR(흰 배경): 22.3 dB

## step25_psd_stack.png (2-5 PSD 조립)
- PSD 레이어 17개를 아래(먼 쪽)부터 하나씩 쌓아 가는 모습, 빨간 상자 = 방금 추가한 레이어 범위
- 생성PNG차이/원본차이: 레이어 픽셀 RGB 평균 차이 (0이면 그 파일 그대로)
| PSD 순서(아래→위) | 레이어 | bbox | 픽셀 | 생성PNG 차이 | 원본 차이 | 픽셀 출처 |
|---|---|---|---|---|---|---|
| 0 | back hair | (157, 180, 868, 815) | 168,800 | 0.0 | 17.6 | 생성 PNG |
| 1 | headwear | (358, 145, 685, 429) | 26,080 | 0.0 | 62.4 | 생성 PNG |
| 2 | handwear-l | (547, 462, 700, 679) | 12,685 | 0.0 | 42.6 | 생성 PNG |
| 3 | legwear | (411, 617, 672, 864) | 32,486 | 0.0 | 24.0 | 생성 PNG |
| 4 | bottomwear | (455, 584, 649, 670) | 12,334 | 0.0 | 47.9 | 생성 PNG |
| 5 | mouth | (545, 433, 558, 444) | 118 | 64.6 | 0.0 | 원본 픽셀 |
| 6 | topwear | (471, 445, 620, 639) | 18,124 | 0.0 | 19.1 | 생성 PNG |
| 7 | handwear-r | (374, 461, 508, 675) | 12,965 | 0.0 | 11.5 | 생성 PNG |
| 8 | eyebrow-l | (590, 328, 641, 339) | 224 | 0.0 | 112.1 | 생성 PNG |
| 9 | eyebrow-r | (468, 320, 540, 334) | 305 | 0.0 | 99.0 | 생성 PNG |
| 10 | irides-l | (588, 366, 620, 419) | 1,299 | 0.0 | 29.8 | 생성 PNG |
| 11 | eyewhite-r | (467, 358, 530, 414) | 2,895 | 0.0 | 133.5 | 생성 PNG |
| 12 | eyewhite-l | (586, 365, 629, 420) | 1,744 | 0.0 | 129.4 | 생성 PNG |
| 13 | eyelash-l | (585, 356, 635, 405) | 895 | 0.0 | 62.5 | 생성 PNG |
| 14 | irides-r | (480, 359, 524, 415) | 2,127 | 0.0 | 24.5 | 생성 PNG |
| 15 | eyelash-r | (461, 350, 538, 402) | 1,445 | 0.0 | 43.8 | 생성 PNG |
| 16 | front hair | (404, 178, 704, 471) | 47,468 | 0.0 | 10.8 | 생성 PNG |

- PSD 전체 합성 vs src_img.png PSNR(흰 배경): 22.9 dB

## step26_coverage.png (2-6 품질: 어디가 빠졌나)
- 원본에만 있음(빠짐, 빨강): 19,381px / PSD에만 있음(파랑): 79px / 둘 다: 283,118px
- 둘 다 있는 곳 중 색 차이 > 40: 9,637px
- 빠진 덩어리 큰 순서 (x, y, w, h, 픽셀): (459, 287, 178, 184, 12455), (447, 162, 142, 71, 3838), (371, 265, 57, 66, 1028), (593, 295, 22, 40, 422), (606, 176, 21, 29, 298)
- 초록 상자 = 2-2 머리 자르기 상자 (상자 밖의 머리 장식은 생성되지 않음)

## step27_hidden_parts.png (8⑤ 가려진 부분 확인)
- 각 레이어를 혼자 띄움, 초록 = 그 위 레이어들에 가려지는 부분(앞 레이어를 움직이면 드러날 곳)
| 레이어(앞→뒤) | 픽셀 | 가려지는 픽셀 | 비율 |
|---|---|---|---|
| front hair | 47,468 | 0 | 0% |
| eyelash-r | 1,445 | 143 | 10% |
| irides-r | 2,127 | 368 | 17% |
| eyelash-l | 895 | 47 | 5% |
| eyewhite-l | 1,744 | 412 | 24% |
| eyewhite-r | 2,895 | 2,460 | 85% |
| irides-l | 1,299 | 1,299 | 100% |
| eyebrow-r | 305 | 150 | 49% |
| eyebrow-l | 224 | 111 | 50% |
| handwear-r | 12,965 | 0 | 0% |
| topwear | 18,124 | 1,761 | 10% |
| mouth | 118 | 0 | 0% |
| bottomwear | 12,334 | 4,926 | 40% |
| legwear | 32,486 | 5,939 | 18% |
| handwear-l | 12,685 | 5,333 | 42% |
| headwear | 26,080 | 8,265 | 32% |
| back hair | 168,800 | 21,911 | 13% |

## stages_strip.png
- src_img.png · head.png · src_head.png · face_depth.png · back hair_depth.png · reconstruction.png
