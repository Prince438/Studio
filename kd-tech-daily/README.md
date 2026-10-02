# KD Tech Daily: video template

A 62-second **16:9 (1920×1080)** tech recap, presented by **Kopi**, KD's pixel anime anchor: an original character with LED visor shades that show her expressions, a headset mic, a wrist gadget, and a hovering drone sidekick whose light flashes red on bad news.
All episodes from the DevDay special onward are 16:9; `index.html` is the 16:9 photo-mode layout.
It's built as an HTML animation and rendered to MP4.

## Make a new episode (easiest)
Attach this zip in a Claude (Cowork) chat and say:

> Make today's KD Tech Daily episode from this template. Find today's 5 biggest tech stories,
> fact-check them, update the STORIES data, date and narration, then record the voiceover,
> lip-sync Kopi, render the MP4 with music, and send it to me.

## What's inside
| File | What it does |
|---|---|
| `index.html` | The whole video: layout, doodles, Kopi's placements and the animation timeline (GSAP). Edit `STORIES` near the top for new content. |
| `anchor.js` | Kopi, the anchor: pixel-art sprite, LED-visor eyes (normal/blink/happy/worried/dollar/shocked/star), lip-sync mouth shapes, drone, wave frames and the six outfits. |
| `brand/kd_logo.png` | The KD logo with a transparent background (topbar, intro, desk, cam, lapel pin). |
| `vo/narration.json` | The spoken script: one line per scene, with start time and max length. |
| `vo/gen_vo.py` | Records each line with the open-source Kokoro voice and auto-fits its speed to the scene. Switch voices with e.g. `python3 gen_vo.py bm_george`. |
| `lipsync.py` | Turns the voice clips into per-frame mouth shapes for Kopi → `lipsync.js` |
| `render.mjs` | Renders every frame with headless Chromium and encodes it with ffmpeg → `out/video_silent.mp4` |
| `audio.py` | Synthesizes an original chiptune track and sound effects synced to the animation (+ stems). |
| `mix_vo.py` | Lays the voice over the music, ducking music and effects under speech → `out/audio_vo.wav` |
| `snap.mjs` | Grabs still frames for checking layout: `node snap.mjs 3 12.5 30` |


## Kopi v3: she moves now (from the 01.10.26 episode)
`anchor.js` now has an arms layer. Render `KOPI.svg(uid, outfit, 'base')` behind the desk and `KOPI.svg(uid, outfit, 'arms')` in front of it, then call `KOPI.update` on both.
- **Poses** (`state.pose`): rest, papers (tidies her script, uses `frame`), read, sip (KOPI mug), tablet (swipes, uses `frame`), headset (listening to the producer), tuck (hair behind her ear), point (to the story screen), pen (pen to chin), write (scribbles a note), thumb, heart (heart hands), visor (taps the LED shades), fist, wave.
- **New eyes:** down (reading), wink, heart. **New mouths:** grin, pout. `state.look` turns her head, and `state.drone` flies the drone (it parks on its desk dock at the end of the show).
- **Desk** (`newsdesk.js`): LED clock, sticker laptop, desk mic with KD flag, script papers + pen, KOPI coffee mug with steam, tablet, succulent and a drone dock. Props she picks up hide on the desk while they are in her hands.
- **Action schedule:** `ACT` in index.html lists what she does when, timed to words in her script with `WT(line, word)`. She tidies her papers between stories, sips coffee in pauses, points at the screen as each story starts, and reacts to the mood.

## Episode layout (16:9, from 01.10.26)
Intro with the rundown, then a wide studio shot: Kopi at the full desk, wall screen, city skyline, rundown card. Each story opens in the wide studio with an over-the-shoulder card, then cuts to the story package (headline, bullets, terminal, media panel with real photo or **video clip**, and Kopi's studio cam). The outro returns to the wide studio.
Video clips play as JPEG frame sequences in `clips/<name>/`. YouTube can't be downloaded, so frames were captured from the official videos in the browser and smoothed to 30 fps with ffmpeg `minterpolate`.

## Kopi's moods
Each story sets Kopi's expression in `MOODS` (index.html): `happy`, `worried`, `normal`, `dollar`, `shocked`.
Worried and shocked moods also make the antenna blink red. The mouth follows the voice automatically.

## Rules for each story
- `sign`: `'+'` for good news / launches, `'-'` for setbacks. This sets the colours.
- `lines`: 3 headline lines, each 13 characters max.
- `bullets`: 2 facts, each about 75 characters max, so each wraps to 2 lines.
- `term`: command / output / joke, each 34 characters max (the terminal shares its row with Kopi's live cam).
- If the story changes, the doodle in `ILL[i]` and its motion in `CUSTOM_S{i}` need updating too.

## Run it yourself
Needs Node 18+, Python 3 (numpy, scipy, soundfile, kokoro-onnx) and ffmpeg.
Kokoro model files go in `vo/`, from https://github.com/thewh1teagle/kokoro-onnx/releases
(`kokoro-v1.0.onnx`, `voices-v1.0.bin`).
```
npm i gsap @fontsource/jetbrains-mono @fontsource/silkscreen @fontsource/space-grotesk playwright
npx playwright install chromium
cd vo && python3 gen_vo.py && cd ..     # 1. voice
python3 lipsync.py                      # 2. mouth shapes
node render.mjs 2                       # 3. video frames
python3 audio.py && python3 mix_vo.py   # 4. music + voice mix
ffmpeg -i out/video_silent.mp4 -i out/audio_vo.wav -af "loudnorm=I=-14:TP=-1.5" -c:v copy -c:a aac -b:a 160k kd-tech-daily.mp4
```

## Kopi's wardrobe (rotate one per episode)
Set `const OUTFIT = '<id>'` in index.html (defaults to `classic`). All outfits live in `anchor.js`.
| id | Name | Look |
|---|---|---|
| classic | Classic Green Blazer | green blazer, mint tie (episode 1) |
| hoodie | Launch Hoodie | violet hoodie, drawstrings, kangaroo pocket, mint </> print (episode 2) |
| batik | Batik Blazer | teal Malaysian batik blazer, gold/aqua florals, gold tie |
| bomber | Night Shift Bomber | charcoal bomber, orange rib collar and hem, silver zip |
| varsity | Varsity K | red letterman, cream sleeves, chenille K patch |
| raid | Raid Armor | steel plates, cyan glowing core, shoulder pauldrons, HP bar |

## Layouts
- `index.html`: 16:9 photo mode. Text column left, real image top-right (with an "IMAGE: <source>" credit), Kopi's studio cam bottom-right. Put images in `img/`.
- `episodes/2026-09-30-devday-16x9.html`: the DevDay special in 16:9 (same as index.html).
- `episodes/2026-09-30-devday-vertical.html` and `episodes/2026-09-29-daily-vertical.html`: the earlier 9:16 versions (the second uses drawn doodles instead of photos).
- `render.mjs` and `snap.mjs` read the frame size from the page (`window.__W`, `window.__H`), so any layout renders at its own size.

## Company logos
Put official logo files in `logos/` and set `logo:'logos/<file>.svg'` on each story. The logo then appears in a "COMPANY" badge next to the story header and in the photo label.
Follow each company's brand guidelines: use the logo unmodified and smaller than the KD logo, never imply endorsement, and credit the trademark in the outro sources line.
OpenAI asks for permission requests via partnercomms@openai.com.

## Voiceover tips
- Spell out numbers and symbols ("one hundred fifty billion dollars", not "$150B").
- Keep each story line to about 22–26 words so it fits the 9-second window at a natural pace.
- Voices to try: af_heart (current), af_bella, am_michael, am_fenrir, bm_george, bf_emma.
