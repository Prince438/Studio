"""Mix voiceover over the music + SFX stems, ducking the bed under the voice -> out/audio_vo.wav"""
import json, numpy as np, soundfile as sf
from scipy.signal import resample_poly, butter, sosfilt

SR = 44100
music = np.load('out/music.npy'); sfx = np.load('out/sfx.npy'); N = len(music)
tl = json.load(open('vo/timeline.json'))

# --- voice track: resample 24k -> 44.1k, clean low end, gentle compression ---
vo = np.zeros(N)
hp = butter(2, 90, 'high', fs=SR, output='sos')
for c in tl['clips']:
    a, sr = sf.read(f"vo/clips/{c['id']}.wav")
    a = resample_poly(a, 147, 80) if sr == 24000 else a
    a = sosfilt(hp, a)
    a = np.sign(a) * (np.abs(a) ** 0.85)          # soft upward compression for consistent level
    i = int(c['start'] * SR); vo[i:i + len(a)] += a[: N - i]

# --- duck mask from known clip windows (smooth 120ms ramps) ---
mask = np.zeros(N)
for c in tl['clips']:
    a, b = int((c['start'] - 0.08) * SR), int((c['start'] + c['dur'] + 0.12) * SR)
    mask[max(0, a):min(N, b)] = 1
ramp = int(0.12 * SR); k = np.ones(ramp) / ramp
mask = np.convolve(mask, k, mode='same')

def rms(x, m=None):
    x = x if m is None else x[m > 0.99]
    return np.sqrt(np.mean(x ** 2) + 1e-12)

MUSIC_DUCK_DB, SFX_DUCK_DB, VO_OVER_BED_DB = -10.0, -5.0, 10.0
music_g = 10 ** (MUSIC_DUCK_DB * mask / 20)
sfx_g = 10 ** (SFX_DUCK_DB * mask / 20)
bed = music * music_g[:, None] + sfx * sfx_g[:, None]

# set voice level: VO_OVER_BED_DB above the ducked bed where the voice is active
act = (np.abs(vo) > 1e-4).astype(float); act = np.convolve(act, np.ones(2205) / 2205, mode='same')
vo_gain = rms(bed.mean(axis=1), mask) * 10 ** (VO_OVER_BED_DB / 20) / rms(vo, act)
vo *= vo_gain
mix = bed + vo[:, None] * np.array([1.0, 1.0])
mix /= np.max(np.abs(mix)) / 0.95
sf.write('out/audio_vo.wav', mix.astype(np.float32), SR, subtype='FLOAT')
print(f"vo gain {vo_gain:.2f}; voice-over-bed {VO_OVER_BED_DB} dB; music duck {MUSIC_DUCK_DB} dB")
