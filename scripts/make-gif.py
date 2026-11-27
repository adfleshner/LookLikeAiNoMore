#!/usr/bin/python3 -I
"""make-gif.py OUT.gif WIDTH SECONDS_PER_FRAME FRAME.png...  -> a looping GIF with one shared palette."""
import sys
from PIL import Image

out, width, secs, frames = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4:]
imgs = []
for f in frames:
    im = Image.open(f).convert("RGB")
    imgs.append(im.resize((width, round(im.height * width / im.width)), Image.LANCZOS))
pal = imgs[0].quantize(colors=128, method=Image.Quantize.MEDIANCUT)
q = [im.quantize(palette=pal, dither=Image.Dither.NONE) for im in imgs]
q[0].save(out, save_all=True, append_images=q[1:], duration=int(secs * 1000), loop=0, optimize=True)
print("wrote", out)
