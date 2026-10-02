"""Decode captured screenshot pairs (800x940: frame 450 + 20px barcode, twice) into numbered frames.
usage: python3 decode_caps.py <clipname> [since_ms]   -> caps/<clipname>/<ms>.jpg  (ms = video time *1000)"""
import sys, glob, os
from PIL import Image
import numpy as np
D = '/root/.claude/projects/-home-claude/7d4b50e2-c8e4-58d2-9bbe-39469d2a7d3e/tool-results/'
name = sys.argv[1]; since = int(sys.argv[2]) if len(sys.argv) > 2 else 0
out = f'/home/claude/kd-news-1001/caps/{name}'; os.makedirs(out, exist_ok=True)
def code(a, y):
    v = 0
    for b in range(20):
        px = a[y + 10, b * 40 + 20]
        v = (v << 1) | (1 if px.mean() > 128 else 0)
    return v
got = {}
for f in sorted(glob.glob(D + 'mcp-remote-devices-blob-*.jpg'), key=os.path.getmtime):
    ms = int(os.path.basename(f).split('-')[4])
    if ms < since: continue
    im = Image.open(f).convert('RGB')
    if im.size != (800, 940): continue
    a = np.asarray(im)
    for k, (y0, yc) in enumerate([(0, 450), (470, 920)]):
        v = code(a, yc)
        if v == 0: continue
        im.crop((0, y0, 800, y0 + 450)).save(f'{out}/{v:06d}.jpg', quality=95)
        got[v] = got.get(v, 0) + 1
print(len(got), 'frames:', sorted(got)[:3], '...', sorted(got)[-3:])
