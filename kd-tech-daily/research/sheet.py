"""Contact sheet of PNG/JPG stills sorted by time: python research/sheet.py <dir> <out.jpg> [cols] [w]"""
import sys, os, re
from PIL import Image, ImageDraw
d, out = sys.argv[1], sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 3; w = int(sys.argv[4]) if len(sys.argv) > 4 else 640
fs = sorted([f for f in os.listdir(d) if f.endswith(('.png', '.jpg'))], key=lambda f: float(re.sub(r'[^0-9.]', '', f.rsplit('.', 1)[0]) or 0))
im0 = Image.open(os.path.join(d, fs[0])); h = round(w * im0.height / im0.width); rows = (len(fs) + cols - 1) // cols; S = Image.new('RGB', (cols * w, rows * h))
for i, f in enumerate(fs):
    im = Image.open(os.path.join(d, f)).convert('RGB').resize((w, h)); ImageDraw.Draw(im).text((6, 4), f, fill=(255, 255, 0)); S.paste(im, ((i % cols) * w, (i // cols) * h))
S.save(out, quality=85); print(out, len(fs))
