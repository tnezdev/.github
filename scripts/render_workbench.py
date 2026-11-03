"""Render theme-aware organization headers with Pillow; no network/system fonts.

Brand reference: tnezdev/brand@0ecee6ba7f503c635d18a5c525533b9da6bf8ee8.
Run from any directory: python scripts/render_workbench.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'profile' / 'assets'
SCALE = 2
WIDTH, HEIGHT = 1200, 300
# Printed red roles, unchanged from index.html's palettes.printed.
PALETTES = {
    'light': {'bg': '#F2F0EB', 'fg': '#18243B', 'muted': '#596579',
              'accent': '#C1412C', 'line': '#C8CAD0'},
    'dark': {'bg': '#18243B', 'fg': '#F2F0EB', 'muted': '#B5C0D0',
             'accent': '#F17864', 'line': '#42516C'},
}
CHEVRON = ((28, 22), (72, 50), (28, 78))
CHEVRON_STROKE = 8


def font(size, weight=400):
    face = ImageFont.truetype(str(ASSETS / 'fonts' / 'dm-sans.ttf'), round(size * SCALE))
    face.set_variation_by_axes([min(40, max(9, size)), weight])
    return face


def luminance(hex_color):
    rgb = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]
    return sum(a * b for a, b in zip(linear, (.2126, .7152, .0722)))


def contrast(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + .05) / (lo + .05)


def smooth(value):
    value = max(0, min(1, value))
    return value * value * (3 - 2 * value)


def background(color):
    # Fade brand-colored paper into the actual page, not into a guessed
    # GitHub background color. Alpha reaches zero on all four image edges.
    w, h = WIDTH*SCALE, HEIGHT*SCALE
    horizontal = [smooth(min(x, w-1-x)/(112*SCALE)) for x in range(w)]
    vertical = [smooth(min(y/(64*SCALE), (h-1-y)/(132*SCALE))) for y in range(h)]
    mask = Image.frombytes('L', (w, h), bytes(
        round(200 * horizontal[x] * vertical[y]) for y in range(h) for x in range(w)
    ))
    im = Image.new('RGBA', (w, h), color)
    im.putalpha(mask)
    return im


def render(mode):
    colors = PALETTES[mode]
    im = background(colors['bg'])
    draw = ImageDraw.Draw(im)

    def dot(x, y, radius, role):
        draw.ellipse(((x-radius)*SCALE, (y-radius)*SCALE,
                      (x+radius)*SCALE, (y+radius)*SCALE), fill=colors[role])

    def path(points, role, width: float = 1, rounded=False):
        draw.line([(round(x*SCALE), round(y*SCALE)) for x, y in points],
                  fill=colors[role], width=round(width*SCALE), joint='curve')
        if rounded:
            for x, y in points:
                dot(x, y, width/2, role)

    # Enlarge the identity, not its repeated metadata. Scale canonical
    # 24px name / 28px mark / 12px gap; preserve 550 weight and -.04em tracking.
    size, baseline = 116, 190
    mark_size, mark_x = size * 28/24, 12
    name_x = mark_x + mark_size + size * 12/24
    face = font(size, 550)
    x_box = face.getbbox('x', anchor='ls')
    lowercase_center = baseline + (x_box[1] + x_box[3]) / (2*SCALE)
    mark_y = lowercase_center - mark_size/2
    points = [(mark_x+x*mark_size/100, mark_y+y*mark_size/100) for x,y in CHEVRON]
    path(points, 'accent', CHEVRON_STROKE*mark_size/100, rounded=True)
    cursor = name_x*SCALE
    for letter in 'tnezdev':
        box = draw.textbbox((cursor, baseline*SCALE), letter, font=face, anchor='ls')
        assert box[0] >= 0 and box[1] >= 0 and box[2] < WIDTH*SCALE and box[3] < HEIGHT*SCALE
        draw.text((cursor, baseline*SCALE), letter, font=face, fill=colors['fg'], anchor='ls')
        cursor += face.getlength(letter) - .04*size*SCALE
    assert cursor < 780*SCALE

    # Two independent routes remain the Workbench motif. No improvised arrow,
    # enclosing rule, grid, small labels, byline, or repeated tagline.
    path([(850,100), (928,100), (980,148), (1136,148)], 'accent', 5, True)
    path([(850,212), (928,212), (980,168), (1136,168)], 'muted', 5, True)
    dot(850,100,7,'accent')
    dot(850,212,7,'muted')

    # Check brand role contrast on the brand surface. Actual composite
    # backgrounds and theme routing are separately checked in preview tests.
    for role in ('fg', 'muted', 'accent'):
        ratio = contrast(colors[role], colors['bg'])
        assert ratio >= 4.5, (mode, role, ratio)
        print(f'{mode} {role}/brand-bg contrast: {ratio:.2f}:1')
    alpha = im.getchannel('A')
    w, h = im.size
    for edge in ((0,0,w,1), (0,h-1,w,h), (0,0,1,h), (w-1,0,w,h)):
        assert alpha.crop(edge).getextrema() == (0,0)
    dest = ASSETS / f'workbench-{mode}.png'
    im.save(dest)
    with Image.open(dest) as check:
        assert check.mode == 'RGBA' and check.size == (2400,600)
        check.verify()
    print(f'Rendered and verified: {dest}')
    return im


if __name__ == '__main__':
    for treatment in PALETTES:
        render(treatment)
