"""Turn the voiceover clips into per-frame mouth shapes, one track per speaker -> lipsync.js
window.LIPSYNC = {fps, codes: {kenji: "...", kopi: "..."}}
codes: 0 closed/idle, 1 small, 2 medium, 3 wide, 4 'O' (rounded vowel)"""
import json, numpy as np, soundfile as sf
import sys
FPS, DUR = 30, float(sys.argv[1]) if len(sys.argv) > 1 else 30.0
tl = json.load(open('vo/timeline.json'))
nf = int(FPS * DUR); tracks = {}
for c in tl['clips']:
    a, sr = sf.read(f"vo/clips/{c['id']}.wav"); a = a if a.ndim == 1 else a.mean(1)
    hop = sr // FPS; n = len(a) // hop
    fr = a[: n * hop].reshape(n, hop)
    rms = np.sqrt((fr ** 2).mean(1))
    spec = np.abs(np.fft.rfft(fr * np.hanning(hop), axis=1)); freqs = np.fft.rfftfreq(hop, 1 / sr)
    cent = (spec * freqs).sum(1) / (spec.sum(1) + 1e-9)
    ref = np.percentile(rms[rms > 1e-4], 90) if (rms > 1e-4).any() else 1
    lvl = np.convolve(rms / ref, [0.25, 0.5, 0.25], mode='same')
    k = np.select([lvl < 0.14, lvl < 0.42, lvl < 0.75], [0, 1, 2], 3)
    k[(k >= 2) & (cent < 1100)] = 4            # low, rounded vowels -> 'O'
    k = np.repeat(k[::2], 2)[:n]               # hold each shape 2 frames (15 fps, cartoon feel)
    codes = tracks.setdefault(c['speaker'], np.zeros(nf, dtype=int))
    f0 = int(round(c['start'] * FPS)); codes[f0:f0 + n] = k[: nf - f0]
body = ','.join('%s:"%s"' % (sp, ''.join(map(str, c))) for sp, c in tracks.items())
open('lipsync.js', 'w').write('window.LIPSYNC={fps:%d,codes:{%s}};\n' % (FPS, body))
for sp, c in tracks.items():
    print(f"lipsync {sp}: {nf} frames, mouth open {(c > 0).mean():.0%} of the time, dist {np.bincount(c, minlength=5).tolist()}")
