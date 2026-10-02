"""Text -> Kokoro phonemes for both shows.

Kokoro was trained on misaki's phoneme set, so we convert text with misaki (dictionary first,
eSpeak only for unknown words) instead of kokoro-onnx's built-in eSpeak path. eSpeak alone gets
words like "Pentagon" wrong and reads spelled-out acronyms ("A P Is") as "uh pee iz".

Write narration as normal text: acronyms as they are written (AI, APIs, FTC, GPT-6), numbers
as digits or words. Add anything misaki gets wrong to LEXICON below (misaki phonemes: A=ay,
I=eye, O=oh, W=ow, Y=oy, T=flap t, ᵊ=light schwa; ˈ primary and ˌ secondary stress).

    python tools/kd_voice.py "some text"      -> phonemes + any words misaki had to guess
"""
import re, sys

LEXICON = {
    # people, shows, community
    'Kracked': 'kɹˈækt', 'Kopi': 'kˈOpi', 'Kenji': 'kˈɛnʤi', 'Arkedia': 'ɑɹkˈAdiə', 'Judeen': 'ʤudˈin',
    # companies and products
    'Huawei': 'wˈɑwˌA', 'Nvidia': 'ɛnvˈɪdiə', 'DeepSeek': 'dˈipsˌik', 'Devvit': 'dˈɛvɪt',
    'Shopify': 'ʃˈɑpᵻfˌI', 'Cloudflare': 'klˈWdflɛɹ', 'ElevenLabs': 'əlˈɛvᵊn lˈæbz',
    'Jev': 'ʤˈɛv', 'Jevons': 'ʤˈɛvənz', 'TypeSafe': 'tˈIpsˌAf', 'Clef': 'klˈɛf', 'Kokoro': 'kəkˈɔɹO', 'Newsom': 'nˈusəm',
    # tech terms
    'TFLOPS': 'tˈiflˌɑps', 'FLOPS': 'flˈɑps', 'GEMM': 'ʤˈɛm', 'CUDA': 'kˈudə', 'SQL': 'sˈikwəl',
    'GIF': 'ɡˈɪf', 'GUI': 'ɡˈui', 'JSON': 'ʤˈAsᵊn', 'YAML': 'jˈæməl', 'nginx': 'ˈɛnʤɪnˌɛks',
}

# phoneme-level fixes for whole phrases (applied after G2P)
PHRASES = [
    ('kɹˈækt dˈɛvz', 'kɹˈækt, dˈɛvz'),   # "Kracked Devs": a hair of a pause keeps the -ed from melting into "Devs"
]

_g2p = None
def g2p():
    global _g2p
    if _g2p is None:
        from misaki import en, espeak
        _g2p = en.G2P(trf=False, british=False, fallback=espeak.EspeakFallback(british=False))
        for w, ps in LEXICON.items():
            for k in {w, w.lower(), w.capitalize(), w.upper()}: _g2p.lexicon.golds[k] = ps
    return _g2p

def phonemize(text):
    """Return Kokoro phonemes for a line of narration."""
    ps, _ = g2p()(text)
    for a, b in PHRASES: ps = ps.replace(a, b)
    return ps

def guessed(text):
    """Words misaki could not find in its dictionaries (so eSpeak guessed them): worth a listen."""
    _, toks = g2p()(text); lx = g2p().lexicon; out = []
    for t in toks:
        w = t.text
        if not re.search(r'[A-Za-z]', w) or re.fullmatch(r"[\d$%.,'-]+", w): continue
        forms = {w, w.lower(), w.capitalize(), re.sub(r"('s|s)$", '', w).lower(), re.sub(r'ies$', 'y', w).lower(), re.sub(r'(ed|ing)$', '', w).lower()}
        if not any(k in lx.golds or k in lx.silvers for k in forms):
            out.append((w, t.phonemes))
    return out

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    text = ' '.join(sys.argv[1:]) or 'Good morning, Kracked Devs! The Pentagon, APIs, AI and 431 TFLOPS.'
    print(phonemize(text))
    for w, ps in guessed(text): print(f'  guessed: {w:16s} {ps}')
