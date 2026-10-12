import sys, os
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import swarf

ASCII = ''.join(chr(c) for c in range(33, 127))
SAMPLE = [
    "The quick brown fox jumps over the lazy dog. 0123456789",
    "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG! (#$%&@)",
    "Il1| O0Q rn m cl d g9q 5S 2Z 8B ,.;:'\" -_=+*/\\<> {}[]~^`?",
    "C:\\WINDOWS> dir /w   File Edit View Help   Start  12:45 PM",
]

def render_lines(cells, lines, H, fg=1):
    width = max(sum(cells.get(c, cells['?']).adv for c in l) for l in lines) + 2
    img = Image.new('L', (width, H * len(lines) + 2), 255)
    px = img.load()
    for li, l in enumerate(lines):
        x = 1
        for c in l:
            cell = cells.get(c, cells['?'])
            for y, r in enumerate(cell.rows):
                for i, v in enumerate(r):
                    if v:
                        px[x + cell.lsb + i, 1 + li * H + y] = 0
            x += cell.adv
    return img

def sheet(cells, H, chars, per_line=32):
    lines = [chars[i:i + per_line] for i in range(0, len(chars), per_line)]
    # spaced grid so glyph boxes are visible
    return render_lines(cells, [' '.join(l) for l in lines], H)

def compose(imgs, scale, pad=6, label=None):
    imgs = [i.resize((i.width * scale, i.height * scale), Image.NEAREST) for i in imgs]
    W = max(i.width for i in imgs) + 2 * pad
    Ht = sum(i.height + pad for i in imgs) + pad
    out = Image.new('L', (W, Ht), 255)
    y = pad
    for i in imgs:
        out.paste(i, (pad, y)); y += i.height + pad
    return out

if __name__ == '__main__':
    sizes = [int(s) for s in sys.argv[1].split(',')] if len(sys.argv) > 1 else list(swarf.SIZES)
    which = sys.argv[2] if len(sys.argv) > 2 else 'reg'
    scale = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    ms, reg, bold = swarf.all_sizes()
    src = reg if which == 'reg' else bold
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'preview')
    for p in sizes:
        cells = src[p]
        H = p
        extra = ''.join(c for c in cells if ord(c) > 126 and c not in swarf.PROCEDURAL)
        imgs = [sheet(cells, H, ASCII), sheet(cells, H, extra),
                render_lines(cells, SAMPLE, H)]
        compose(imgs, scale).save(os.path.join(outdir, f'{which}_{p}.png'))
    print('ok')
