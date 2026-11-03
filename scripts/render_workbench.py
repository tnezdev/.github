"""Render the organization banner with Pillow; no network or system fonts.

Brand reference: tnezdev/brand@0ecee6ba7f503c635d18a5c525533b9da6bf8ee8.
Run from any directory: python scripts/render_workbench.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'profile' / 'assets'
SCALE = 2
WIDTH, HEIGHT = 1200, 330
# Printed red, dark treatment; source: index.html's palettes.printed.dark.
COLORS = {
    'bg': '#18243B', 'fg': '#F2F0EB', 'muted': '#B5C0D0',
    'accent': '#F17864', 'line': '#42516C',
}
CHEVRON = ((28, 22), (72, 50), (28, 78))
CHEVRON_STROKE = 8


def font(size, weight=400):
    face = ImageFont.truetype(str(ASSETS / 'fonts' / 'dm-sans.ttf'), round(size * SCALE))
    # DM Sans variable axes: optical size then weight. Match optical sizing
    # at this display size, within the font's supported 9–40 range.
    face.set_variation_by_axes([min(40, max(9, size)), weight])
    return face


def luminance(hex_color):
    rgb = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]
    return sum(a * b for a, b in zip(linear, (.2126, .7152, .0722)))


def contrast(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + .05) / (lo + .05)


def render():
    im = Image.new('RGB', (WIDTH * SCALE, HEIGHT * SCALE), COLORS['bg'])
    draw = ImageDraw.Draw(im)

    def dot(x, y, radius, role):
        draw.ellipse(((x-radius)*SCALE, (y-radius)*SCALE,
                      (x+radius)*SCALE, (y+radius)*SCALE), fill=COLORS[role])

    def path(points, role, width: float = 1, rounded=False):
        draw.line([(round(x*SCALE), round(y*SCALE)) for x, y in points],
                  fill=COLORS[role], width=round(width*SCALE), joint='curve')
        if rounded:
            for x, y in points:
                dot(x, y, width/2, role)

    def text(x, y, value, size, role, weight=400):
        face = font(size, weight)
        bounds = draw.textbbox((x*SCALE, y*SCALE), value, font=face, anchor='lt')
        assert min(bounds[:2]) >= 0 and bounds[2] <= WIDTH*SCALE and bounds[3] <= HEIGHT*SCALE
        draw.text((x*SCALE, y*SCALE), value, font=face, fill=COLORS[role], anchor='lt')

    text(52, 36, 'INDEPENDENT SOFTWARE PRACTICE', 16, 'muted', 500)

    # Name: reference lockup weight and -.04em tracking. Scale the reference
    # 24px name / 28px square mark / 12px gap together, preserving geometry.
    size, baseline = 100, 192
    mark_size, mark_x = size * 28/24, 24
    name_x = mark_x + mark_size + size * 12/24
    face = font(size, 550)
    x_box = face.getbbox('x', anchor='ls')
    lowercase_center = baseline + (x_box[1] + x_box[3]) / (2*SCALE)
    mark_y = lowercase_center - mark_size/2
    # Optical alignment uses actual lowercase ink at export size rather than
    # duplicating the browser line-box correction after raster layout.
    points = [(mark_x+x*mark_size/100, mark_y+y*mark_size/100) for x,y in CHEVRON]
    path(points, 'accent', CHEVRON_STROKE*mark_size/100, rounded=True)
    cursor = name_x*SCALE
    for letter in 'tnezdev':
        draw.text((cursor, baseline*SCALE), letter, font=face, fill=COLORS['fg'], anchor='ls')
        cursor += face.getlength(letter) - .04*size*SCALE
    assert cursor < 800*SCALE

    text(53, 222, 'People and AI, building useful things together.', 23, 'fg')
    path([(52, 278), (1148, 278)], 'line')
    text(53, 294, 'Travis + Dottie Weaver', 16, 'muted')

    # Retain the selected two-path composition as decoration, not a second
    # logo or directional arrow. Only brand colors; both routes stay distinct.
    for x in range(865, 1150, 28):
        for y in range(88, 242, 28):
            dot(x, y, 1, 'line')
    path([(875,112), (949,112), (995,158), (1125,158)], 'accent', 5, True)
    path([(875,224), (949,224), (995,178), (1125,178)], 'muted', 5, True)
    dot(875,112,7,'accent')
    dot(875,224,7,'muted')

    for role in ('fg', 'muted', 'accent'):
        ratio = contrast(COLORS[role], COLORS['bg'])
        assert ratio >= 4.5, (role, ratio)
        print(f'{role}/bg contrast: {ratio:.2f}:1')
    dest = ASSETS / 'workbench.png'
    im.save(dest)
    with Image.open(dest) as check:
        assert check.size == (2400,660)
        check.verify()
    print(f'Rendered and verified: {dest}')
    return im


if __name__ == '__main__':
    render()
