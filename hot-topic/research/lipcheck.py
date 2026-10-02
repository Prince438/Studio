"""Lip-sync QC: correlate Kopi's open-mouth pixel count in the final video with the voice RMS per frame."""
import json, subprocess, sys, numpy as np, soundfile as sf
V = sys.argv[1] if len(sys.argv) > 1 else 'out/video_silent.mp4'; FPS = 30
W, H = 1920, 1080
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', V, '-vf', 'crop=560:640:980:300', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
cols = np.array([[0x5b, 0x1a, 0x24], [0xe3, 0x6d, 0x7a]])
regions = [(0, 0, 400, 480), (309, 348, 240, 288)]           # studio Kopi, cam Kopi (full res, inside the 980,300 crop)
counts = []
while True:
    b = p.stdout.read(560 * 640 * 3)
    if len(b) < 560 * 640 * 3: break
    f = np.frombuffer(b, np.uint8).reshape(640, 560, 3).astype(int); n = 0
    t = len(counts) / FPS   # studio shots: open, first 3 s of each story, outro; otherwise the studio cam
    studio = 4.5 <= t < 11 or t >= 76 or any(11 + 13 * i <= t < 14 + 13 * i for i in range(5))
    x, y, w, h = regions[0 if studio else 1]
    c = f[y:y + h, x:x + w]
    for col in cols: n += int((np.abs(c - col).sum(2) < 60).sum())
    counts.append(n / (100 if studio else 36))   # per pixel-art unit: studio Kopi is drawn 10 px/unit, the cam 6 px/unit
counts = np.array(counts, float); nf = len(counts)
tl = json.load(open('vo/timeline.json')); rms = np.zeros(nf)
for c in tl['clips']:
    a, sr = sf.read(f"vo/clips/{c['id']}.wav"); hop = sr // FPS; k = len(a) // hop
    r = np.sqrt((a[:k * hop].reshape(k, hop) ** 2).mean(1)); f0 = int(round(c['start'] * FPS)); rms[f0:f0 + k] = r[:nf - f0]
talk = rms > 0
import math
for lag in (-2, -1, 0, 1, 2):
    a, b = counts[talk], np.roll(rms, lag)[talk]
    print(f'lag {lag:+d}: r = {np.corrcoef(a, b)[0, 1]:.3f}')
print('frames', nf, 'talking', int(talk.sum()))
import re
code = np.array([int(ch) for ch in re.search(r'kopi:"(\d+)"', open('lipsync.js').read()).group(1)][:nf], float)
area = np.array([0, 10, 15, 24, 8.0])[code.astype(int)]          # open-mouth area per shape, in pixel-art units
for lag in (-1, 0, 1):
    print(f'mouth pixels vs lip-sync track, lag {lag:+d}: r = {np.corrcoef(counts[talk], np.roll(area, lag)[talk])[0, 1]:.3f}')
print('lip-sync track vs voice RMS: r =', round(float(np.corrcoef(area[talk], rms[talk])[0, 1]), 3))
st = np.array([4.5 <= k / FPS < 11 or k / FPS >= 76 or any(11 + 13 * i <= k / FPS < 14 + 13 * i for i in range(5)) for k in range(nf)])
for name, m in (('studio', st & talk), ('cam', ~st & talk)):
    print(name, 'r(lag 0) =', round(float(np.corrcoef(counts[m], rms[m])[0, 1]), 3), 'frames', int(m.sum()))
# baseline shifts (poses, arms, cam thumbnails) swamp the raw counts; compare after removing a 2 s rolling median
from scipy.ndimage import median_filter
hpc = counts - median_filter(counts, 61, mode='nearest'); hpa = area - median_filter(area, 61, mode='nearest'); hpr = rms - median_filter(rms, 61, mode='nearest')
for lag in (-1, 0, 1):
    print(f'detrended: mouth vs track lag {lag:+d}: r = {np.corrcoef(hpc[talk], np.roll(hpa, lag)[talk])[0, 1]:.3f}   mouth vs voice: r = {np.corrcoef(hpc[talk], np.roll(hpr, lag)[talk])[0, 1]:.3f}')
