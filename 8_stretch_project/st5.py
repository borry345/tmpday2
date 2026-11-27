"""Make a .stretch project with real joint pivots (from rig.json test bones) and limb skin weights computed for them.
Order matters: Stretchy computes elbow/knee weights when a limb mesh is (re)generated, from the pivots at that time.
  load PSD -> wizard (bounds rig, no DWPose) -> set 8 joint pivots -> hide armature -> Remesh every limb layer -> Save
usage: st5.py <stretchy psd> <out .stretch> <tag>"""
import os, sys
from playwright.sync_api import sync_playwright
T = os.path.dirname(os.path.abspath(__file__))
psd, out, tag = sys.argv[1], sys.argv[2], sys.argv[3]
# Stretchy groups are character-side: left* = image right = our *_r
PIVOTS = {'rightArm': (488.3, 480), 'rightElbow': (466.1, 554.8), 'leftArm': (565, 480), 'leftElbow': (601.7, 558.8),
          'rightLeg': (497.4, 620), 'rightKnee': (484.8, 721.9), 'leftLeg': (584.3, 621), 'leftKnee': (605.3, 732.1)}
LIMBS = ['handwear-l', 'handwear-r', 'legwear-l', 'legwear-r']

with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge', headless=True)
    pg = b.new_page(viewport={'width': 1600, 'height': 1000}, accept_downloads=True)
    logs = []
    pg.on('console', lambda m: logs.append(m.text) if '[Skinning]' in m.text or 'rror' in m.text else None)
    pg.goto('https://editor.stretchy.studio', wait_until='networkidle', timeout=90000)
    pg.wait_for_timeout(2000)
    pg.locator('input[type=file]').set_input_files(psd)
    pg.wait_for_timeout(5000)
    pg.get_by_role('button', name='Continue →').click(); pg.wait_for_timeout(3000)
    pg.get_by_text('Next: Adjust Joints').click(); pg.wait_for_timeout(3000)
    pg.get_by_role('button', name='Finish Setup').click(); pg.wait_for_timeout(8000)
    logs.clear()  # skinning lines from Finish Setup used the guessed pivots
    num = pg.locator('input[type=number]')
    for g, (x, y) in PIVOTS.items():
        pg.get_by_text(g, exact=True).first.click(); pg.wait_for_timeout(600)
        for idx, val in ((5, x), (6, y)):
            e = num.nth(idx); e.fill(str(val)); e.press('Enter'); pg.wait_for_timeout(250)
    n = 0
    for name in LIMBS:
        items = pg.get_by_text(name, exact=True)
        for i in range(items.count()):
            items.nth(i).click(); pg.wait_for_timeout(500)
            pg.get_by_role('button', name='Remesh').first.click(); pg.wait_for_timeout(1500)
            n += 1
    pg.wait_for_timeout(2000)
    pg.screenshot(path=f'{T}/st_{tag}_10_remeshed.png')
    pg.locator('button[title="Save project"]').click(); pg.wait_for_timeout(1500)
    pg.get_by_role('tab', name='Download File').click(); pg.wait_for_timeout(500)
    pg.locator('#name').fill(os.path.splitext(os.path.basename(out))[0])
    with pg.expect_download(timeout=120000) as dl:
        pg.get_by_role('button', name='Save', exact=True).click()
    dl.value.save_as(out)
    print('remeshed', n, 'saved', out, os.path.getsize(out))
    print('\n'.join(logs))
    b.close()
