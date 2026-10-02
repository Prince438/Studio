"""Synthesize an original 120 BPM chiptune bed + SFX synced to out/events.json -> out/audio.wav"""
import json, numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

import os as _os
_M = json.load(open('out/music.json')) if _os.path.exists('out/music.json') else {}
SR = 44100; DUR = _M.get('dur', 62.0); N = int(SR * DUR)
BPM = 120; BEAT = 60 / BPM; STEP = BEAT / 4; BAR = BEAT * 4
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

# ---------- instruments ----------
def kick_():
    x = sine_sweep(160, 42, 0.38, 0.35) * expenv(0.38, 0.13)
    c = hp(rng.standard_normal(len(x)), 2500) * expenv(0.38, 0.004)
    return np.tanh(1.6 * x) + 0.25 * c
def snare():
    n = bp(rng.standard_normal(int(0.22 * SR)), 1500, 7000) * expenv(0.22, 0.06)
    tone = np.sin(2 * np.pi * 190 * tt(0.22)) * expenv(0.22, 0.03)
    return 0.8 * n + 0.5 * tone
def hat(open_=False):
    d = 0.25 if open_ else 0.05
    return hp(rng.standard_normal(int(d * SR)), 7500) * expenv(d, 0.07 if open_ else 0.014)
def bass(m, d):
    x = lp(pulse(mtof(m), d, 0.25), 900) * expenv(d, 0.18, 0.004)
    return x
def arp(m, d=0.12):
    x = lp(pulse(mtof(m), d, 0.125), 3200) * expenv(d, 0.06)
    return x
def pad(ms, d):
    t = tt(d); x = np.zeros(len(t))
    for m in ms:
        for det in (-0.08, 0.0, 0.08):
            f = mtof(m + det); x += 2 * ((t * f) % 1) - 1
    x = lp(x / (len(ms) * 3), 1400, 2)
    env = np.minimum(1, t / 0.25) * np.minimum(1, (d - t) / 0.3).clip(0, 1)
    return x * env

KICK = kick_()
CH = [  # (bass root midi, pad notes, arp notes)
    (45, [57, 60, 64], [69, 72, 76, 81]),   # Am
    (41, [57, 60, 65], [65, 69, 72, 77]),   # F
    (48, [55, 60, 64], [72, 76, 79, 84]),   # C
    (43, [55, 59, 62], [67, 71, 74, 79]),   # G
]
ARP_PAT = [0, 1, 2, 3, 2, 1, 0, 1, 0, 2, 3, 2, 1, 2, 3, 1]
BASS_PAT = [0, None, 12, 0, None, 0, 12, None, 0, None, 12, 0, None, 7, 12, None]
# song map from the page (window.__MUSIC via render.mjs): intro length, outro start, scene cuts to fill into
INTRO_BARS = max(1, int(_M.get('intro', 6.0) / BAR)); OUTRO_BAR = int(_M.get('outro', 56.0) / BAR)
CUTS = _M.get('cuts', [16, 26, 36, 46, 56])
infill = lambda ts: any(c - 1.0 <= ts < c for c in CUTS)      # 1-second snare fill into every scene cut

nbars = int(DUR / BAR)
for b in range(nbars):
    t_bar = b * BAR
    root, padn, arpn = CH[b % 4]
    intro = b < INTRO_BARS; outro = b >= OUTRO_BAR
    # pad
    add(music, t_bar, pad(padn, BAR + 0.25), 0.16 if not outro else 0.2)
    # arp (filtered open during intro)
    for s in range(16):
        g = 0.10
        if intro: g *= 0.35 + 0.65 * (b * 16 + s) / (INTRO_BARS * 16)
        if outro and b == nbars - 1: g *= max(0, 1 - s / 16)
        add(music, t_bar + s * STEP, arp(arpn[ARP_PAT[s]]), g, pan=0.35 if s % 2 else -0.35)
        # echo
        add(music, t_bar + s * STEP + 3 * STEP, arp(arpn[ARP_PAT[s]]) , g * 0.3, pan=-0.5 if s % 2 else 0.5)
    if b == 0: continue
    # bass
    if b <= nbars - 2:
        for s, iv in enumerate(BASS_PAT):
            if iv is None: continue
            if outro and s % 4: continue
            add(music, t_bar + s * STEP, bass(root - 12 + iv + 12, STEP * 1.8), 0.22)
    if intro:  # hats build, then a kick lift in the last intro bar
        for s in range(0, 16, 2): add(music, t_bar + s * STEP, hat(), 0.06 + 0.004 * s, pan=0.2)
        if b == INTRO_BARS - 1:
            for s in (0, 8): add(music, t_bar + s * STEP, KICK, 0.5)
            for s in range(12, 16): add(music, t_bar + s * STEP, snare(), 0.1 + 0.04 * (s - 12))
        continue
    if outro:
        if b <= nbars - 2: add(music, t_bar, KICK, 0.55)
        continue
    # drums
    for s in range(16):
        ts = t_bar + s * STEP; fill = infill(ts)
        if s in (0, 8) or (s == 10 and b % 2) or (s == 7 and b % 4 == 3):
            if not fill: add(music, ts, KICK, 0.62)
        if s in (4, 12) and not fill: add(music, ts, snare(), 0.3, pan=0.05)
        if fill: k = min(8, int((ts - max(c for c in CUTS if c > ts) + 1.0) / STEP)); add(music, ts, snare(), 0.12 + 0.03 * k, pan=0.05)
        if s % 2 == 0 and not fill: add(music, ts, hat(s in (6, 14)), 0.07 if s % 4 else 0.05, pan=0.25)
    add(music, t_bar + 3 * STEP, hat(), 0.03, pan=-0.3)

# gentle bus: lowpass shimmer, fade in/out
music = np.stack([lp(music[:, c], 9000) for c in range(2)], axis=1)
fade = np.ones(N); fi = int(0.05 * SR); fade[:fi] = np.linspace(0, 1, fi)
fo0 = int((DUR - 2.2) * SR); fade[fo0:] = np.linspace(1, 0, N - fo0) ** 1.5
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
