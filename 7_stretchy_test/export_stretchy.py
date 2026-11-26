"""PSDs for Stretchy Studio (https://github.com/MangoLion/stretchystudio) from miku_v1 / miku_v2.

Stretchy reads See-through tag names (src/io/armatureOrganizer.js matchTag/boneForTag) and each layer's bounds:
  - names: exact tag, or tag + '-'/' '/'_' + anything. The prefix test runs in KNOWN_TAGS order, so 'handwear-l_x'
    becomes 'handwear' (both arms); only the exact name 'handwear-l' goes to the left-arm bone. So every left-arm piece
    is named exactly 'handwear-l' (same for -r, legwear-l/-r). Eye parts use 'eyelash-l' style (in its tag list).
  - bounds: layers are cropped to their pixels (top/left kept), not full-canvas (the bounds guess the skeleton).
  - l/r: Stretchy is not consistent. Its splitLR.js calls the lower-x half '-l' (viewer side, like our files), but
    its skeleton (DWPose COCO keypoints and estimateSkeletonFromBounds) puts the 'leftArm'/'leftLeg' pivot on the
    character's own left (image right in a front view). Layers named for the viewer side were hung on the opposite
    shoulder/hip (crossed legs in the check). So these PSDs use the CHARACTER's side: our *_l (image left) -> '-r'.
Writes final/miku_v1/miku_v1_stretchy.psd, final/miku_v2/miku_v2_stretchy.psd (+ *_stretchy.json: our name -> its tag)
Variants (other hands, expressions) are not put in: Stretchy imports hidden layers too and would rig them all.
"""
import json
import os

import numpy as np
from PIL import Image
from psd_tools import PSDImage
from psd_tools.api.layers import PixelLayer

I2L = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(I2L)

KNOWN_TAGS = ['back hair', 'front hair', 'headwear', 'face', 'irides', 'irides-l', 'irides-r', 'eyebrow', 'eyebrow-l',
              'eyebrow-r', 'eyewhite', 'eyewhite-l', 'eyewhite-r', 'eyelash', 'eyelash-l', 'eyelash-r', 'eyewear', 'ears',
              'ears-l', 'ears-r', 'earwear', 'nose', 'mouth', 'neck', 'neckwear', 'topwear', 'handwear', 'handwear-l',
              'handwear-r', 'bottomwear', 'legwear', 'legwear-l', 'legwear-r', 'footwear', 'footwear-l', 'footwear-r',
              'tail', 'wings', 'objects']  # copied from armatureOrganizer.js


def match_tag(name):
    """same as Stretchy's matchTag"""
    low = name.lower().strip()
    if low in KNOWN_TAGS:
        return low
    for t in KNOWN_TAGS:
        if low.startswith(t + '-') or low.startswith(t + ' ') or low.startswith(t + '_'):
            return t
    return None


SUBJECT = {'l': 'r', 'r': 'l'}  # our l/r = viewer side; Stretchy's bones use the character's own side (see top)


def stretchy_name(n):
    for side in 'lr':
        sv = SUBJECT[side]
        arm = ('upperarm', 'forearm', 'hand', 'cloth_upper', 'cloth_lower')
        if any(n == f'{a}_{side}' or n.startswith(f'{a}_{side}_') for a in arm):
            return f'handwear-{sv}'
        if any(n == f'{a}_{side}' or n.startswith(f'{a}_{side}_') for a in ('thigh', 'shin')):
            return f'legwear-{sv}'
        for t in ('eyelash', 'irides', 'eyewhite', 'eyebrow'):
            if n == f'{t}_{side}':
                return f'{t}-{sv}'
    for base in ('handwear', 'legwear'):  # v1 names (viewer side) -> character side
        for side in 'lr':
            if n == f'{base}-{side}':
                return f'{base}-{SUBJECT[side]}'
    if n in ('front_hair', 'front hair'):
        return 'front hair'
    if n == 'back_center':
        return 'back hair'
    return n  # face, mouth, topwear, bottomwear, headwear_*, tail_* already match; handwear-l etc. too


def write(src_psd, out, order):
    """order: [(our name, rgba array)] front -> back"""
    psd = PSDImage.new('RGBA', (1024, 1024))
    table = []
    for n, a in reversed(order):  # psd: bottom first
        sn = stretchy_name(n)
        ys, xs = np.nonzero(a[..., 3] > 0)
        if not len(ys):
            continue
        t, l, b, r = ys.min(), xs.min(), ys.max() + 1, xs.max() + 1
        psd.append(PixelLayer.frompil(Image.fromarray(a[t:b, l:r]), psd, sn, top=int(t), left=int(l)))
        table.append({'layer': n, 'stretchy_name': sn, 'tag': match_tag(sn), 'bbox': [int(l), int(t), int(r), int(b)]})
    psd.save(out)
    json.dump({'from': src_psd, 'front_to_back': table[::-1]}, open(out[:-4] + '.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    return table


def main():
    v1 = json.load(open('final/miku_v1/mix.json', encoding='utf-8')) if False else None  # noqa (order from files)
    order1 = [(f[3:-4], np.asarray(Image.open(f'final/miku_v1/layers/{f}').convert('RGBA')))
              for f in sorted(os.listdir('final/miku_v1/layers'))]
    rig = json.load(open('final/miku_v2/rig.json', encoding='utf-8'))
    order2 = [(L['name'], np.asarray(Image.open(f"final/miku_v2/{L['file']}").convert('RGBA')))
              for L in rig['layers_front_to_back']]
    for src, out, order in (('final/miku_v1/miku_v1.psd', 'final/miku_v1/miku_v1_stretchy.psd', order1),
                            ('final/miku_v2/miku_v2.psd', 'final/miku_v2/miku_v2_stretchy.psd', order2)):
        tab = write(src, out, order)
        tags = {}
        for r in tab:
            tags.setdefault(r['tag'], []).append(r['layer'])
        print(out, len(tab), 'layers')
        for k, v in sorted(tags.items(), key=lambda kv: str(kv[0])):
            print(f'  {k}: {v}')


if __name__ == '__main__':
    main()
