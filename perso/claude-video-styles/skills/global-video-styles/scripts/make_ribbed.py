"""Render the fluted (ribbed) dark-glass background of the Dark Teal scenes as a high-res PNG.

usage: python make_ribbed.py out.png [w=2160] [h=3840] [tint=#16191c] [accent=none|teal|red] [split=1] [seed=3]
Each flute = a cylinder: dark edge -> lit centre -> dark edge (cosine profile + specular strip), widths 0.65-1.2 x base,
a soft vertical light pool (key light from the upper left), the diagonal split (bottom-left -> top-right, ~62 deg) where the right
half is lighter with a 1 px bright edge, and 2 % monochrome grain. Matches the reference crops in eightsenses-study/hires.
"""
import sys, numpy as np
from PIL import Image

args = dict(a.split("=", 1) for a in sys.argv[2:])
out = sys.argv[1]
W, H = int(args.get("w", 2160)), int(args.get("h", 3840))
rng = np.random.default_rng(int(args.get("seed", 3)))
tint = np.array([int(args.get("tint", "#16191c")[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255

# flute layout
base = W / float(args.get('flutes', 18))
xs, x = [], 0.0
while x < W:
    w = base * rng.uniform(0.65, 1.2); xs.append((x, w)); x += w
col = np.zeros(W, np.float32); spec = np.zeros(W, np.float32)
for x0, w in xs:
    i0, i1 = int(x0), min(W, int(x0 + w))
    u = (np.arange(i0, i1) - x0) / w  # 0..1 across the flute
    col[i0:i1] = 0.30 + 0.70 * np.clip(np.sin(np.pi * u), 0, 1) ** 1.1          # cylinder shading
    spec[i0:i1] = np.exp(-((u - 0.38) / 0.07) ** 2) * rng.uniform(0.15, 0.35)  # specular strip, slightly left of centre
    col[i0:min(W, i0 + 2)] *= 0.55                                 # dark seam
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
# light pool: soft key light upper-left + vertical falloff
pool = 0.55 + 0.45 * np.exp(-(((xx - 0.38 * W) / (0.55 * W)) ** 2 + ((yy - 0.25 * H) / (0.75 * H)) ** 2))
lum = col[None, :] * pool + spec[None, :] * 0.35 * pool
# diagonal split: right/lower region lighter
if args.get("split", "1") == "1":
    # line from (0.02W, H) to (W, 0.05H)
    x1, y1, x2, y2 = 0.02 * W, H, W, 0.05 * H
    d = ((x2 - x1) * (y1 - yy) - (y2 - y1) * (x1 - xx)) / np.hypot(x2 - x1, y2 - y1)
    right = (d < 0).astype(np.float32)
    soft = np.clip(-d / (0.5 * W), 0, 1)
    flat = 0.95 + 0.20 * (1 - soft)  # the split side is a flat lighter glass sheet, flutes only faintly visible
    lum = lum * (1 - right) + right * (0.35 * lum + flat)
    edge = np.exp(-(d / (W / 900)) ** 2) * 1.6
    lum = lum + edge * (0.4 + 0.6 * (1 - yy / H))
lum = lum / lum.max()
img = tint[None, None, :] * 0.6 + (lum[..., None] * np.array([0.21, 0.225, 0.235], np.float32))
acc = args.get("accent", "none")
if acc != "none":
    a = {"teal": [0.10, 0.55, 0.55], "red": [0.89, 0.04, 0.09]}[acc]
    glow = np.exp(-(((xx - 0.5 * W) / (0.6 * W)) ** 2 + ((yy - 1.05 * H) / (0.35 * H)) ** 2)) * 0.18
    img = img + glow[..., None] * np.array(a, np.float32)
from PIL import ImageFilter
im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(W / 540))  # out-of-focus softness
img = np.asarray(im).astype(np.float32) / 255 + rng.normal(0, 0.010, (H, W, 1)).astype(np.float32)  # grain after blur
Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).save(out)
print("wrote", out, W, H)
