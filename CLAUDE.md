# KD Studio

Prince's KrackedDevs (KD) video shows, made as HTML/GSAP animations and rendered to MP4.
- `kd-tech-daily/`: daily tech news, anchored by Kopi. `index.html` is always the latest episode; earlier ones are in `episodes/`.
- `built-at-kd/`: community project showcase, hosted by Kenji Neo.
- `hot-topic/`: KD Hot Topic (working title), a deep dive on today's trending tech topic.
  - Kopi and Kenji co-anchor from a KL newsroom and cut to full-screen media.
  - See `hot-topic/README.md` and HANDOFF §3b.

**Every video ships twice: 16:9 (1920x1080) and 9:16 (1080x1920).** For Tech Daily, `index.html?fmt=916` is the vertical layout of the same episode. Render it with `FMT=916 node render.mjs 6` (writes to `out-916/`) and mux it with the same `out/audio_final.wav`.

**Read `HANDOFF.md` before any episode work.** It holds the standing rules, characters, outfit rotation, layouts, pipeline and backlog. Keep its episode log and backlog (§2.1, §3.3, §9) up to date after each episode.

## This machine (Windows, migrated from the Cowork sandbox on 1 Oct 2026)
- Python: use the project venv `.venv/Scripts/python` (kokoro-onnx, numpy, scipy, soundfile, pillow, opencv-python-headless). There is no `python3`.
- Kokoro models live in `models/` and are hard-linked into each show's `vo/`.
- Node 24 with Playwright Chromium. `render.mjs` and `snap.mjs` load the page through `pathToFileURL`; set `PAGE=episodes/x.html` to render another page.
- ffmpeg 8.1 is on PATH. In the two-pass encode, pass 1 writes to `NUL`.
- Network: the PC shell reaches YouTube, GitHub, company CDNs, Hugging Face and Wikimedia Commons, so official press media can be fetched directly with curl. `.mil` and `defense.gov` block scripts; use Wikimedia Commons copies of public-domain DoD photos instead.
- There is no 20 MB file-transfer limit here. Finished videos go straight to `Downloads/KD-Tech-Daily` or `Downloads/Built-at-KD`.
- Voice: both `gen_vo.py` scripts send text through `tools/kd_voice.py`, which uses misaki (Kokoro's own converter) plus a KD dictionary, and pass phonemes to Kokoro.
  - Don't use kokoro-onnx's built-in eSpeak path. It mispronounced "Pentagon" and read "A P Is" as "uh pee iz".
  - Write acronyms normally (AI, APIs) and put fixes in `LEXICON`/`PHRASES`, not in the script text. `python tools/kd_voice.py "text"` shows phonemes and any guessed words.
  - After recording, run `.venv/Scripts/python tools/vo_check.py <show>/vo` (Whisper transcription diff) and check every flagged word.

## Per-episode media workflow (tech daily)
`research/raw-<date>/` holds downloaded sources. A `research/prep_<date>.py` script turns them into `img/*.jpg` (1600x900), `clips/<name>/####.jpg` (30 fps) and white logos in `logos/`. A `research/ep_<date>_patch.py` script swaps the page content. Check stills with `node snap.mjs ...` and `.venv/Scripts/python research/sheet.py snaps out.jpg` before rendering.
