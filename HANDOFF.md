# KD video studio: handoff for a new Claude session

This file carries over everything from the original Cowork session (29 Sep to 1 Oct 2026) so a new Claude, on any account, can carry on making the two KrackedDevs video shows exactly as before. Read all of it before starting work.

> **1 Oct 2026:** the studio moved to Prince's Windows PC at `C:\UTHMAAN\AntiGravit\KD-Studio`. `CLAUDE.md` covers what changed: the Python venv, no 20 MB limit, and direct media downloads. The sandbox-only notes below (§1 deliveries, §5, §8) are kept for history.

**Owner:** Prince. KD is **KrackedDevs**, a developer community (krackeddevs.com). Its tagline is "Learn. Build. Ship." Its brand is dark/terminal with a green pixel "KD" logo.

---

## 1. Standing rules (apply to every video)
- **Every video ships in two formats (rule from 2 Oct 2026):** 16:9 at 1920x1080 and 9:16 at 1080x1920. Both are made from the same page, voice and timeline.
  - KD Tech Daily: `index.html` renders 16:9, and `index.html?fmt=916` renders the stacked 9:16 layout. Use `FMT=916 node render.mjs 6` (writes to `out-916/`) and `FMT=916 node snap.mjs ...` (writes to `snaps-916/`).
  - Built at KD: no 9:16 layout yet. Build one before EP.02 (see §9).
- **Background music is subtle (rule from 2 Oct 2026):** it should sit in harmony with the voice. It shouldn't be too soft, and never near voice level. The target is roughly 18-20 dB under the voice while anyone talks and no more than about 9 dB under it with no voice. Don't let the bed swell up between lines. Tech Daily's `mix_vo.py` still uses the older, louder setting (10 dB under, ducking between lines); bring it in line on its next episode.
- **Every video comes with a post caption (format updated 2 Oct 2026):**
  - Hook: one catchy line that teases the episode **without naming any of the stories**.
  - Then one bullet (•) per story with slightly more detail than the video (a key number, name or fact), but still short.
  - Then the sign-off. See §6. Paste it in the chat reply with every delivery (re-renders too), ready to copy. One caption covers both formats.
- **Use real media:**
  - Real photos and real video clips of the companies and products covered, with on-screen credit ("IMAGE: GOOGLE", "VIDEO: DOORDASH").
  - Official company logos, smaller than the KD logo, with no implied endorsement. Trademark credit goes in the outro sources line.
- **Narration (updated 2 Oct 2026):**
  - The voice now goes through `tools/kd_voice.py` (misaki, the converter Kokoro was trained on, plus a KD dictionary). Write acronyms the normal way ("AI", "APIs", "FTC", "GPT-6"). **Don't** space them out ("A P Is" is read as "uh pee iz"). Numbers can be digits or words.
  - Add any name it gets wrong to `LEXICON` (and multi-word fixes to `PHRASES`) in `tools/kd_voice.py`.
  - After `gen_vo.py`, run `.venv/Scripts/python tools/vo_check.py <show>/vo`. It transcribes each clip with Whisper and lists the words heard differently, so check those.
- **Deliveries:**
  - Send both MP4s in chat. Keep each under 30 MB: two-pass x264, around 2.0 to 2.6 Mbps for 80 to 105 s. Both formats share one audio mix.
  - The desktop bridge can only write files up to 20 MB, so large videos stay in chat, or are split and rejoined on the PC (see §8).
  - Templates, sheets and images go to the PC's `Downloads/KD-Tech-Daily` and `Downloads/Built-at-KD` folders.
- **Built at KD:** before starting an episode, check that all five materials are there (§3.2). Ask Prince for anything missing; don't build without it.

---

## 2. Show 1: KD Tech Daily (news)
A daily tech-news recap of the five biggest stories, anchored by **Kopi**.

### 2.1 Kopi (the news anchor)
- **Look:** an original pixel-anime anchor (Prince asked for "Naruto with shades and gadgets"; we made an original instead, which he accepted).
  - Indigo hair with a mint streak, and a high ponytail with a mint hair-tie.
  - **LED visor shades** that show her eyes and expressions.
  - Headset mic, a mint wrist gadget, a KD lapel pin.
  - A **hovering drone sidekick** whose light flashes red on bad-news stories.
- **Code:** `shows/kd-tech-daily/anchor.js`. Pixel grid 40x48 units, `KOPI.svg(uid, outfit, layer)` and `KOPI.update(el, state)`.
- **Expressions (visor eyes):**
  - Originals: normal, blink, happy (^ ^), worried, dollar ($ $), shocked, star.
  - Added in v3: down (reading), wink, heart.
- **Mouths:**
  - Lip-sync shapes: closed, m1, m2, m3, O.
  - Others: smile, frown, grin, pout.
- **Kopi v3 (1 Oct 2026): life-like moves.** Prince asked for this: "more animations to make her feel life like, she's a girl and a news anchor."
  - She has an arms layer and 15 poses: rest, papers (tidies her script), read, sip (KOPI coffee mug), tablet (swipes), headset (listening to the producer), tuck (hair behind her ear), point (to the story), pen (thinking), write (scribbles a note), thumb, heart (heart hands), visor (taps her shades), fist, wave.
  - Draw the `'base'` layer behind the desk and the `'arms'` layer in front of it.
  - `state.look` turns her head. `state.drone = {x, y, parked}` moves the drone (it parks on its desk dock at the end of the show).
  - Her actions are scheduled in the `ACT` list in index.html and timed to words in her script with `WT(lineId, word)`.
- **Desk** (`newsdesk.js`, requested by Prince: "make her desk much better with items she interacts with"):
  - Props: LED clock, laptop with stickers, desk mic with a KD flag, script papers and pen, KOPI coffee mug with steam, tablet, succulent, drone dock.
  - Any prop she picks up is hidden on the desk while it's in her hands.
- **Voice:** Kokoro TTS `af_heart` (American female), base speed 1.1. Each line is auto-sped (up to 1.4) to fit its window.
- **Wardrobe:** rotate one outfit per episode.

| # | id | Name | Look |
|---|---|---|---|
| - | classic | Classic Green Blazer | ep 1 only, outside the rotation |
| 1 | hoodie | Launch Hoodie | violet hoodie, white drawstrings, kangaroo pocket, mint </> print |
| 2 | batik | Batik Blazer | teal Malaysian batik blazer, gold/aqua florals, white shirt, gold tie |
| 3 | bomber | Night Shift Bomber | charcoal bomber, orange rib collar/hem, silver zip, orange flight tag |
| 4 | varsity | Varsity K | red letterman, cream sleeves, striped rib, chenille K patch |
| 5 | raid | Raid Armor | steel plates, cyan glowing core, pauldrons, HP bar |

**Episodes so far:**
- 29 Sep 2026: daily recap, classic. Vertical, drawn doodles.
- 30 Sep 2026: OpenAI DevDay special, hoodie. Made vertical, then 16:9, then v2 with OpenAI logos.
- 1 Oct 2026: daily, **batik**.
- Fri 2 Oct 2026: daily, **bomber**. Made on the evening of 1 Oct in KD-Studio. Stories: decision models (Amazon Strands Decider + Cloudflare Clef), the Pentagon/DMDC breach, DeepSeek x Huawei Ascend tools, Newsom's veto of the smart-glasses bill (SB 1130), and Shopify Canvas.

**Next episode → `varsity`**, then raid, hoodie, batik, bomber, and round again.

### 2.2 Current news format (1 Oct 2026 layout: `shows/kd-tech-daily/index.html`)
- **Length:** about 83 s.
- **Intro (0 to 4.5 s):** KD logo, "TECH DAILY", date chip, today's rundown with company logos.
- **Studio open (4.5 to 11 s):** wide shot.
  - Kopi at the full desk, a wall screen, a pixel city skyline, ceiling spots and an ON AIR tag.
  - A rundown card on the left. Kopi greets, waves and points.
- **Five stories × 13 s:**
  - **First 3 s, studio:** an over-the-shoulder card (number, tag, thumbnail, short title). The wall screen shows the company logo, and Kopi reacts.
  - **Next 10 s, story package:**
    - Left side: diff-style headline ("+" green for good news, "-" red for bad), two typed bullets and a terminal joke.
    - Right side: a media panel with a real photo, chart or **video clip**, and Kopi's studio cam (desk, with a mini screen behind her).
- **Outro (76 to 83 s):** wide studio with "that's the diff.", "now go build something", a sources line and a fade.
- **Look and sound:** dark terminal style with matrix rain, scanlines and grain. Scrolling ticker. Original 120 BPM chiptune ducked under the voice. Loudness -14 LUFS.
- **Story data** lives in `STORIES` in index.html: sign, tag, short, lines, mood, bullets, term, sticker, logo, media, credit, label.

---

## 3. Show 2: Built at KD (community project showcase)
- **Purpose:** showcases projects built by KrackedDevs members. Separate from the news.
- **Host: Kenji Neo**, an original pixel anime host (`shows/built-at-kd/kenji.js`).
  - Male, casual but cool and techy: messy black hair with lime tips, smart glasses with a HUD glint, headphones around his neck. Teh tarik is always nearby.
  - **Voice:** Kokoro `am_puck` at speed 1.1 (alternates: am_fenrir, am_michael).
  - **"Alive" poses:** rest, type, sip (teh tarik), glasses (pushes them up), thumb, point, stretch, wave. He nods to the beat and glances while talking.
  - **Faces:** eyes normal, blink, happy, wide, wink. Brows normal, up, focus.

| # | id | Name | Episode |
|---|---|---|---|
| 1 | overshirt | Studio Overshirt (olive over white KD tee) | EP.00 style test |
| 2 | windbreaker | Retro Windbreaker (mint, cream band, violet stripe) | EP.01 Arkedia |
| 3 | blackout | Blackout Hoodie (black, lime strings, lightning, chain) | **next: EP.02** |
| 4 | denim | Denim + Pins | |
| 5 | techwear | Techwear Vest | |

- **Set:** milky cream background (Prince asked for "milky, more funky but still KD").
  - Drifting pastel blobs (mint, lilac, butter, peach, sky), milk drips, halftone, squiggles.
  - Chunky ink outlines with offset shadows. Fonts: Bungee, Silkscreen, Space Grotesk, Archivo.
  - **Techy desk:** graphite with a mint LED edge, LED marquee, speaker grills, stripes, a checker band.
  - Props: RGB keyboard, sticker laptop, RGB cube lamp, teh tarik, rubber duck, plant.
- **Music:** original 104 BPM chip-funk in E dorian. Kopi's chiptune sparkle plays during her cameo. Claps play during the builder scenes.

### 3.1 Episode structure (EP.01, about 1:45)
1. Intro: title slam.
2. Studio open: Kenji says hi, then "Today's build comes from a builder you should meet."
3. **Builder intro (mini):**
   - An iris wipe opens it, and their **KrackedDevs profile card** flies in back-first (the KD side) and lands face up.
   - It sits **centred, filling the screen**, inside an animated rainbow holo border with corner brackets, tilting slowly.
   - Name and stats pop in as Kenji says one or two lines. This is mandatory every episode.
   - Prince's card images are small, so upscale them 3x (EDSR, see §5).
4. **Project segments:**
   - A browser-frame demo panel playing the maker's videos, with camera zooms.
   - An info card per segment, with facts popping in on Kenji's words.
   - Kenji's picture-in-picture cam, and a B-roll film strip.
5. **Kopi's cameo**, in the studio:
   - She slides in, star eyes, gives ONE compliment, waves and leaves.
   - **Never reuse a compliment.** Check `compliments.json` first, then add the new one.
6. "Under the hood": stack and house rules.
7. **Meet the builder (detailed):** their **full KrackedDevs profile screenshot** at about 3/4 screen in a cool animated border, with glowing rings and callouts on name, rank, contributions and shipped projects.
8. Studio outro: the URL on the wall screen, sign-off.
9. End card.

### 3.2 Materials checklist (ask Prince before building)
1. The project site link (go through it for the facts).
2. The creator's name and handle.
3. Demo videos (screen recordings).
4. The KrackedDevs **profile card** image (the close-up card).
5. A screenshot of the **full KrackedDevs profile**.

### 3.3 Episodes and compliments so far
- **EP.00 style test** (30 Sep). Kopi: "Ooh, look at this studio! So fresh. Kenji, you're gonna crush it!"
- **EP.01 Arkedia by Judeen** (30 Sep / 1 Oct). arkedia.judeen.dev: 14 classic games, each with rules, a worked example, strategy and "the idea underneath". Astro. No accounts, ads or timers.
  - Kopi: "Hold on, recursion hiding inside a puzzle game? Judeen, that's sneaky smart. Bookmarked!"
  - Narration pronounces it "Arcadia" (Prince confirmed this on 1 Oct). The referral code doesn't appear in the final video, so nothing needs blurring.
  - The source videos are on Prince's PC in `Downloads/Arkedia Videos`. Rebuild frames with `extract_clips.sh`.

---

## 3b. Show 3: KD Hot Topic (added 2 Oct 2026; working title)
Folder: `hot-topic/`. Read `hot-topic/README.md` for the build steps.
- **Concept:** a deep dive on today's single trending tech topic. Find the hot topic yourself; Prince doesn't supply it.
- **Anchors:** Kopi and Kenji report together.
  - The dialogue alternates between them, with banter and reactions ("Free output? Okay, now I'm listening").
  - The listener looks at the speaker and nods.
  - They interact: Kenji points at Kopi, Kopi's drone flies over to Kenji, and the desk buzzers light up.
- **Set:** a proper newsroom, all pixel art.
  - A curved desk in the centre.
  - A huge video wall behind them showing the news.
  - A giant window with a Kuala Lumpur skyline at dusk (Merdeka 118, Petronas Twin Towers, Menara KL).
  - The desk carries each anchor's items plus props tied to the topic (EP.01: magic 8-ball and YES/NO buzzers).
- **Media:**
  - Images and videos, with **video first**: official company clips, such as the company site's own animations or official YouTube keynotes cut with yt-dlp `--download-sections`.
  - The show cuts back and forth between the newsroom and full-screen media. The camera pushes into the wall, then a flash cut to the media, which carries the watermark bug, LIVE chip, ticker, credit and a lower third with a talking avatar of whoever is speaking.
- **Length:** about 1:45, and both formats.
- **Music:** an ambient synth score (Prince asked for synth ambient background music on 2 Oct). It isn't the chiptune the other shows use. See `hot-topic/audio.py`.
  - The mix is a steady bed 19 dB under the voice, 14 dB under in the intro and outro. Finish with `finish_audio.sh` (fixed gain), not single-pass loudnorm.
- **Video wall:** big (Prince asked for it bigger on 2 Oct). In 16:9, card text stays in the top band, above the anchors' heads.
- **Caption:** same house style, with the hashtag #KDHotTopic.
- **Voices:** Kopi uses af_heart, Kenji am_puck, both at 1.1.
- **Wardrobe:** this show has its own picks. EP.01: Kopi in batik, Kenji in denim.
- **Episodes:** EP.01, 2 Oct 2026, "The Decision Model Wars".

---

## 4. Production pipeline (all shows)
Each video is an HTML/CSS/JS animation on a GSAP timeline (paused). The page exposes:
- `window.__seek(t)`: deterministic. It returns a promise that resolves when any images for that frame have decoded.
- `__ready`, `__DURATION`, `__FPS`, `__W`/`__H`.
- `__EVENTS`: the cue sheet for sound effects.
- `__MUSIC`: song length and sections.

Steps (run inside the show folder):
```
npm i gsap @fontsource/jetbrains-mono @fontsource/silkscreen @fontsource/space-grotesk @fontsource/bungee @fontsource-variable/archivo simple-icons playwright
# Kokoro voice models (HuggingFace is blocked in the sandbox; GitHub releases work):
#   https://github.com/thewh1teagle/kokoro-onnx/releases  -> vo/kokoro-v1.0.onnx, vo/voices-v1.0.bin
pip install kokoro-onnx soundfile scipy numpy --break-system-packages
cd vo && python3 gen_vo.py              # 1. voice clips (+ timeline.json). gen_vo.py <id> re-records one line
#    then set each line's "start" in narration.json + timeline.json to its scene time
#    on the PC: ../../.venv/Scripts/python gen_vo.py, then ../.venv/Scripts/python ../tools/vo_check.py vo (from the show folder) to catch mispronounced words
python3 wordtimes.py && cd ..           # 2. word timings -> words.js (WT(line, word) in the page)
python3 lipsync.py <seconds>            # 3. per-speaker mouth shapes -> lipsync.js
node snap.mjs 3 12.5 30                 #    check stills in snaps/ (look at them!); FMT=916 node snap.mjs ... for 9:16
node render.mjs 2                       # 4. frames -> out/video_silent.mp4 (+ out/events.json, out/music.json)
FMT=916 node render.mjs 2               #    9:16 frames -> out-916/video_silent.mp4 (muxed with the same out/audio_final.wav)
python3 audio.py && python3 mix_vo.py   # 5. music + SFX from the cue sheet, voice mixed 10 dB over a ducked bed
ffmpeg -i out/audio_vo.wav -af "acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120,loudnorm=I=-14:TP=-2.5:LRA=9,alimiter=limit=0.7:level=false" out/audio_final.wav
ffmpeg -i out/video_silent.mp4 -c:v libx264 -preset slow -tune animation -b:v 2400k -maxrate 5000k -bufsize 10000k -pass 1 -an -f mp4 /dev/null
ffmpeg -i out/video_silent.mp4 -i out/audio_final.wav -c:v libx264 -preset slow -tune animation -b:v 2400k -maxrate 5000k -bufsize 10000k -pass 2 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart -shortest final.mp4
```
**Quality checks before delivering:**
- A contact sheet of about 24 frames.
- Loudness at -14 LUFS, true peak no higher than -1.5.
- Lip-sync: correlate mouth-pixel counts in the final video with voice RMS. Above 0.6 at lag 0 or ±1 is good.
- File size under 30 MB.

---

## 5. Getting real media (the sandbox's network is restricted)
- **Blocked from the cloud sandbox and the PC shell:** youtube, storage.googleapis.com, wikimedia, huggingface, ctfassets, doordash, reddit, krackeddevs.com and others. pypi, npm and GitHub releases work.
- **Use the desktop app's built-in browser** (Claude_Browser tools) on Prince's PC.
  - Prince has allowed youtube.com, blog.google and elevenlabs.io. Reddit is blocked by safety rules.
  - The pane can't download files, so draw the media on a canvas and screenshot it. Use `tools/browser-capture.js` (instructions at the top of that file), with `decode_caps.py` and `mkbatch.py` in `shows/kd-tech-daily/research/`.
  - **Video:** play the official YouTube video, seek, and capture two barcoded frames per screenshot at 10 to 12 fps. Prime each screenshot with a tiny one (scale 0.1) first, otherwise you get stale frames. Decode, then smooth to 30 fps with ffmpeg `minterpolate`.
  - **Images:** draw the full-res image in four 800x450 tiles with barcodes, then stitch them to 1600x900.
  - `YouTube /oembed` gives titles for video IDs. Channel `/videos` pages list `contentId`s.
- **Logos:** the `simple-icons` npm package (recolor to white). OpenAI's wordmark is in `logos/`.
- **Chromium can't play H.264**, so the page shows clips as JPEG frame sequences (`clips/<name>/0001.jpg`), stepped per frame in `procedural(t)`.
- **Upscaling small images:** OpenCV EDSR x3. Model: raw.githubusercontent.com/Saafke/EDSR_Tensorflow/master/models/EDSR_x3.pb. Use `opencv-contrib-python-headless==4.8.1.78` in a venv, because newer OpenCV versions break `dnn_superres`.

---

## 6. Captions (house style, updated 2 Oct 2026)
- The hook is one catchy line that teases the episode and doesn't give away the stories.
- Each story gets one short bullet with a little more detail than the video.
- End with the sign-off, and paste it in the chat with every delivery.
> Friday's changelog just dropped, and it's a spicy one 🌶️
>
> • Amazon's Strands Decider 2B and Cloudflare's Clef are open-source decision models: pick an option, get odds, no text. Clef-flash answers in 39 ms vs Jev's 524 ms
> • Hackers sat in a Pentagon personnel file share for ~9 months and took ~3M records, with SSNs stored unencrypted. Attacker still unknown
> • DeepSeek and Huawei open-sourced 6 AI tools for Ascend 950 chips, keeping Nvidia-style APIs, with kernels hitting 99.8% of peak
> • Newsom vetoed SB 1130, California's ban on secret recording with smart glasses, calling it too broad. Meta sold 7M+ pairs last year
> • Shopify Canvas lets merchants chat with Sidekick to build their store, editing real theme code live. Desktop-only, rolling out now
>
> Learn. Build. Ship. #KDTechDaily

---

## 7. What's in this kit
| Path | What |
|---|---|
| `shows/kd-tech-daily/` | The latest news project (1 Oct episode): Kopi v3 + desk, page, voice clips, captured clips, images, logos, capture scripts. `episodes/` has earlier pages (DevDay 16:9 v2 uses `episodes/devday-img/` as its `img/`). |
| `shows/built-at-kd/` | The latest Built at KD project (EP.01 Arkedia): Kenji, set, builder intro, profile scene, compliments log, clip extractor. `style-test/` is EP.00. Its `kopi.js` is Kopi v2 (cameo only). Swap in v3 `anchor.js` if she should move there too. |
| `videos/` | Final MP4s: news 1 Oct, DevDay 16:9 v2, Built at KD style test, EP.01 Arkedia |
| `sheets/` | Character and moves sheets, Kenji voice options, the original voice sampler |
| `tools/browser-capture.js` | Media capture helpers for the built-in browser |
| `memory-import.txt` | Paste this into the new account's Settings > Memory > Start import |

Not included because they're large and easy to recreate:
- `node_modules` (npm install).
- The Kokoro models (GitHub releases).
- The Arkedia clip frames (`extract_clips.sh` with Prince's videos).

## 8. Moving big files to Prince's PC
The desktop bridge writes at most 20 MB per file. For bigger files:
1. Split them with `split -b 19m` in the sandbox.
2. Commit the parts to a connected folder.
3. Rejoin them on the PC with the device shell (`cat part_* > file`).
4. Delete the parts once Prince approves deletion.

## 9. Backlog
- KD Tech Daily: the next daily, in Varsity K.
- Built at KD EP.02: Kenji in the Blackout Hoodie. Ask Prince for the five materials, and write a brand-new Kopi compliment.
- Built at KD 9:16 layout: needed before EP.02, since every video now ships in 16:9 and 9:16. Follow the Tech Daily approach: a `?fmt=916` switch on the same page with a `.v916` stylesheet, with wide panels reused at scale inside wrappers.
- Optional: upgrade Built at KD's Kopi cameo to v3 (arms and props).
