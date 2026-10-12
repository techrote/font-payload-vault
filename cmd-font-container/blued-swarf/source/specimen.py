"""Specimen sheets rendered straight from the (FreeType-verified) bitmaps."""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import swarf

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'specimen')
BG = (28, 27, 25)
INK = (216, 210, 196)
DIM = (128, 122, 110)
RUST = (110, 142, 196)      # temper blue (name kept for diff-friendliness)
PANEL = (40, 38, 35)

def draw_text(img, cells, x, y, text, color):
    px = img.load()
    for ch in text:
        c = cells.get(ch, cells['?'])
        for yy, r in enumerate(c.rows):
            for i, v in enumerate(r):
                if v:
                    X, Y = x + c.lsb + i, y + yy
                    if 0 <= X < img.width and 0 <= Y < img.height:
                        px[X, Y] = color
        x += c.adv
    return x

def width(cells, text):
    return sum(cells.get(c, cells['?']).adv for c in text)

def sizes_sheet(reg, bold, scale=2):
    sizes = sorted(swarf.SIZES)
    lab = reg[9]
    lines = ['The quick brown fox jumps over the lazy dog. 0123456789',
             'SPHINX OF BLACK QUARTZ, JUDGE MY VOW! (#$%&@) [{<>}]']
    W = 64 + max(width(bold[16], l) for l in lines) + 20
    H = 40 + sum(2 * p + 14 for p in sizes)
    img = Image.new('RGB', (W, H), BG)
    draw_text(img, reg[11], 20, 10, 'BLUED SWARF  pixel font  6-16px   regular + bold', RUST)
    y = 34
    for p in sizes:
        draw_text(img, lab, 20, y + max(0, (p - 9) // 2), f'{p}px', DIM)
        draw_text(img, reg[p], 64, y, lines[0], INK)
        y += p + 2
        draw_text(img, bold[p], 64, y, lines[1], INK)
        y += p + 12
    img = img.crop((0, 0, W, y))
    return img.resize((img.width * scale, img.height * scale), Image.NEAREST)

def charset_sheet(cells, p, scale):
    chars = [c for c in sorted(cells, key=ord) if c not in ('\u00a0', '\u00ad', ' ')]
    per = 32
    cw = max(cells[c].adv for c in chars) + 3
    rows = (len(chars) + per - 1) // per
    W = per * cw + 40
    H = rows * (p + 6) + 40
    img = Image.new('RGB', (W, H), BG)
    draw_text(img, cells, 20, 10,
              f'{p}px  {len(chars)} glyphs', RUST)
    for i, ch in enumerate(chars):
        x = 20 + (i % per) * cw
        y = 30 + (i // per) * (p + 6)
        c = cells[ch]
        draw_text(img, cells, x + (cw - c.adv) // 2, y, ch, INK)
    return img.resize((img.width * scale, img.height * scale), Image.NEAREST)

def ui_mock(reg, bold, p_ui=11, scale=2):
    """A Win3.x/9x-flavoured mock-up to judge the font in context at 1:1 pixels."""
    W, H = 520, 300
    img = Image.new('RGB', (W, H), (58, 64, 62))
    d = ImageDraw.Draw(img)
    f, fb = reg[p_ui], bold[p_ui]
    # window
    d.rectangle([30, 20, 330, 200], fill=(190, 186, 176), outline=(20, 20, 20))
    d.rectangle([33, 23, 327, 23 + p_ui + 4], fill=(38, 58, 98))
    draw_text(img, fb, 38, 25, 'C:\\BLUED\\README.TXT - Notepad', (235, 228, 214))
    menu_y = 23 + p_ui + 6
    x = 38
    for m in ('File', 'Edit', 'Search', 'Help'):
        x = draw_text(img, f, x, menu_y, m, (20, 20, 20)) + 10
    d.rectangle([33, menu_y + p_ui + 2, 327, 197], fill=(244, 240, 230), outline=(110, 106, 98))
    body = ['BLUED SWARF: a pixel font for small sizes.',
            'Every size from 6 to 16px is hand-tuned',
            'to the pixel grid: no blur, no mush.',
            '', 'Sizes:  6 7 8 9 10 11 12 13 14 15 16',
            'Weights: Regular, Bold (VGA-style)']
    yy = menu_y + p_ui + 5
    for line in body:
        draw_text(img, f, 37, yy, line, (24, 24, 24)); yy += p_ui + 1
    # DOS box
    t = reg[10]
    d.rectangle([250, 110, 500, 250], fill=(12, 12, 12), outline=(140, 136, 126))
    lines = ['Microsoft(R) MS-DOS(R) Version 6.22', '', 'C:\\>dir /w *.fon',
             ' Volume in drive C is BLUED', '[FON]   BLUEDSYS.FON  BLUEDSYB.FON',
             '        2 file(s)   85,568 bytes', '', 'C:\\>_']
    yy = 114
    for l in lines:
        draw_text(img, t, 255, yy, l, (200, 196, 186)); yy += 11
    # taskbar
    d.rectangle([0, H - 26, W, H], fill=(190, 186, 176))
    d.line([0, H - 26, W, H - 26], fill=(240, 236, 228))
    d.rectangle([3, H - 23, 56, H - 4], fill=(205, 201, 191), outline=(30, 30, 30))
    draw_text(img, fb, 10, H - 20, 'Start', (20, 20, 20))
    bx = 62
    for title in ('README.TXT - Notepad', 'MS-DOS Prompt'):
        wdt = width(f, title) + 12
        d.rectangle([bx, H - 23, bx + wdt, H - 4], fill=(205, 201, 191), outline=(90, 88, 84))
        draw_text(img, f, bx + 6, H - 19, title, (20, 20, 20))
        bx += wdt + 4
    d.rectangle([W - 66, H - 23, W - 4, H - 4], outline=(120, 116, 108))
    draw_text(img, f, W - 58, H - 19, '12:45 PM', (20, 20, 20))
    # small-size labels
    draw_text(img, reg[8], 34, 212, 'tiny 8px label: ready.  disk 74% full  [OK] [Cancel]', (230, 226, 216))
    draw_text(img, reg[6], 34, 226, '6px micro text: 192.168.0.1  CPU 42C  fan 1200rpm', (230, 226, 216))
    draw_text(img, bold[16], 34, 240, 'VGA 16px BOLD', (230, 226, 216))
    return img.resize((W * scale, H * scale), Image.NEAREST)

def main():
    ms, reg, bold = swarf.all_sizes()
    os.makedirs(OUT, exist_ok=True)
    sizes_sheet(reg, bold, 2).save(os.path.join(OUT, 'specimen-sizes.png'))
    imgs = [charset_sheet(reg[p], p, 2) for p in (6, 10, 16)]
    W = max(i.width for i in imgs); H = sum(i.height for i in imgs)
    sheet = Image.new('RGB', (W, H), BG)
    y = 0
    for i in imgs:
        sheet.paste(i, (0, y)); y += i.height
    sheet.save(os.path.join(OUT, 'specimen-charset.png'))
    ui_mock(reg, bold).save(os.path.join(OUT, 'specimen-ui.png'))
    print('ok')

if __name__ == '__main__':
    main()
