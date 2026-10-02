"""KD Hot Topic mix: voice on top, the ambient score as a steady, subtle bed -> out/audio_vo.wav

Unlike the Tech Daily mix (which ducks the music between every line), the bed here holds one level for the whole
conversation, so the pads never swell up in the short gaps between Kopi and Kenji. Levels are set relative to the voice:
  BED_UNDER_VO_DB  how far the music sits under the voice while they talk (subtle, but audible)
  OPEN_UNDER_VO_DB the music level in the intro / outro, when nobody is talking (still well under voice level)
The bed also gets a gentle dip around 1-3.5 kHz, where speech is clearest, so the two never fight.
Prints the measured voice-vs-music gap at the end."""
import json, numpy as np, soundfile as sf
from scipy.signal import resample_poly, butter, sosfilt
from scipy.ndimage import uniform_filter1d

SR = 44100
BED_UNDER_VO_DB, OPEN_UNDER_VO_DB, SFX_UNDER_VO_DB = 19.0, 14.0, 15.0
music = np.load('out/music.npy'); sfx = np.load('out/sfx.npy'); N = len(music)
tl = json.load(open('vo/timeline.json', encoding='utf8'))

# --- voice track: resample 24k -> 44.1k, clean low end, gentle compression ---
vo = np.zeros(N); hp = butter(2, 90, 'high', fs=SR, output='sos')
for c in tl['clips']:
    a, sr = sf.read(f"vo/clips/{c['id']}.wav")
    a = resample_poly(a, 147, 80) if sr == 24000 else a
    a = sosfilt(hp, a); a = np.sign(a) * (np.abs(a) ** 0.85)
    i = int(c['start'] * SR); vo[i:i + len(a)] += a[: N - i]

def rms(x, m=None):
    x = x if m is None else x[m > 0.5]
    return np.sqrt(np.mean(x ** 2) + 1e-12)
db = lambda v: 10 ** (v / 20)

# --- where the conversation runs: one smooth region, not a mask per line ---
starts = [c['start'] for c in tl['clips']]; ends = [c['start'] + c['dur'] for c in tl['clips']]
a, b = int((min(starts) - 0.6) * SR), int((max(ends) + 0.5) * SR)
region = np.zeros(N); region[max(0, a):min(N, b)] = 1
region = uniform_filter1d(region, int(1.5 * SR), mode='nearest')

# --- carve a little space for speech in the bed (about -5 dB around 1-3.5 kHz) ---
bp = butter(2, [1000, 3500], 'band', fs=SR, output='sos')
music = music - 0.45 * np.stack([sosfilt(bp, music[:, c]) for c in range(2)], 1)

# --- levels, all relative to the voice ---
speech = uniform_filter1d((np.abs(vo) > 1e-4).astype(float), 2205, mode='nearest')
vo_level = rms(vo, speech)
m_mono = music.mean(1)
g_talk = vo_level * db(-BED_UNDER_VO_DB) / rms(m_mono, region)
g_open = vo_level * db(-OPEN_UNDER_VO_DB) / rms(m_mono, 1 - region)
gain = g_talk * region + g_open * (1 - region)
bed_music = music * gain[:, None]
s_mono = sfx.mean(1); s_act = uniform_filter1d((np.abs(s_mono) > 0.02 * np.abs(s_mono).max()).astype(float), 441, mode='nearest')
g_sfx = vo_level * db(-SFX_UNDER_VO_DB) / rms(s_mono, s_act)
duck = db(-4.0 * np.clip(speech * 1.5, 0, 1))                     # sound effects step back a little under the voice
bed_sfx = sfx * (g_sfx * duck)[:, None]

mix = bed_music + bed_sfx + vo[:, None]
mix /= np.max(np.abs(mix)) / 0.95
sf.write('out/audio_vo.wav', mix.astype(np.float32), SR, subtype='FLOAT')
talk = (region > 0.99) & (speech > 0.5)
gap = 20 * np.log10(rms(vo, talk.astype(float)) / rms(bed_music.mean(1), talk.astype(float)))
print(f"music under voice while talking: {gap:.1f} dB; intro/outro music {OPEN_UNDER_VO_DB} dB under voice level; sfx {SFX_UNDER_VO_DB} dB under")
