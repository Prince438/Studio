"""Built at KD: synthesize an original 104 BPM chip-funk groove + SFX synced to out/events.json
-> out/music.npy, out/sfx.npy (stems for mix_vo.py) and out/audio.wav (no voice)"""
import json, numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

import os as _os
DUR = json.load(open('out/music.json'))['dur'] if _os.path.exists('out/music.json') else 97.0
SR = 44100; N = int(SR * DUR)
BPM = 104; BEAT = 60 / BPM; STEP = BEAT / 4; BAR = BEAT * 4; SWING = 0.14
rng = np.random.default_rng(11)
music = np.zeros((N, 2)); sfx = np.zeros((N, 2))

def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)
def lp(x, f, o=2): return sosfilt(butter(o, min(f, SR / 2 - 100), 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, min(hi, SR / 2 - 100)], 'band', fs=SR, output='sos'), x)
def tt(d): return np.arange(int(d * SR)) / SR
def expenv(d, dec, att=0.002): t = tt(d); return np.minimum(1, t / att) * np.exp(-t / dec)
def phase(freq, d): f = np.full(int(d * SR), freq) if np.isscalar(freq) else freq; return np.cumsum(f) / SR
def pulse(freq, d, duty=0.5): return np.where((phase(freq, d) % 1) < duty, 1.0, -1.0)
def saw(freq, d): return 2 * (phase(freq, d) % 1) - 1
def sine(freq, d): return np.sin(2 * np.pi * phase(freq, d))
def sweep(f0, f1, d, curve=1.0): return f0 + (f1 - f0) * np.linspace(0, 1, int(d * SR)) ** curve
def add(buf, t, x, gain=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= N or i + len(x) <= 0: return
    if i < 0: x, i = x[-i:], 0
    x = x[: N - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[i:i + len(x), 0] += x * gain * l * 1.414
    buf[i:i + len(x), 1] += x * gain * r * 1.414
def st(bar, step): return bar * BAR + step * STEP + (SWING * STEP if step % 2 else 0)   # swung 16ths

# ---------- instruments ----------
def kick():
    x = np.sin(2 * np.pi * phase(sweep(150, 44, 0.34, 0.3), 0.34)) * expenv(0.34, 0.12)
    c = hp(rng.standard_normal(len(x)), 3000) * expenv(0.34, 0.003)
    return np.tanh(1.8 * x) + 0.3 * c
def snare(ghost=False):
    d = 0.18 if ghost else 0.24
    n = bp(rng.standard_normal(int(d * SR)), 1800, 8000) * expenv(d, 0.03 if ghost else 0.07)
    tone = np.sin(2 * np.pi * 200 * tt(d)) * expenv(d, 0.03)
    return 0.8 * n + (0.2 if ghost else 0.55) * tone
def clap():
    d = 0.3; n = bp(rng.standard_normal(int(d * SR)), 1000, 6000); env = np.zeros(int(d * SR))
    for k, o in enumerate((0, 0.011, 0.022)):
        i = int(o * SR); e = expenv(d, 0.012 if k < 2 else 0.09)[: len(env) - i]; env[i:i + len(e)] += e
    return n * env
def hat(open_=False):
    d = 0.22 if open_ else 0.045
    return hp(rng.standard_normal(int(d * SR)), 8000) * expenv(d, 0.08 if open_ else 0.012)
def tamb():
    d = 0.08; return bp(rng.standard_normal(int(d * SR)), 6000, 14000) * expenv(d, 0.03, 0.006)
def bass(m, d, pop=False):
    """plucky funk bass: bright attack decaying into a round tone; 'pop' = short slapped octave"""
    f = mtof(m); raw = 0.6 * saw(f, d) + 0.4 * pulse(f, d, 0.3)
    bright, dark = lp(raw, 2600 if pop else 1500), lp(raw, 420)
    t = tt(d); k = np.exp(-t / (0.035 if pop else 0.06))
    x = bright * k + dark * (1 - k) + 0.5 * np.sin(2 * np.pi * f * t)
    return x * expenv(d, 0.09 if pop else 0.3, 0.003) * np.clip((d - t) / 0.02, 0, 1)
def clav(ms, d=0.12):
    x = sum(lp(pulse(mtof(m), d, 0.22), 3400) for m in ms) / len(ms)
    return x * expenv(d, 0.045)
def keys(ms, d):
    """soft electric-piano pad for the milky warmth"""
    t = tt(d); x = np.zeros(len(t))
    for m in ms:
        f = mtof(m); x += np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t) * np.exp(-t / 0.4)
    x *= (1 + 0.18 * np.sin(2 * np.pi * 4.6 * t))
    return x / len(ms) * np.minimum(1, t / 0.02) * np.exp(-t / 1.6) * np.clip((d - t) / 0.08, 0, 1)
def chip(m, d=0.1): return lp(pulse(mtof(m), d, 0.125), 5000) * expenv(d, 0.05)
def brass(ms, d=0.28):
    t = tt(d); x = sum(saw(mtof(m) * (1 + 0.004 * s), d) for m in ms for s in (-1, 1)) / (2 * len(ms))
    k = np.exp(-t / 0.08); x = lp(x, 3200) * k + lp(x, 900) * (1 - k)
    return x * np.minimum(1, t / 0.012) * np.exp(-t / 0.22)

KICK = kick()
# (bass root, clav voicing, pad voicing, arp notes) in E dorian
CH = {'Em9': (40, [67, 71, 74, 78], [55, 59, 62, 66], [76, 79, 83, 86]),
      'A13': (45, [67, 73, 78], [55, 61, 66], [73, 76, 81, 85]),
      'Cmaj9': (36, [64, 67, 71, 74], [52, 55, 59, 62], [72, 76, 79, 83]),
      'B7#9': (47, [63, 69, 74], [51, 57, 62], [71, 75, 78, 81])}
# 8-bar A and B phrases for variety; the last bar is the tag ending
PA = ['Em9', 'A13', 'Em9', 'A13', 'Em9', 'A13', 'Cmaj9', 'B7#9']
PB = ['Cmaj9', 'Cmaj9', 'B7#9', 'B7#9', 'Em9', 'A13', 'Cmaj9', 'B7#9']
NBARS = int(DUR / BAR)
PROG = ((PA + PA + PB + PA + PB + PA) * 2)[:NBARS - 1] + ['Em9']
BASS = [(0, 0, 2, 0), (3, 12, 1, 1), (4, 0, 1, 0), (6, 10, 1, 0), (7, 12, 1, 1), (8, 0, 2, 0),
        (10, 7, 1, 0), (11, 10, 1, 0), (12, 12, 1, 1), (14, 3, 1, 0), (15, 5, 1, 0)]
CLAV = [2, 5, 9, 13, 15]
ARP = [0, 1, 2, 3, 2, 1, 3, 2, 0, 1, 2, 3, 1, 2, 3, 0]
# sections (seconds): Kopi's chiptune sparkle during her cameo, claps + tambourine for the builder shout-out
CHIP_WIN, CLAP_WIN = [], []
import os
if os.path.exists('out/music.json'):   # written by render.mjs from the page's window.__MUSIC
    _m = json.load(open('out/music.json')); CHIP_WIN = [tuple(w) for w in _m.get('chip', [])]; CLAP_WIN = [tuple(w) for w in _m.get('claps', [])]
inwin = (lambda wins, t: any(a <= t < b for a, b in wins))

nb = len(PROG)
for b, name in enumerate(PROG):
    root, cv, pv, av = CH[name]; tb = b * BAR
    last = b == nb - 1
    if last:   # tag ending: stab on 1 and a ring-out on beat 3
        add(music, tb, KICK, 0.7); add(music, tb, brass([64, 67, 71, 74]), 0.32); add(music, tb, bass(root, BEAT * 1.2), 0.5)
        t3 = tb + 2 * BEAT
        add(music, t3, KICK, 0.6); add(music, t3, hat(True), 0.08)
        add(music, t3, brass([64, 67, 71, 74, 78], 1.4), 0.34); add(music, t3, keys(pv + [74], 1.6), 0.28)
        add(music, t3, bass(root, 1.4), 0.5); add(music, t3, hp(rng.standard_normal(int(1.5 * SR)), 5000) * expenv(1.5, 0.5), 0.07)
        break
    add(music, tb, keys(pv, BAR), 0.2)
    for s, iv, ln, pop in BASS:
        add(music, st(b, s), bass(root + iv, STEP * ln * 0.95, pop), 0.42 if pop else 0.5)
    for s in CLAV:
        add(music, st(b, s), clav(cv), 0.13, pan=-0.35)
    # drums
    for s in range(16):
        ts = st(b, s)
        if s in (0, 7, 10): add(music, ts, KICK, 0.72 if s == 0 else 0.6)
        if s in (4, 12): add(music, ts, snare(), 0.36, pan=0.05)
        if s in (9, 15): add(music, ts, snare(True), 0.07, pan=0.05)
        add(music, ts, hat(s == 14), (0.075 if s % 2 == 0 else 0.04) * (0.8 if s == 14 else 1), pan=0.3)
    for s in range(16):
        ts = st(b, s)
        if inwin(CHIP_WIN, ts): add(music, ts, chip(av[ARP[s]]), 0.05, pan=0.4 if s % 2 else -0.4)   # Kopi's chiptune sparkle
        if inwin(CLAP_WIN, ts):
            if s in (4, 12): add(music, ts, clap(), 0.22, pan=-0.1)
            add(music, ts, tamb(), 0.05 if s % 2 else 0.03, pan=0.45)
    if b % 4 == 3:    # little fill into every 4th bar
        for s in (13, 14, 15): add(music, st(b, s), snare(True), 0.12 + 0.04 * (s - 13))

music = np.stack([lp(music[:, c], 11000) for c in range(2)], axis=1)
fade = np.ones(N); fi = int(0.03 * SR); fade[:fi] = np.linspace(0, 1, fi)
fo0 = int((DUR - 0.6) * SR); fade[fo0:] = np.linspace(1, 0, N - fo0) ** 1.3
music *= fade[:, None]; music /= np.max(np.abs(music)) + 1e-9; music *= 0.55

# ---------- SFX ----------
def whoosh(d=0.4, lo=250, hi=6000):
    n = rng.standard_normal(int(d * SR)); out = np.zeros_like(n); segs = 24
    for k in range(segs):
        a, b2 = k * len(n) // segs, (k + 1) * len(n) // segs; f = lo * (hi / lo) ** (k / segs)
        out[a:b2] = bp(n[max(0, a - 400):b2], f * 0.7, min(f * 1.4, 20000))[-(b2 - a):]
    return out * np.sin(np.linspace(0, np.pi, len(n))) ** 1.5
def key():
    d = 0.03; c = hp(rng.standard_normal(int(d * SR)), 2200) * expenv(d, 0.005)
    return 0.8 * c + 0.3 * np.sin(2 * np.pi * rng.uniform(1600, 2600) * tt(d)) * expenv(d, 0.004)
def blip(f, d=0.09): return lp(pulse(f, d, 0.5), 5000) * expenv(d, 0.04)
def bell(f, d=0.6, dec=0.25): t = tt(d); return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t / 0.08)) * expenv(d, dec)
def pop(): return np.sin(2 * np.pi * phase(sweep(480, 980, 0.07), 0.07)) * expenv(0.07, 0.03)
def boing():
    d = 0.42; t = tt(d); f = 260 + 260 * np.minimum(1, t / 0.08) + 70 * np.sin(2 * np.pi * 17 * t) * np.exp(-t / 0.15)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * expenv(d, 0.16)
def buzz():
    d = 0.5; x = lp(pulse(120, d, 0.5), 1800) * 0.6 + 0.2 * bp(rng.standard_normal(int(d * SR)), 2000, 6000)
    gate = np.repeat(rng.random(int(d * 26) + 1) > 0.4, int(SR / 26) + 1)[: len(x)]
    return x * gate * np.linspace(1, 0.5, len(x))
def slurp():
    d = 0.4; n = rng.standard_normal(int(d * SR)); out = np.zeros_like(n); segs = 20
    for k in range(segs):
        a, b2 = k * len(n) // segs, (k + 1) * len(n) // segs; f = 500 + 1300 * (k / segs) + 250 * np.sin(k * 1.9)
        out[a:b2] = bp(n[max(0, a - 300):b2], f * 0.8, f * 1.25)[-(b2 - a):]
    wob = 0.55 + 0.45 * np.sin(2 * np.pi * 22 * tt(d))
    return out * wob * np.sin(np.linspace(0, np.pi, len(n)))
def sparkle():
    out = np.zeros(int(0.9 * SR))
    for k, m in enumerate([88, 91, 95, 100, 103]):
        x = bell(mtof(m), 0.4, 0.12); i = int(k * 0.055 * SR); out[i:i + len(x)] += x[: len(out) - i] * (1 - 0.1 * k)
    return out
def shutter():
    out = np.zeros(int(0.2 * SR))
    for o in (0, 0.045):
        c = bp(rng.standard_normal(int(0.03 * SR)), 1500, 9000) * expenv(0.03, 0.006); i = int(o * SR); out[i:i + len(c)] += c
    th = np.sin(2 * np.pi * 90 * tt(0.2)) * expenv(0.2, 0.03); return out + 0.4 * th
def crash(d=1.2): return hp(rng.standard_normal(int(d * SR)), 5000) * expenv(d, 0.4)
def riser(d=0.55):
    n = whoosh(d, 400, 9000) * np.linspace(0.2, 1, int(d * SR))
    s = lp(pulse(sweep(200, 900, d), d, 0.5), 3000) * np.linspace(0, 0.35, int(d * SR)); return n + s

events = json.load(open('out/events.json'))
for e in events:
    t, ty = e['t'], e['type']
    if ty == 'key': add(sfx, t, key(), rng.uniform(0.10, 0.16), pan=rng.uniform(-0.2, 0.2))
    elif ty == 'whoosh': add(sfx, t, whoosh(), 0.28 if e.get('soft') else 0.5)
    elif ty == 'swish': add(sfx, t, whoosh(0.2, 1500, 9000), 0.18)
    elif ty == 'riser': add(sfx, t, riser(), 0.3)
    elif ty == 'hit':
        g = 1.0 if e.get('big') else 0.7
        add(sfx, t, KICK, 0.7 * g); add(sfx, t, crash(), 0.1 * g); add(sfx, t, brass([64, 71, 76] if e.get('big') else [67, 74], 0.3), 0.3 * g)
    elif ty == 'blip': add(sfx, t, blip([880, 988, 1175, 1319][e.get('pitch', 0) % 4]), 0.08)
    elif ty == 'pop': add(sfx, t, pop(), 0.24)
    elif ty == 'boing': add(sfx, t, boing(), 0.16)
    elif ty == 'buzz': add(sfx, t, buzz(), 0.07)
    elif ty == 'click': add(sfx, t, key(), 0.3); add(sfx, t, blip(1500, 0.03), 0.06)
    elif ty == 'tink': add(sfx, t, bell(2637, 0.4, 0.1), 0.07)
    elif ty == 'slurp': add(sfx, t, slurp(), 0.16)
    elif ty == 'sparkle': add(sfx, t, sparkle(), 0.1)
    elif ty == 'ding': add(sfx, t, bell(1319, 0.8, 0.3), 0.09); add(sfx, t + 0.08, bell(1976, 0.7, 0.25), 0.06)
    elif ty == 'stamp':
        th = np.sin(2 * np.pi * phase(sweep(120, 48, 0.28, 0.5), 0.28)) * expenv(0.28, 0.08)
        cr = bp(rng.standard_normal(int(0.08 * SR)), 800, 5000) * expenv(0.08, 0.015); x = np.tanh(2 * th); x[:len(cr)] += 0.7 * cr
        add(sfx, t, x, 0.45)
    elif ty == 'shutter': add(sfx, t, shutter(), 0.35); add(sfx, t, brass([[64, 71], [66, 73], [67, 74], [69, 76], [71, 78]][e.get('n', 0) % 5], 0.22), 0.22)

np.save('out/music.npy', music.astype(np.float32)); np.save('out/sfx.npy', sfx.astype(np.float32))
mix = music + sfx; peak = np.max(np.abs(mix)); mix = mix / peak * 0.89
wavfile.write('out/audio.wav', SR, (mix * 32767).astype(np.int16))
print('audio ok', len(events), 'events, peak before norm', round(float(peak), 3))
