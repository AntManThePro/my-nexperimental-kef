#!/usr/bin/env python3
"""MY KEF icon set builder — five-blade rotor + QR finder mark.
Neon #00ff87 on void #07070a, cyan #60efff accents.
Full-detail version for 512/192/180; simplified bold version for .ico (48/32/16).
"""
from PIL import Image, ImageDraw
import math, os

OUT = os.path.dirname(os.path.abspath(__file__))
VOID = (7, 7, 10, 255)
NEON = (0, 255, 135, 255)
CYAN = (96, 239, 255, 255)
NEON_DARK = (0, 180, 96, 255)

def blade_layer(size, sweep=True):
    """One blade pointing up from centre, on its own transparent layer."""
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx = cy = size // 2
    u = size / 512.0  # unit scale
    # Swept petal blade: base at hub, tip offset to one side (fan sweep)
    pts = [
        (cx - 16*u, cy - 34*u),
        (cx + 16*u, cy - 34*u),
        (cx + 40*u, cy - 108*u),
        (cx + 52*u, cy - 158*u),
        (cx + 26*u, cy - 192*u),
        (cx - 6*u,  cy - 186*u),
        (cx - 30*u, cy - 118*u),
    ]
    d.polygon(pts, fill=NEON)
    return layer

def rotor(img, simple=False):
    size = img.width
    cx = cy = size // 2
    u = size / 512.0
    if simple:
        # Bold wedges: 5 thick triangles, no sweep, big hub — survives 16px
        d = ImageDraw.Draw(img)
        for i in range(5):
            a = math.radians(i * 72 - 90)
            # wedge as a fat triangle from hub to rim
            tip = (cx + 0.34*size*math.cos(a), cy + 0.34*size*math.sin(a))
            perp = a + math.pi/2
            w = 0.13*size
            p1 = (cx + w*math.cos(perp), cy + w*math.sin(perp))
            p2 = (cx - w*math.cos(perp), cy - w*math.sin(perp))
            d.polygon([p1, p2, tip], fill=NEON)
        r = int(0.14*size)
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=NEON)
        r2 = int(0.055*size)
        d.ellipse([cx-r2, cy-r2, cx+r2, cy+r2], fill=VOID)
        return img
    # Full rotor: 5 swept blades rotated 72 deg apart
    base = blade_layer(size)
    for i in range(5):
        rot = base.rotate(-i*72, resample=Image.BICUBIC, center=(cx, cy))
        img.alpha_composite(rot)
    d = ImageDraw.Draw(img)
    # Hub: neon disc, cyan ring, void centre dot
    r = int(46*u)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=NEON)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=CYAN, width=max(2, int(5*u)))
    r2 = int(16*u)
    d.ellipse([cx-r2, cy-r2, cx+r2, cy+r2], fill=VOID)
    return img

def qr_finder(d, x, y, s, w):
    """QR position marker: outer square outline + filled centre square."""
    d.rectangle([x, y, x+s, y+s], outline=CYAN, width=w)
    inner = s//3
    off = (s-inner)//2
    d.rectangle([x+off, y+off, x+off+inner, y+off+inner], fill=CYAN)

def bracket(d, x, y, dx, dy, length, w):
    """Thin archive-bracket corner: two lines forming an L."""
    d.line([(x, y+dy*length), (x, y), (x+dx*length, y)], fill=CYAN, width=w)

def full_icon(size):
    img = Image.new("RGBA", (size, size), VOID)
    u = size / 512.0
    d = ImageDraw.Draw(img)
    # Archive-bracket corners (thin cyan L's at the four corners)
    inset = int(14*u)
    blen = int(38*u)
    bw = max(2, int(4*u))
    bracket(d, inset, inset, 1, 1, blen, bw)                                  # TL
    bracket(d, size-inset, inset, -1, 1, blen, bw)                           # TR
    bracket(d, inset, size-inset, 1, -1, blen, bw)                           # BL
    bracket(d, size-inset, size-inset, -1, -1, blen, bw)                     # BR
    # QR finder marks: TL, TR, BL (three, like a QR code)
    fs = int(46*u)   # finder outer size
    fw = max(2, int(6*u))
    pad = int(34*u)
    qr_finder(d, pad, pad, fs, fw)                                            # TL
    qr_finder(d, size-pad-fs, pad, fs, fw)                                    # TR
    qr_finder(d, pad, size-pad-fs, fs, fw)                                    # BL
    # Rotor at centre
    rotor(img, simple=False)
    return img

def simple_icon(size):
    img = Image.new("RGBA", (size, size), VOID)
    rotor(img, simple=True)
    return img

if __name__ == "__main__":
    for size, name in [(512, "favicon-512.png"), (192, "favicon-192.png"), (180, "apple-touch-icon.png")]:
        full_icon(size).convert("RGB").save(os.path.join(OUT, name), "PNG")
        print(name, size)
    # Multi-size .ico from simplified bold versions
    imgs = [simple_icon(s).convert("RGB") for s in (48, 32, 16)]
    imgs[0].save(os.path.join(OUT, "favicon.ico"), format="ICO",
                 sizes=[(48, 48), (32, 32), (16, 16)])
    print("favicon.ico 48/32/16")
