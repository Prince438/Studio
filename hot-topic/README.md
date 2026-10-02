# KD Hot Topic

One trending tech story per episode, reported **together by Kopi and Kenji** from the KD newsroom in Kuala Lumpur. They read the story and banter about it as they go.

Every episode renders in **16:9** (`index.html`) and **9:16** (`index.html?fmt=916`) from the same page, voice and timeline.

## The set (`newsroom.js`)
- A giant window onto KL at dusk, drawn as pixel art in a small canvas and scaled up:
  - Merdeka 118, the Petronas Twin Towers and Menara KL. In 9:16 the Petronas Towers stand between the anchors; in 16:9 they're in the right pane.
  - Twinkling windows, aircraft lights, a passing plane and drifting clouds.
- A big video wall behind the anchors (2 Oct: enlarged ~1.75x in 16:9, 1.3x in 9:16). It's laid out at a design size (640x360, or 800x450 in 9:16) and scaled up as one piece.
  - In 16:9 the anchors' heads cover its lower half, so card text must sit in the top band (design y < 185). In 9:16 the cards stay centred.
  - The landmarks moved to the side panes: Merdeka 118 and KL Tower on the left, the Petronas Towers on the right.
- Wall cards (`data-w` in `index.html`):
  - `title`, `ts` (company card), `jevons` (portrait card), `vs` (two-option card), `flow` (diagram), `quote`.
  - `m:<media>` shows the next media clip, so the camera can push into the wall before cutting to full screen.
- A curved anchor desk (smooth body, pixel props). Kopi sits at sprite x 0..40 and Kenji at x 64..104.
  - Kopi's props: mic, tablet, papers and pen, and the KOPI mug.
  - Kenji's props: teh tarik, RGB keyboard, mic and rubber duck.
  - Topic props in the middle: a magic 8-ball and YES/NO buzzers. Swap these for something that fits each new topic.
  - Props hide while an anchor holds them (`.d-mug`, `.d-papers`, `.d-pen`, `.d-tablet`, `.d-tea`).

## How an episode is built
1. Write the dialogue in `vo/narration.json`. Each line has a `speaker` (kopi or kenji) and a `gap` (the pause before it).
2. Record and time it:
   ```
   cd vo && ../../.venv/Scripts/python gen_vo.py && ../../.venv/Scripts/python plan.py && ../../.venv/Scripts/python wordtimes.py && cd ..
   ../.venv/Scripts/python lipsync.py <duration>
   ../.venv/Scripts/python ../tools/vo_check.py vo
   ```
   `plan.py` lays the lines end to end, so the whole show is timed from the real voice.
3. Edit `index.html`:
   - `PLAN`: what the camera shows for each line.
     - Room shots are `wide`, `two`, `kopi`, `kenji` or `wall` (plus an optional `cuts: [[word, shot]]`).
     - Full-screen media is set with `media` and `side`.
   - `MEDIA`: the clips and images used.
   - `MOMENTS`: overlays timed to words with `WT(line, word)`.
   - `HEAD`: lower-third headlines.
   - `KOPI_ACT` / `KENJI_ACT`: poses, eyes and looks timed to words.
     - Kopi sits on the left, so looking +1 is looking at Kenji. Kenji's `point` points left, at Kopi.
     - When one anchor talks, the other looks at them and nods.
4. Render and finish:
   ```
   node render.mjs 6 && FMT=916 node render.mjs 6
   ../.venv/Scripts/python audio.py && ../.venv/Scripts/python mix_vo.py
   ```
   Then `bash finish_audio.sh` (compression plus one fixed gain to -14 LUFS; don't use single-pass loudnorm, which lifts the quiet intro and end card), then `bash encode.sh kd-hot-topic_<date>`.

## Music
`audio.py` writes an original ambient synth score: Dm9 - Bbmaj7 - Fmaj7 - C6/9 at 90 BPM, with
- warm supersaw pads and a slow filter swell,
- a gentle sine sub,
- soft plucks through a ping-pong delay,
- band-passed "air" noise and a long synthetic reverb,
- a very light pulse between the intro and the outro.

The SFX come from the page's cue sheet. Check the balance by band: pads should lead, with the sub and plucks about 5 dB under.

**Mix (`mix_vo.py`, set by Prince on 2 Oct 2026):** the music is subtle and stays in harmony with the voice.
- It holds a steady bed 19 dB under the voice for the whole conversation, with no ducking pumps between lines.
- It's 14 dB under in the intro and outro, and effects are 15 dB under.
- The bed has a gentle 1-3.5 kHz dip so it leaves room for speech.
- Measured on EP.01: pauses about 16 dB under the voice, intro and end card about 9 dB under (title effects included).

## Wardrobe
This show keeps its own outfit picks, separate from Tech Daily's and Built at KD's rotations. EP.01: Kopi in the Batik Blazer (made for a KL newsroom) and Kenji in Denim + Pins.

## Episodes
- EP.01 (2 Oct 2026): The Decision Model Wars. TypeSafe's Jev, OpenAI's Decisions API, and Amazon Strands Decider and Cloudflare Clef going open source.
