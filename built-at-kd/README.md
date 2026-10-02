# Built at KD: video template

A **16:9 (1920×1080)** show that breaks down projects made by KrackedDevs community members.
It's hosted by **Kenji Neo**, an original pixel anime host with messy lime-tipped hair, smart glasses, neck headphones and a glass of teh tarik.
Once per episode **Kopi**, the KD Tech Daily anchor, drops in, has a look, gives one compliment and leaves.

It's built as an HTML animation and rendered to MP4, using the same pipeline as KD Tech Daily.

## Make an episode (easiest)
Attach this zip in a Claude (Cowork) chat, then send the project link and the maker's demo videos. Say:

> Make a Built at KD episode from this template about <project link>. Go through the site for the info,
> use my videos for the demo and B-roll, give Kopi a new compliment (check compliments.json),
> rotate Kenji's outfit, then voice, lip-sync, render and send me the MP4 with a caption.

## The look
- **Set:** milky cream wall with drifting pastel blobs (mint, lilac, butter, peach, sky), milk drips, halftone and squiggles, with chunky ink outlines and offset shadows. It keeps KD's green pixel logo, neon and terminal touches.
- **Desk:** graphite with a mint LED edge, a scrolling LED marquee, speaker grills, stripes and a checker band.
  - Props on the desk: an RGB keyboard, a laptop covered in stickers, an RGB cube lamp, teh tarik, a rubber debug duck and a plant.
- **Fonts:** Bungee (titles), Silkscreen (pixel labels), Space Grotesk (body).

## Kenji Neo
- **Voice:** Kokoro `am_puck` at speed 1.1. `am_fenrir` and `am_michael` are the alternates; switch voices in `vo/narration.json`.
- **"Alive" poses** (`kenji.js`), scheduled in `SCHED` in index.html:
  - `rest`, `type` (typing), `sip` (teh tarik), `glasses` (pushes them up), `thumb`, `point` (points to his right, toward the wall screen), `stretch` (yawn), `wave`.
  - Between poses he nods to the beat and blinks.
- **Faces:**
  - Eyes: normal, blink, happy, wide, wink.
  - Brows: normal, up, focus.
  - Mouth: follows the voice automatically.
- **Wardrobe:** one outfit per episode, set with `const OUTFIT` in index.html.

| id | Name | Look |
|---|---|---|
| overshirt | Studio Overshirt | olive overshirt over a white KD tee (EP.00) |
| windbreaker | Retro Windbreaker | mint two-tone windbreaker, cream band, violet stripe |
| blackout | Blackout Hoodie | black hoodie, lime drawstrings, lightning print, silver chain |
| denim | Denim + Pins | denim jacket with enamel pins over a white tee |
| techwear | Techwear Vest | black strap vest over a grey long-sleeve, orange tag |

## Kopi's cameo
- She slides in, her visor eyes turn to stars, she says her line in a speech bubble (voice `af_heart`), waves and slides out. A "SPECIAL GUEST" lower third runs during the visit.
- **Never reuse a compliment.** Every compliment used so far is in `compliments.json`. Check it before writing a new one, then add the new one.

## Episode structure (style test timings)
| Scene | What happens |
|---|---|
| Intro | "BUILT AT KD" title slams in and Kenji pops up to wave |
| Studio | Kenji at the desk, with the wall screen, neon sign and ON AIR light |
| Project segment | the demo video panel, a project card (name, maker, demo / stack / story), Kenji's picture-in-picture cam and a B-roll film strip |
| Studio + cameo | Kopi drops in |
| Fit check | Kenji's outfit cards (only in the style test) |
| End card | Learn. Build. Ship. |

For real episodes, the placeholder panels get the maker's footage.
Chromium can't play H.264, so first turn each clip into frames with ffmpeg, then show them frame-accurately.


## Before every episode: material checklist
Ask for anything missing before building:
1. **Project site link**: gone through for the facts on the info cards.
2. **Creator's name and handle.**
3. **Demo videos**: screen recordings of the project, used for the demo panel and B-roll.
4. **KrackedDevs profile card image**: the close-up card. It's used for the builder intro near the start, a trading-card reveal.
5. **Full KrackedDevs profile screenshot**: used for "Meet the builder" near the end.

The builder intro comes right after Kenji's opening line:
- An iris wipe opens it, and the card spins in showing its KD back, then lands with a flash.
- The card stays centred in a holo border and tilts slowly.
- Kenji says one or two lines about the builder while their name and stats pop in, ending on the project name.
- The close-up card is low-res, so it's upscaled 3x with EDSR, giving `img/<builder>_card_x3.png`.

## Real episodes (from EP.01 Arkedia)
EP.01 (`index.html` in this folder) is the full episode layout. Copy it for each new project and change:

1. **Clips.** Put the maker's recordings in a folder, set the cut points in `extract_clips.sh`, then run it. Each clip becomes `clips/<name>/0001.jpg...` (30 fps, already sped up or slowed down).
2. **`WINS`** in index.html: one entry per demo segment, with:
   - timing, clip name and frame count;
   - the URL and tag shown on the browser frame;
   - a camera path `[t, centerX, centerY, zoom]` so the view can zoom in on the board.
3. **Info card pages** (`.pg` blocks): the project's real facts, one page per segment. Pop-ins are timed to Kenji's words with `WT(line, word)`.
4. **Narration** in `vo/narration.json` (Kenji, plus one Kopi line):
   - Run `gen_vo.py`, then `wordtimes.py` (it writes `words.js`), then `lipsync.py <seconds>`.
   - Write numbers out in words. Spell tricky names the way they should sound (e.g. "Arcadia" for Arkedia).
5. **Builder profile**: their KrackedDevs profile screenshot goes in `img/`. It's shown at about 3/4 screen size in the "Meet the builder" scene, with glowing rings and callouts timed to the voice.
6. **Kopi's compliment** must be new. Check `compliments.json` and add the new one.
7. **Kenji's outfit rotates**: EP.00 overshirt, EP.01 windbreaker, EP.02 blackout, EP.03 denim, EP.04 techwear.

Episode flow:
- Intro
- Studio open
- Builder intro (card reveal)
- Project segments (the shelf, then one segment per game or feature, then how deep it goes)
- Kopi's cameo in the studio
- Under the hood
- Meet the builder
- Studio outro
- End card

Encode about 2.2 Mbps two-pass for a roughly 95-second episode, so the file stays under 30 MB.

## Files
| File | What it does |
|---|---|
| `index.html` | The whole video: set, scenes, timeline (GSAP) and Kenji's action schedule |
| `kenji.js` | Kenji: sprite, faces, poses, 5 outfits. `svg(uid, outfit, layer)` can split `base` and `arms` so desk props sit between them. |
| `kopi.js` | Kopi (shared with KD Tech Daily) |
| `props.js` | Pixel desk props: keyboard, glass, laptop, plant, cube, duck, sparkle |
| `vo/narration.json` | Script lines, each with a speaker (`kenji` / `kopi`), start time and max length |
| `vo/gen_vo.py` | Records each line with the right voice and fits its speed to the window |
| `lipsync.py` | Turns the clips into per-speaker mouth shapes, written to `lipsync.js` |
| `audio.py` | Original 104 BPM chip-funk groove (E dorian) and sound effects synced to the animation |
| `mix_vo.py` | Mixes the voices over the music, ducking the music under speech |
| `render.mjs` / `snap.mjs` | Renders the frames to MP4, or grabs still frames to check the layout |
| `compliments.json` | Log of Kopi's compliments, so none repeat |

## Run it yourself
Needs Node 18+, Python 3 (numpy, scipy, soundfile, kokoro-onnx) and ffmpeg.
Kokoro model files go in `vo/` (`kokoro-v1.0.onnx`, `voices-v1.0.bin`), from https://github.com/thewh1teagle/kokoro-onnx/releases
```
npm i && npm i playwright && npx playwright install chromium
cd vo && python3 gen_vo.py && cd ..        # 1. voices
python3 lipsync.py 30                      # 2. mouth shapes (arg = video length in seconds)
node render.mjs 2                          # 3. frames -> out/video_silent.mp4
python3 audio.py && python3 mix_vo.py      # 4. music + SFX + voice mix
ffmpeg -i out/video_silent.mp4 -i out/audio_vo.wav -af "loudnorm=I=-14:TP=-1.5" -c:v copy -c:a aac -b:a 160k built-at-kd.mp4
```
