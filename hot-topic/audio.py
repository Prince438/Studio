"""KD Hot Topic: original ambient synth score (Dm9-Bbmaj7-Fmaj7-C6/9, 90 BPM) + SFX synced to out/events.json -> out/audio.wav"""
import json, numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

import os as _os
_M = json.load(open('out/music.json')) if _os.path.exists('out/music.json') else {}
SR = 44100; DUR = _M.get('dur', 62.0); N = int(SR * DUR)
BPM = 104; BEAT = 60 / BPM; STEP = BEAT / 4; BAR = BEAT * 4
rng = np.random.default_rng(7)
music = np.zeros((N, 2)); sfx = np.zeros((N, 2))

def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def tt(d): return np.arange(int(d * SR)) / SR
def expenv(d, dec, att=0.002):
    t = tt(d); return np.minimum(1, t / att) * np.exp(-t / dec)
def pulse(freq, d, duty=0.5):
    ph = np.cumsum(np.full(int(d * SR), freq) if np.isscalar(freq) else freq) / SR
    return np.where((ph % 1) < duty, 1.0, -1.0)
def sweep(f0, f1, d):
    return np.linspace(f0, f1, int(d * SR))
def sine_sweep(f0, f1, d, curve=1.0):
    k = np.linspace(0, 1, int(d * SR)) ** curve
    f = f0 + (f1 - f0) * k
    return np.sin(2 * np.pi * np.cumsum(f) / SR)
def add(buf, t, x, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N or i + len(x) <= 0: return
    x = x[: N - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[i:i + len(x), 0] += x * gain * l * 1.414
    buf[i:i + len(x), 1] += x * gain * r * 1.414

# ---------- ambient synth score ----------
# Dm9 - Bbmaj7 - Fmaj7 - C6/9, two bars each at 90 BPM: warm supersaw pads, a sine sub, soft delayed plucks,
# airy noise and a very light pulse, all through a long synthetic reverb. Ducked under the voice by mix_vo.py.
from scipy.signal import fftconvolve
BPM = 90; BEAT = 60 / BPM; BAR = BEAT * 4; SEG = BAR * 2
CHORDS = [(38, [62, 65, 69, 72, 76]), (34, [58, 62, 65, 69, 74]), (41, [60, 64, 65, 69, 72]), (36, [60, 62, 64, 67, 69])]
INTRO = _M.get('intro', 3.5); OUTRO = _M.get('outro', DUR - 6)

def saw(f, n, ph):
    return 2 * ((np.arange(n) * f / SR + ph) % 1) - 1
def env_ar(n, att, rel):
    t = np.arange(n) / SR; d = n / SR
    return np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1)

KICK = sine_sweep(120, 44, 0.5, 0.4) * expenv(0.5, 0.16)       # also used by the SFX 'hit'
pad = np.zeros((N, 2)); sub = np.zeros(N); pl = np.zeros((N, 2)); air = np.zeros((N, 2)); pulse_ = np.zeros((N, 2))
nseg = int(np.ceil(DUR / SEG)) + 1
for k in range(nseg):
    t0 = k * SEG - 0.6; root, notes = CHORDS[k % 4]; n = int((SEG + 2.2) * SR); i0 = int(t0 * SR)
    seg = np.zeros((n, 2))
    for j, m in enumerate(notes):
        f = mtof(m)
        for d, pan in ((-0.09, -0.7), (-0.04, -0.3), (0.0, 0.0), (0.05, 0.35), (0.1, 0.7)):
            v = saw(f * 2 ** (d / 12), n, rng.random()) * (0.6 if j == 0 else 0.45)
            seg[:, 0] += v * np.cos((pan + 1) * np.pi / 4); seg[:, 1] += v * np.sin((pan + 1) * np.pi / 4)
    e = env_ar(n, 1.4, 2.0)[:, None]
    dark = np.stack([lp(seg[:, c], 650, 2) for c in range(2)], 1); bright = np.stack([lp(seg[:, c], 2300, 2) for c in range(2)], 1)
    tt_ = (np.arange(n) / SR + t0); w = (0.5 + 0.5 * np.sin(2 * np.pi * tt_ / 9.0))[:, None] * 0.6
    seg = (dark * (1 - w) + bright * w) * e / 18
    a0, a1 = max(0, i0), min(N, i0 + n)
    if a1 <= a0: continue
    seg = seg[a0 - i0: a1 - i0]; pad[a0:a1] += seg
    # sine sub (root two octaves down, plus a soft octave)
    ns = a1 - a0; ts = np.arange(ns) / SR
    s1 = (np.sin(2 * np.pi * mtof(root) * ts) + 0.3 * np.sin(4 * np.pi * mtof(root) * ts)) * env_ar(ns, 0.5, 1.6)
    sub[a0:a1] += s1 * 0.5
    # plucks: chord tones an octave up on 8th notes, sparse during the intro
    up = [m + 12 for m in notes]; pat = [0, 2, 4, 1, 3, 2, 4, 3]
    for q in range(16):
        tq = k * SEG + q * BEAT / 2
        if tq >= DUR or tq < 0: continue
        if tq < INTRO + 4 and q % 2: continue
        f = mtof(up[pat[q % 8]]); d = 0.9; tn = np.arange(int(d * SR)) / SR
        x = (0.7 * np.sin(2 * np.pi * f * tn) + 0.3 * (2 * np.abs(2 * ((tn * f) % 1) - 1) - 1)) * np.exp(-tn / 0.28) * np.minimum(1, tn / 0.004)
        add(pl, tq, x, 0.07, pan=-0.45 if q % 2 else 0.45)
# ping-pong dotted-eighth delay on the plucks
dly = int(BEAT * 0.75 * SR); fb = 0.38; out = pl.copy(); tap = pl.copy()
for r_ in range(5):
    tap = np.roll(tap[:, ::-1], dly, axis=0) * fb; tap[:dly] = 0; out += np.stack([lp(tap[:, c], 2600) for c in range(2)], 1)
pl = out
# air: band-passed noise breathing slowly
nz = rng.standard_normal((N, 2)); air = np.stack([bp(nz[:, c], 2500, 7500) for c in range(2)], 1) * (0.012 + 0.01 * np.sin(2 * np.pi * np.arange(N) / SR / 13))[:, None]
# a very light pulse (soft kick on 1 and 3, shaker on the off-beats) between the intro and the outro
t = INTRO
while t < OUTRO:
    b = int(round((t - INTRO) / BEAT))
    if b % 2 == 0: add(pulse_, t, KICK, 0.18)
    add(pulse_, t + BEAT / 2, hp(rng.standard_normal(int(0.05 * SR)), 6000) * expenv(0.05, 0.012), 0.025, pan=0.3)
    t += BEAT
# long synthetic reverb on pads + plucks
ir_n = int(3.2 * SR); tir = np.arange(ir_n) / SR
ir = np.stack([lp(rng.standard_normal(ir_n), 5000) * np.exp(-tir / 0.9) for _ in range(2)], 1); ir /= np.sqrt((ir ** 2).sum(0))
wet_in = pad + pl * 0.8
wet = np.stack([fftconvolve(wet_in[:, c], ir[:, c])[:N] for c in range(2)], 1)
sub = lp(sub, 140)
music = pad * 1.0 + wet * 0.85 + pl * 0.7 + sub[:, None] * 0.12 + air * 1.4 + pulse_ * 0.7
music = np.stack([hp(music[:, c], 32) for c in range(2)], 1)

# bus: gentle fade in/out, normalise
fade = np.ones(N); fi = int(1.0 * SR); fade[:fi] = np.linspace(0, 1, fi) ** 2
fo0 = int((DUR - 3.0) * SR); fade[fo0:] = np.linspace(1, 0, N - fo0) ** 1.5
music *= fade[:, None]
music /= np.max(np.abs(music)) + 1e-9; music *= 0.55

# ---------- SFX ----------
def whoosh(d=0.42, lo=250, hi=5000):
    n = rng.standard_normal(int(d * SR)); out = np.zeros_like(n)
    segs = 24
    for k in range(segs):
        a, b2 = k * len(n) // segs, (k + 1) * len(n) // segs
        f = lo * (hi / lo) ** (k / segs)
        out[a:b2] = bp(n[max(0, a - 400):b2], f * 0.7, min(f * 1.4, 20000))[-(b2 - a):]
    env = np.sin(np.linspace(0, np.pi, len(n))) ** 1.5
    return out * env
def key():
    d = 0.03; c = hp(rng.standard_normal(int(d * SR)), 2200) * expenv(d, 0.005)
    tone = np.sin(2 * np.pi * rng.uniform(1600, 2600) * tt(d)) * expenv(d, 0.004)
    return 0.8 * c + 0.3 * tone
def blip(f, d=0.09): return lp(pulse(f, d, 0.5), 5000) * expenv(d, 0.04)
def zip_(): return lp(pulse(sweep(380, 1300, 0.14), 0.14, 0.3), 4000) * expenv(0.14, 0.07)
def stamp():
    th = sine_sweep(110, 45, 0.3, 0.5) * expenv(0.3, 0.09)
    cr = bp(rng.standard_normal(int(0.08 * SR)), 800, 5000) * expenv(0.08, 0.015)
    out = np.tanh(2 * th); out[:len(cr)] += 0.7 * cr; return out
def crash(d=1.4): return hp(rng.standard_normal(int(d * SR)), 5000) * expenv(d, 0.45)
def riser(d=0.5):
    n = whoosh(d, 400, 9000) * np.linspace(0.2, 1, int(d * SR))
    s = lp(pulse(sweep(200, 900, d), d, 0.5), 3000) * np.linspace(0, 0.35, int(d * SR))
    return n + s

events = json.load(open('out/events.json'))
for e in events:
    t, ty = e['t'], e['type']
    if ty == 'key':    add(sfx, t, key(), rng.uniform(0.10, 0.16), pan=rng.uniform(-0.2, 0.2))
    elif ty == 'whoosh': add(sfx, t, whoosh(), 0.5)
    elif ty == 'swish':  add(sfx, t, whoosh(0.2, 1500, 9000), 0.18)
    elif ty == 'riser':  add(sfx, t, riser(), 0.35)
    elif ty == 'hit':    add(sfx, t, KICK, 0.8); add(sfx, t, crash(), 0.12); add(sfx, t, np.sin(2*np.pi*55*tt(0.6))*expenv(0.6,0.25), 0.4)
    elif ty == 'hl':     add(sfx, t, zip_(), 0.09)
    elif ty == 'blip':   add(sfx, t, blip([880, 1175, 988, 1319][e.get('pitch', 0) % 4]), 0.05 if e.get('soft') else 0.08)
    elif ty == 'coin':   add(sfx, t, blip(1319, 0.07), 0.1); add(sfx, t + 0.07, blip(1976, 0.18), 0.1)
    elif ty == 'stamp':  add(sfx, t, stamp(), 0.55)
    elif ty == 'pop':    add(sfx, t, np.sin(2*np.pi*np.cumsum(sweep(500, 950, 0.07))/SR)*expenv(0.07,0.03), 0.22)
    elif ty == 'ok':     add(sfx, t, blip(988, 0.07), 0.08); add(sfx, t + 0.075, blip(1319, 0.1), 0.08)
    elif ty == 'err':    add(sfx, t, lp(pulse(330, 0.1, 0.2), 2500)*expenv(0.1,0.08), 0.1); add(sfx, t + 0.11, lp(pulse(247, 0.16, 0.2), 2500)*expenv(0.16,0.1), 0.1)
    elif ty == 'click':  add(sfx, t, key(), 0.3); add(sfx, t, blip(1500, 0.03), 0.06)
    elif ty == 'count':
        for k in range(22): add(sfx, t + k * 0.055, blip(700 + 28 * k, 0.03), 0.045)

np.save('out/music.npy', music.astype(np.float32)); np.save('out/sfx.npy', sfx.astype(np.float32))
mix = music + sfx
peak = np.max(np.abs(mix)); mix = mix / peak * 0.89   # ~ -1 dBFS
wavfile.write('out/audio.wav', SR, (mix * 32767).astype(np.int16))
print('audio ok', len(events), 'events, peak before norm', round(float(peak), 3))
