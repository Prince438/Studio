"""Estimate when each word starts inside each clip (character-weighted, with extra weight for
pauses at punctuation) -> words.json  {id: [[word, t_abs], ...]}"""
import json, numpy as np, soundfile as sf
tl = json.load(open('timeline.json')); out = {}
PAUSE = {',': 3, ':': 3, ';': 3, '.': 6, '?': 6, '!': 6}
for c in tl['clips']:
    a, sr = sf.read(f"clips/{c['id']}.wav"); hop = int(sr * 0.01); n = len(a) // hop
    rms = np.sqrt((a[:n * hop].reshape(n, hop) ** 2).mean(1)); v = np.where(rms > 0.012)[0]
    s0, s1 = v[0] / 100, v[-1] / 100
    ws = c['text'].split(); wts = [len(w) + 1 + PAUSE.get(w[-1], 0) for w in ws]; tot = sum(wts); acc = 0; words = []
    for w, k in zip(ws, wts): words.append([w, round(c['start'] + s0 + (s1 - s0) * acc / tot, 2)]); acc += k
    out[c['id']] = words
json.dump(out, open('words.json', 'w'))
vo = {c['id']: [c['start'], c['dur']] for c in tl['clips']}
open('../words.js', 'w').write('window.WORDS=' + json.dumps(out) + ';\nwindow.VO=' + json.dumps(vo) + ';\n')
