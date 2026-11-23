# miku_chibi_sprite See-through 단계별 검토

- 만든 도구: `tools/review_seethrough.py --run seethrough_test/miku_chibi_sprite` (모델 실행 없음, 기존 파일만 읽음)
- 원본: `C:\Users\SSAFY\Desktop\borry\seethrough_work_2026-11-23\i2l\miku_chibi_sprite.png` (1312x1199)
- 중간 파일: `C:\Users\SSAFY\Desktop\borry\seethrough_work_2026-11-23\i2l\seethrough_test\miku_chibi_sprite\miku_chibi_sprite`

## step20_preprocess.png (2-0 전처리)
- 긴 변 1312에 맞춰 정사각형 패딩(좌우 0px, 위아래 56px) → 1024로 축소 (0.78배)

## step21_body_tags.png (2-1 LayerDiff 몸 단계)
| 태그 | 픽셀 |
|---|---|
| front hair | 47,303 |
| back hair | 235,566 |
| head | 40,918 |
| neck | 0 |
| neckwear | 0 |
| topwear | 17,897 |
| handwear | 26,620 |
| bottomwear | 11,693 |
| legwear | 32,235 |
| footwear | 0 |
| tail | 0 |
| wings | 0 |
| objects | 0 |

- 빈 레이어 6개: neck, neckwear, footwear, tail, wings, objects

## step22_head_crop.png (2-2 머리 자르기)
- 초록: head.png 범위 / 빨강: 실제 자르기 상자(여백 1/5, 코드 계산 재현) / 보라: headwear.png
- head 범위(1024): (434, 227, 649, 459), 자르기 상자(1024): [391, 180, 692, 504]
- headwear가 상자 경계에 닿은 쪽(잘림 의심): left, top

## step23_head_tags.png (2-3 LayerDiff 머리 단계)
| 태그 | 픽셀 |
|---|---|
| headwear | 13,638 |
| face | 33,232 |
| irides | 3,453 |
| eyebrow | 506 |
| eyewhite | 4,424 |
| eyelash | 2,355 |
| eyewear | 0 |
| ears | 0 |
| earwear | 0 |
| nose | 0 |
| mouth | 118 |

- 빈 레이어 4개: eyewear, ears, earwear, nose

## step24_depth.png (2-4 Marigold 깊이)
- PSD 레이어를 깊이 중앙값(psd.json) 순서로 배치, 레이어 안은 <태그>_depth.png를 색으로 표시
| 순서 | 레이어 | 깊이 중앙값 |
|---|---|---|
| 1 | front hair | 0.043 |
| 2 | eyelash | 0.180 |
| 3 | irides | 0.192 |
| 4 | eyewhite | 0.271 |
| 5 | eyebrow | 0.349 |
| 6 | mouth | 0.446 |
| 7 | face | 0.447 |
| 8 | topwear | 0.553 |
| 9 | bottomwear | 0.600 |
| 10 | headwear | 0.616 |
| 11 | legwear | 0.675 |
| 12 | handwear | 0.729 |
| 13 | back hair | 0.898 |

- reconstruction.png vs src_img.png PSNR(흰 배경): 22.1 dB

## step25_psd_stack.png (2-5 PSD 조립)
- PSD 레이어 13개를 아래(먼 쪽)부터 하나씩 쌓아 가는 모습, 빨간 상자 = 방금 추가한 레이어 범위
- 생성PNG차이/원본차이: 레이어 픽셀 RGB 평균 차이 (0이면 그 파일 그대로)
| PSD 순서(아래→위) | 레이어 | bbox | 픽셀 | 생성PNG 차이 | 원본 차이 | 픽셀 출처 |
|---|---|---|---|---|---|---|
| 0 | back hair | (157, 161, 868, 815) | 235,566 | 0.0 | 28.4 | 생성 PNG |
| 1 | handwear | (374, 461, 700, 678) | 26,620 | 0.0 | 30.3 | 생성 PNG |
| 2 | legwear | (411, 616, 672, 864) | 32,235 | 0.0 | 24.6 | 생성 PNG |
| 3 | headwear | (391, 180, 685, 419) | 13,638 | 0.0 | 44.7 | 생성 PNG |
| 4 | bottomwear | (460, 587, 648, 670) | 11,693 | 0.0 | 44.4 | 생성 PNG |
| 5 | topwear | (470, 447, 621, 639) | 17,897 | 0.0 | 18.8 | 생성 PNG |
| 6 | face | (447, 246, 636, 458) | 33,232 | 0.0 | 66.1 | 생성 PNG |
| 7 | mouth | (546, 432, 560, 442) | 118 | 62.0 | 0.0 | 원본 픽셀 |
| 8 | eyebrow | (471, 319, 637, 339) | 506 | 0.0 | 105.4 | 생성 PNG |
| 9 | eyewhite | (467, 361, 628, 420) | 4,424 | 0.0 | 130.1 | 생성 PNG |
| 10 | irides | (481, 358, 620, 419) | 3,453 | 0.0 | 24.0 | 생성 PNG |
| 11 | eyelash | (460, 350, 637, 404) | 2,355 | 0.0 | 50.1 | 생성 PNG |
| 12 | front hair | (404, 180, 703, 470) | 47,303 | 0.0 | 11.7 | 생성 PNG |

- PSD 전체 합성 vs src_img.png PSNR(흰 배경): 23.3 dB

## step26_coverage.png (2-6 품질: 어디가 빠졌나)
- 원본에만 있음(빠짐, 빨강): 5,692px / PSD에만 있음(파랑): 1px / 둘 다: 296,807px
- 둘 다 있는 곳 중 색 차이 > 40: 9,435px
- 빠진 덩어리 큰 순서 (x, y, w, h, 픽셀): (391, 146, 67, 38, 1812), (575, 150, 83, 45, 1725), (365, 337, 65, 100, 607), (479, 449, 22, 13, 158), (488, 540, 13, 31, 41)
- 초록 상자 = 2-2 머리 자르기 상자 (상자 밖의 머리 장식은 생성되지 않음)

## step27_hidden_parts.png (8⑤ 가려진 부분 확인)
- 각 레이어를 혼자 띄움, 초록 = 그 위 레이어들에 가려지는 부분(앞 레이어를 움직이면 드러날 곳)
| 레이어(앞→뒤) | 픽셀 | 가려지는 픽셀 | 비율 |
|---|---|---|---|
| front hair | 47,303 | 0 | 0% |
| eyelash | 2,355 | 221 | 9% |
| irides | 3,453 | 598 | 17% |
| eyewhite | 4,424 | 3,751 | 85% |
| eyebrow | 506 | 247 | 49% |
| mouth | 118 | 0 | 0% |
| face | 33,232 | 21,833 | 66% |
| topwear | 17,897 | 227 | 1% |
| bottomwear | 11,693 | 4,028 | 34% |
| headwear | 13,638 | 4,581 | 34% |
| legwear | 32,235 | 5,723 | 18% |
| handwear | 26,620 | 8,287 | 31% |
| back hair | 235,566 | 78,587 | 33% |

## stages_strip.png
- src_img.png · head.png · src_head.png · face_depth.png · back hair_depth.png · reconstruction.png
