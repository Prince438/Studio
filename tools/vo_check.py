"""Pronunciation QC: transcribe each voice clip with Whisper and show the words it heard differently.
A word Whisper mishears is usually a word Kokoro mispronounced (check it, then fix tools/kd_voice.py LEXICON).

    .venv/Scripts/python tools/vo_check.py <show>/vo        (uses narration.json + clips/<id>.wav)
    .venv/Scripts/python tools/vo_check.py <show>/vo s2 s3   (only some lines)
"""
import json, os, re, sys, difflib
sys.stdout.reconfigure(encoding='utf-8')
from faster_whisper import WhisperModel
import numpy as np, soundfile as sf
from scipy.signal import resample_poly

def load16k(path):
    a, sr = sf.read(path, dtype='float32'); a = a if a.ndim == 1 else a.mean(1)
    return resample_poly(a, 16000, sr).astype(np.float32) if sr != 16000 else a

from num2words import num2words
def words(s):
    """Normalise both script and transcript: numbers to words, 2nd -> second, % -> percent, no punctuation."""
    s = s.lower().replace('’', "'").replace('%', ' percent')
    s = re.sub(r'(\d+)(st|nd|rd|th)\b', lambda m: num2words(int(m.group(1)), to='ordinal'), s)
    s = re.sub(r'\d[\d,]*(\.\d+)?', lambda m: num2words(float(m.group(0).replace(',', '')) if m.group(1) else int(m.group(0).replace(',', ''))), s)
    s = s.replace('-', ' ')
    return [{'cracked': 'kracked', 'crack': 'kracked'}.get(w, w) for w in re.findall(r"[a-z']+", s)]

vo = sys.argv[1]; only = set(sys.argv[2:])
cfg = json.load(open(os.path.join(vo, 'narration.json'), encoding='utf8'))
model = WhisperModel('small.en', device='cpu', compute_type='int8')
total = bad = 0
for ln in cfg['lines']:
    if only and ln['id'] not in only: continue
    segs, _ = model.transcribe(load16k(os.path.join(vo, 'clips', ln['id'] + '.wav')), beam_size=5, language='en')
    heard = ' '.join(s.text.strip() for s in segs)
    a, b = words(ln['text']), words(heard)
    sm = difflib.SequenceMatcher(None, a, b); diffs = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != 'equal': diffs.append(f"'{' '.join(a[i1:i2])}' -> '{' '.join(b[j1:j2])}'")
    total += len(a); bad += sum(i2 - i1 for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal')
    print(f"{ln['id']:6s} {'OK' if not diffs else 'CHECK'}  heard: {heard}")
    for d in diffs: print('         ', d)
print(f'word match: {100 * (1 - bad / max(1, total)):.1f}% of {total} words')
