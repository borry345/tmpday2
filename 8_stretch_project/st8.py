"""Bend elbows/knees the way Stretchy skins them: drag the joint's rotation arc on the canvas (SkeletonOverlay).
modes: file = open .stretch ; old = PSD -> wizard -> set pivots afterwards (weights from guessed pivots)"""
import math, os, sys
from playwright.sync_api import sync_playwright
T = os.path.dirname(os.path.abspath(__file__))
mode, src, tag = sys.argv[1], sys.argv[2], sys.argv[3]
PIV = {'rightArm': (488.3, 480), 'rightElbow': (466.1, 554.8), 'leftArm': (565, 480), 'leftElbow': (601.7, 558.8),
       'rightLeg': (497.4, 620), 'rightKnee': (484.8, 721.9), 'leftLeg': (584.3, 621), 'leftKnee': (605.3, 732.1)}
BEND = [('rightElbow', 90), ('leftElbow', -70), ('rightKnee', -60), ('leftKnee', 60)]  # degrees, screen (+ = clockwise)


def circles(pg):
    return pg.evaluate("""() => [...document.querySelectorAll('svg circle')].map(e => {const r = e.getBoundingClientRect();
        return [r.left + r.width / 2, r.top + r.height / 2, r.width]}).filter(c => c[2] > 8 && c[2] < 11)""")


def screen_of(pg, x, y):
    cs = circles(pg)
    for ox, oy in ((562, 8.4), (382, 8.4)):
        best = min(cs, key=lambda c: math.hypot(c[0] - (x + ox), c[1] - (y + oy)))
        if math.hypot(best[0] - (x + ox), best[1] - (y + oy)) < 4:
            return best[0], best[1]
    raise RuntimeError(f'joint at {x},{y} not found among {len(cs)} circles')


def arc_center(pg, jx, jy):
    """rotation arc (270 deg ring, r=28, gap on the right) nearest to the joint dot -> its centre"""
    arcs = pg.evaluate("""() => [...document.querySelectorAll('svg path')].filter(e => (e.getAttribute('stroke')||'').includes('251,191,36'))
        .map(e => {const r = e.getBoundingClientRect(); return [r.left + r.width - 28, r.top + 28]})""")
    return min(arcs, key=lambda a: math.hypot(a[0] - jx, a[1] - jy))


def drag_arc(pg, jx, jy, deg, R=28):
    cx, cy = arc_center(pg, jx, jy)
    a0 = 0.0  # grab the right side of the ring (the gap is on the left)
    pg.mouse.move(cx + R * math.cos(math.radians(a0)), cy); pg.mouse.down()
    steps = 30
    for i in range(1, steps + 1):
        a = math.radians(a0 + deg * i / steps)
        pg.mouse.move(cx + R * math.cos(a), cy + R * math.sin(a))
        pg.wait_for_timeout(20)
    pg.mouse.up(); pg.wait_for_timeout(500)


with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge', headless=True)
    pg = b.new_page(viewport={'width': 1600, 'height': 1000})
    logs = []
    pg.on('console', lambda m: logs.append(m.text) if 'SkeletonOverlay' in m.text else None)
    pg.goto('https://editor.stretchy.studio', wait_until='networkidle', timeout=90000)
    pg.wait_for_timeout(2000)
    pg.locator('input[type=file]').set_input_files(src)
    pg.wait_for_timeout(7000)
    if mode == 'old':
        num = pg.locator('input[type=number]')
        pg.get_by_role('button', name='Continue →').click(); pg.wait_for_timeout(3000)
        pg.get_by_text('Next: Adjust Joints').click(); pg.wait_for_timeout(3000)
        pg.get_by_role('button', name='Finish Setup').click(); pg.wait_for_timeout(8000)
        for g, (x, y) in PIV.items():
            pg.get_by_text(g, exact=True).first.click(); pg.wait_for_timeout(400)
            for idx, val in ((5, x), (6, y)):
                e = num.nth(idx); e.fill(str(val)); e.press('Enter'); pg.wait_for_timeout(200)
        pg.mouse.click(1500, 950); pg.wait_for_timeout(500)
    for g, deg in BEND:
        cx, cy = screen_of(pg, *PIV[g])
        drag_arc(pg, cx, cy, deg)
    pg.wait_for_timeout(1500)
    pg.screenshot(path=f'{T}/st8_{tag}.png')
    print('\n'.join(logs))
    b.close()
print('ok', tag)
