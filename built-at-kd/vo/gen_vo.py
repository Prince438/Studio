"""Generate one VO clip per scene with Kokoro, auto-adjusting speed so each fits its window.
Each line has a speaker; voices and base speeds are set per speaker in narration.json.
Text goes through tools/kd_voice.py (misaki + KD lexicon) so names and acronyms are pronounced properly.
usage: .venv/Scripts/python gen_vo.py [id ...]   -> clips/<id>.wav + timeline.json
(with ids, only those lines are re-recorded; the others keep their existing clips)"""
import json, sys, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools'))
import kd_voice
sys.stdout.reconfigure(encoding='utf-8')

cfg = json.load(open('narration.json'))
k = Kokoro('kokoro-v1.0.onnx', 'voices-v1.0.bin')
os.makedirs('clips', exist_ok=True)

def trim(a, sr, thr=0.01, pad=0.03):
    idx = np.where(np.abs(a) > thr)[0]
    if not len(idx): return a
    s, e = max(0, idx[0] - int(pad * sr)), min(len(a), idx[-1] + int(pad * sr))
    return a[s:e]

ONLY = set(sys.argv[1:])
old = {c['id']: c for c in json.load(open('timeline.json'))['clips']} if ONLY and os.path.exists('timeline.json') else {}
out = []
for ln in cfg['lines']:
    if ONLY and ln['id'] not in ONLY and ln['id'] in old:
        c = dict(old[ln['id']]); c['start'] = ln['start']; out.append(c); continue
    ps = kd_voice.phonemize(ln['text'])
    def synth(sp):
        a, sr = k.create(ps, voice=cfg['voices'][ln['speaker']], speed=sp, is_phonemes=True); a = trim(a, sr); return a, sr, len(a) / sr
    speed = cfg['base_speed'][ln['speaker']]; a, sr, dur = synth(speed)
    if dur > ln['max']:                      # binary-search the gentlest speed that fits
        lo, hi, best = speed, 1.4, None
        for _ in range(5):
            mid = (lo + hi) / 2; r = synth(mid)
            if r[2] <= ln['max']: best, hi = (mid, r), mid
            else: lo = mid
        if best: speed, (a, sr, dur) = best[0], best[1]
    sf.write(f"clips/{ln['id']}.wav", a, sr)
    out.append({'id': ln['id'], 'speaker': ln['speaker'], 'start': ln['start'], 'dur': round(dur, 2), 'speed': round(speed, 3), 'sr': sr, 'text': ln['text']})
    flag = '' if dur <= ln['max'] else '  <-- OVER'
    print(f"{ln['id']:7s} start {ln['start']:5.2f}  dur {dur:5.2f}/{ln['max']:.1f}  speed {speed:.2f}  wps {len(ln['text'].split())/dur:.2f}{flag}")
    for w, p in kd_voice.guessed(ln['text']): print(f"          guessed: {w} /{p}/  (add to tools/kd_voice.py LEXICON if it sounds wrong)")
json.dump({'voices': cfg['voices'], 'clips': out}, open('timeline.json', 'w'), indent=1)
