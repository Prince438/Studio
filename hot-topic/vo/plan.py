"""Lay the recorded lines end to end: each line starts `gap` seconds after the previous one ends.
Writes the start times into narration.json and timeline.json (run after gen_vo.py, before wordtimes.py)."""
import json
cfg = json.load(open('narration.json', encoding='utf8')); tl = json.load(open('timeline.json', encoding='utf8'))
dur = {c['id']: c['dur'] for c in tl['clips']}; t = 0.0
for ln in cfg['lines']:
    t += ln.get('gap', 0.3); ln['start'] = round(t, 2); t += dur[ln['id']]
for c in tl['clips']: c['start'] = next(l['start'] for l in cfg['lines'] if l['id'] == c['id'])
json.dump(cfg, open('narration.json', 'w', encoding='utf8'), indent=1, ensure_ascii=False)
json.dump(tl, open('timeline.json', 'w', encoding='utf8'), indent=1, ensure_ascii=False)
for ln in cfg['lines']: print(f"{ln['id']:4s} {ln['speaker']:6s} {ln['start']:6.2f} -> {ln['start'] + dur[ln['id']]:6.2f}")
print(f'voice ends at {t:.2f}s')
