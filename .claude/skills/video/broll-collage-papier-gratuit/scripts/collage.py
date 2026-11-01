#!/usr/bin/env python3
"""Collage papier demi-teinte animé — 100 % local, gratuit (PIL + numpy + ffmpeg).

Usage :
  python3 collage.py spec.json --still out.png      # image fixe finale (porte 2)
  python3 collage.py spec.json --video out.mp4      # animation d'assemblage (porte 3)
Voir le SKILL.md pour le format de spec.json.
"""
import argparse, json, math, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter, ImageChops

def hexrgb(h): h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def paper_bg(size, color, grain, seed=7):
    rng = np.random.default_rng(seed)
    w, h = size
    base = np.zeros((h, w, 3), np.float32) + hexrgb(color)
    n = rng.normal(0, 1, (h, w)).astype(np.float32)
    n = np.asarray(Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype("uint8"))
                   .filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255 - 0.5
    fib = rng.normal(0, 1, (h // 8 + 1, w // 2 + 1)).astype(np.float32)
    fib = np.asarray(Image.fromarray(((fib - fib.min()) / (fib.max() - fib.min()) * 255).astype("uint8"))
                     .resize((w, h), Image.BICUBIC), np.float32) / 255 - 0.5
    out = base + (n * 60 + fib * 40)[..., None] * grain * 6
    return Image.fromarray(np.clip(out, 0, 255).astype("uint8"), "RGB")

def halftone(img, cell, strength=1.0):
    """Demi-teinte couleur : points dont le rayon dépend de la saturation/obscurité."""
    rgba = np.asarray(img.convert("RGBA"), np.float32)
    h, w, _ = rgba.shape
    cw, ch = math.ceil(w / cell), math.ceil(h / cell)
    small = np.asarray(img.convert("RGBA").resize((cw, ch), Image.BOX), np.float32)
    big = np.asarray(Image.fromarray(small.astype("uint8"), "RGBA").resize((cw * cell, ch * cell), Image.NEAREST), np.float32)[:h, :w]
    yy, xx = np.mgrid[0:h, 0:w]
    u = ((xx % cell) + 0.5) / cell - 0.5
    v = ((yy % cell) + 0.5) / cell - 0.5
    dist = np.sqrt(u * u + v * v)
    px = rgba[..., :3] / 255
    rgb = big[..., :3] / 255 * 0.45 + px * 0.55   # mélange moyenne de cellule / pixel : bords nets
    dark = 1 - (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]) * 0.75
    r = 0.12 + 0.50 * np.sqrt(np.clip(dark, 0, 1)) * strength
    dot = (dist < r)[..., None]
    light = rgb * 0.18 + 0.82                      # fond de la pièce : couleur très éclaircie
    out = np.where(dot, rgb * 0.97, light)
    res = np.dstack([out * 255, rgba[..., 3]])     # alpha d'origine
    return Image.fromarray(np.clip(res, 0, 255).astype("uint8"), "RGBA")

def paper_cut(img, edge, seed):
    """Bord blanc irrégulier (découpe) + ombre portée. Renvoie (pièce, ombre)."""
    a = img.getchannel("A")
    rng = np.random.default_rng(seed)
    noise = Image.fromarray(rng.integers(0, 255, a.size[::-1], dtype=np.uint8)).filter(ImageFilter.GaussianBlur(3))
    grown = a.filter(ImageFilter.MaxFilter(edge * 2 + 1)).filter(ImageFilter.GaussianBlur(1.2))
    grown = ImageChops.multiply(grown, noise.point(lambda p: 200 + p // 5))
    grown = grown.point(lambda p: 255 if p > 110 else 0)
    base = Image.new("RGBA", img.size, (250, 247, 240, 0)); base.putalpha(grown)
    base.alpha_composite(img)
    shadow = Image.new("RGBA", img.size, (30, 20, 10, 0))
    shadow.putalpha(grown.filter(ImageFilter.GaussianBlur(7)).point(lambda p: int(p * 0.38)))
    return base, shadow

def ease_out_back(t, s=1.5):
    t -= 1; return t * t * ((s + 1) * t + s) + 1
def ease_out_cubic(t): return 1 - (1 - t) ** 3
def clamp(x): return max(0.0, min(1.0, x))

def prepare(spec, base_dir):
    W, H = spec["size"]; cell = spec.get("halftone_cell", max(3, W // 300))
    prepared = []
    for i, L in enumerate(spec["layers"]):
        im = Image.open(base_dir / L["src"]).convert("RGBA")
        tw = int(W * L.get("width", 0.3)); th = int(im.height * tw / im.width)
        im = im.resize((tw, th), Image.LANCZOS)
        if L.get("halftone", True): im = halftone(im, L.get("cell", cell), L.get("strength", 1.0))
        piece, shadow = paper_cut(im, L.get("edge", max(3, W // 400)), seed=i + 1)
        prepared.append((piece, shadow))
    return prepared

def frame(spec, prepared, bg, t):
    W, H = spec["size"]
    out = bg.copy().convert("RGBA")
    for L, (piece, shadow) in zip(spec["layers"], prepared):
        d0, dur = L.get("delay", 0.0), L.get("dur", 0.7)
        p = clamp((t - d0) / dur)
        if p <= 0: continue
        cx, cy = L.get("x", 0.5) * W, L.get("y", 0.5) * H
        rot = L.get("rot", 0.0)
        enter = L.get("enter", "scale")
        e, eb = ease_out_cubic(p), ease_out_back(p)
        dx = dy = 0.0; sc = 1.0; extra_rot = 0.0; alpha = 1.0
        if enter == "left": dx = -(1 - eb) * W * 0.7
        elif enter == "right": dx = (1 - eb) * W * 0.7
        elif enter == "top": dy = -(1 - eb) * H * 0.9
        elif enter == "bottom": dy = (1 - eb) * H * 0.9
        elif enter == "drop": dy = -(1 - eb) * H * 0.9; extra_rot = (1 - e) * 12
        elif enter == "spin": sc = max(0.01, eb); extra_rot = (1 - e) * 120
        else: sc = max(0.01, eb)                     # "scale" : pop
        alpha = clamp(p * 4)
        for im, off, op in ((shadow, (10, 14), 1.0), (piece, (0, 0), 1.0)):
            r = im.rotate(rot + extra_rot, expand=True, resample=Image.BICUBIC)
            if sc != 1.0: r = r.resize((max(1, int(r.width * sc)), max(1, int(r.height * sc))), Image.BICUBIC)
            if alpha < 1: r.putalpha(r.getchannel("A").point(lambda a: int(a * alpha)))
            out.alpha_composite(r, (int(cx + dx - r.width / 2 + off[0]), int(cy + dy - r.height / 2 + off[1])))
    # léger « boil » : décalage 1 px par pas de 1/8 s pour une vie de papier
    return out.convert("RGB")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("--still"); ap.add_argument("--video")
    a = ap.parse_args()
    sp = Path(a.spec); spec = json.loads(sp.read_text()); base = sp.parent
    W, H = spec["size"]; fps = spec.get("fps", 24); dur = spec.get("duration", 5.0)
    bg = paper_bg((W, H), spec.get("background", "#efe6d2"), spec.get("grain", 0.05))
    prepared = prepare(spec, base)
    if a.still:
        frame(spec, prepared, bg, 999).save(a.still); print("still ->", a.still)
    if a.video:
        n = int(dur * fps)
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
               "-r", str(fps), "-i", "-", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", a.video]
        pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for i in range(n):
            t = i / fps
            pr.stdin.write(frame(spec, prepared, bg, t).tobytes())
        pr.stdin.close(); pr.wait(); print("video ->", a.video, f"({n} images)")
    if not (a.still or a.video): sys.exit("Précisez --still et/ou --video")

if __name__ == "__main__": main()
