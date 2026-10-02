/* KOPI — KD Tech Daily's pixel anime anchor (original character, v2).
   Indigo hair with a mint streak + ponytail, LED visor shades that show her expressions,
   headset mic, wrist gadget, and a hovering drone sidekick whose light flashes red on bad news.
   Pixel grid is 40 x 48 on whole units, so it stays crisp at any integer scale.
   API:  KOPI.svg(uid, outfit, layer)  -> SVG markup   (outfit id from KOPI.OUTFITS; layer 'all' | 'base' | 'arms')
         KOPI.update(rootEl, state)   -> state = {t, mouth, eyes, bob, look, pose, frame, wave, led, drone}
   v3: arms layer with anchor poses that use desk props:
         rest, papers (tidy/tap the script), read, sip (KOPI mug), tablet (swipe), headset (listening to the producer),
         tuck (hair behind ear), point, pen (thinking), write, wave, thumb, heart, visor (tap the shades), fist
   Wardrobe (rotate one per episode): classic, hoodie, batik, bomber, varsity, raid */
const KOPI = (() => {
  const C = {
    ol:'#0a0a14', hair:'#2e2a6b', hairD:'#1e1b4b', hairL:'#4f46e5', hairL2:'#6366f1',
    skin:'#e3a878', skinD:'#c4895c', blush:'#f29a8e',
    frame:'#0b0d10', frameL:'#2a323c', lens:'#062418', glint:'#134d33',
    glow:'#6ef0a0', glowHi:'#e0ffec', gold:'#ffd84d',
    lip:'#7a3b2e', mouthIn:'#5b1a24', tongue:'#e36d7a', teeth:'#f4f1ea',
    shirt:'#e6ebe8', shirtD:'#aab4ae',
    metal:'#a3adb4', metalD:'#6b757c', dark:'#39434a', dark2:'#56626b', mint:'#4ade80'
  };
  const r = (x, y, w, h, c) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${c}"/>`;
  const rr = (x, y, w, h, c) => r(x + 1, y, w - 2, h, c) + r(x, y + 1, w, h - 2, c);   // corner-cut rect
  const pts = (list, c) => list.map(([x, y]) => r(x, y, 1, 1, c)).join('');
  const glyph = (rows, x0, y0, c) => rows.map((row, j) => [...row].map((ch, i) => ch === '#' ? r(x0 + i, y0 + j, 1, 1, c) : '').join('')).join('');

  /* ---------- shared body pieces ---------- */
  const NECK = r(16, 26, 8, 6, C.ol) + r(17, 26, 6, 6, C.skin) + r(17, 26, 6, 2, C.skinD);
  const torso = (base, light, dark) =>
    r(8, 30, 24, 1, C.ol) + r(5, 31, 30, 1, C.ol) + r(3, 32, 34, 1, C.ol) + r(2, 33, 36, 15, C.ol) +
    r(8, 31, 24, 1, base) + r(5, 32, 30, 1, base) + r(3, 33, 34, 15, base) +
    r(8, 31, 24, 1, light) + r(5, 32, 3, 1, light) + r(32, 32, 3, 1, light) + r(3, 34, 2, 14, dark) + r(35, 34, 2, 14, dark);
  const shirtV = (shirt, shade) =>
    r(15, 32, 10, 1, shirt) + r(16, 33, 8, 2, shirt) + r(17, 35, 6, 2, shirt) + r(18, 37, 4, 2, shirt) + r(19, 39, 2, 1, shirt) +
    r(16, 33, 1, 2, shade) + r(23, 33, 1, 2, shade) + pts([[14, 32], [15, 33], [25, 32], [24, 33]], shirt);
  const tie = (main, knot) => r(19, 33, 2, 2, knot) + r(19, 35, 2, 5, main) + pts([[19, 36], [20, 38]], knot);
  const lapels = c => pts([[14, 33], [15, 34], [15, 35], [16, 36], [16, 37], [17, 38], [17, 39], [18, 40],
                           [25, 33], [24, 34], [24, 35], [23, 36], [23, 37], [22, 38], [22, 39], [21, 40]], c);
  const pin = (x, y) => `<image href="brand/kd_logo.png" x="${x}" y="${y}" width="7" height="5.4" preserveAspectRatio="xMidYMid meet" style="image-rendering:pixelated"/>`;

  /* ---------- wardrobe ---------- */
  const OUTFITS = {
    // Episode 1 look
    classic: { name: 'Classic Green Blazer',
      body: () => torso('#166534', '#22914d', '#0e4424') + shirtV(C.shirt, C.shirtD) + tie('#4ade80', '#15803d') + lapels('#0a361d') +
        r(20, 41, 1, 7, '#0e4424') + pts([[19, 43], [19, 46]], '#0a361d') + r(26, 38, 6, 1, '#0e4424') + r(27, 37, 2, 1, C.mint) + pin(6, 35),
      sleeve: { base: '#166534', light: '#22914d', cuff: C.shirt, cuff2: C.shirt } },

    // 1 — violet dev hoodie, drawstrings, kangaroo pocket, mint </> print
    hoodie: { name: 'Launch Hoodie',
      body: () => torso('#6d28d9', '#8b5cf6', '#4c1d95') +
        r(10, 29, 20, 1, C.ol) + r(10, 30, 20, 3, '#5b21b6') + r(11, 30, 18, 1, '#7c3aed') + r(15, 31, 10, 2, '#1e1033') +   // hood rim
        r(16, 33, 1, 5, '#f1f5f9') + r(23, 33, 1, 5, '#f1f5f9') + pts([[16, 38], [23, 38]], C.metal) +                      // drawstrings
        r(11, 41, 18, 5, '#5b21b6') + r(11, 41, 18, 1, '#4c1d95') + r(11, 42, 1, 4, '#3b0f7a') + r(28, 42, 1, 4, '#3b0f7a') + // pocket
        r(3, 46, 34, 1, '#4c1d95') +                                                                                    // rib hem
        glyph(['..#...#.#..', '.#....#..#.', '#....#....#', '.#..#....#.', '..#.#...#..'], 24, 35, C.mint) +      // </>
        pin(6, 35),
      sleeve: { base: '#6d28d9', light: '#8b5cf6', cuff: '#4c1d95', cuff2: '#5b21b6' } },

    // 2 — Malaysian batik blazer, teal with gold/aqua florals, gold tie
    batik: { name: 'Batik Blazer',
      body: () => {
        let motif = '';
        for (let y = 34, row = 0; y <= 46; y += 4, row++) for (let x = 5 + (row % 2) * 3; x <= 34; x += 6) {
          if (x >= 13 && x <= 26 && y <= 41) continue;              // keep the shirt/tie area clean
          if (x >= 5 && x <= 13 && y >= 34 && y <= 40) continue;    // keep the pin clear
          motif += pts([[x, y - 1], [x - 1, y], [x + 1, y], [x, y + 1]], '#5eead4') + r(x, y, 1, 1, '#fbbf24');
        }
        return torso('#0f766e', '#14b8a6', '#115e59') + motif + shirtV(C.shirt, C.shirtD) + tie('#f59e0b', '#b45309') + lapels('#0b4f4a') +
          r(20, 41, 1, 7, '#115e59') + r(27, 37, 3, 1, '#fbbf24') + pin(6, 35);
      },
      sleeve: { base: '#0f766e', light: '#14b8a6', cuff: C.shirt, cuff2: C.shirt, dot: '#fbbf24' } },

    // 3 — charcoal bomber, orange rib collar/hem, silver zip
    bomber: { name: 'Night Shift Bomber',
      body: () => {
        let rib = ''; for (let x = 10; x < 30; x += 2) rib += r(x, 30, 1, 2, '#c2410c');
        let hem = ''; for (let x = 3; x < 37; x += 2) hem += r(x, 45, 1, 3, '#c2410c');
        return torso('#1f2937', '#374151', '#111827') +
          r(10, 30, 20, 2, '#f97316') + rib + r(15, 32, 10, 2, '#0b0d0f') +      // rib collar + tee
          r(3, 45, 34, 3, '#f97316') + hem +                                      // rib hem
          r(20, 33, 1, 12, C.metal) + r(19, 34, 3, 2, '#e2e8f0') +                // zip + pull
          r(26, 36, 6, 2, '#f97316') + r(27, 36, 1, 1, '#1f2937') + r(29, 36, 2, 1, '#1f2937') +   // flight tag
          pin(6, 35);
      },
      sleeve: { base: '#1f2937', light: '#374151', cuff: '#f97316', cuff2: '#c2410c' } },

    // 4 — red letterman, cream sleeves, striped rib, chenille K patch
    varsity: { name: 'Varsity K',
      body: () => {
        const cream = '#f3ead3', creamD = '#d8ccb0';
        let snaps = ''; [34, 37, 40, 43].forEach(y => snaps += r(20, y, 1, 1, cream));
        return torso('#b91c1c', '#dc2626', '#7f1d1d') +
          r(3, 33, 4, 15, cream) + r(6, 33, 1, 15, creamD) + r(33, 33, 4, 15, cream) + r(33, 33, 1, 15, creamD) +   // leather sleeves
          r(5, 32, 3, 1, cream) + r(32, 32, 3, 1, cream) +
          r(11, 30, 18, 2, cream) + r(11, 31, 18, 1, '#b91c1c') + r(15, 32, 10, 1, '#0b0d0f') +                     // striped collar
          r(7, 44, 26, 1, cream) + r(7, 45, 26, 1, '#b91c1c') + r(7, 46, 26, 1, cream) +                            // striped hem
          snaps +
          r(8, 34, 7, 9, '#7f1d1d') + glyph(['#...#', '#..#.', '#.#..', '##...', '#.#..', '#..#.', '#...#'], 9, 35, cream) +   // K patch
          pin(25, 36);
      },
      sleeve: { base: '#f3ead3', light: '#fffaf0', cuff: '#b91c1c', cuff2: '#f3ead3' } },

    // 5 — KD Raid armour: steel plates, cyan core, shoulder pauldrons, HP bar
    raid: { name: 'Raid Armor',
      body: () => {
        const plate = '#64748b', hi = '#94a3b8', cy = '#22d3ee', cyD = '#0e7490';
        return torso('#475569', '#64748b', '#1e293b') +
          r(13, 30, 14, 2, '#1e293b') + r(14, 30, 12, 1, '#334155') +                                               // gorget
          rr(1, 31, 10, 5, C.ol) + r(2, 32, 8, 3, plate) + r(3, 32, 6, 1, hi) + pts([[3, 34], [8, 34]], '#0f172a') + // left pauldron
          rr(29, 31, 10, 5, C.ol) + r(30, 32, 8, 3, plate) + r(31, 32, 6, 1, hi) + pts([[31, 34], [36, 34]], '#0f172a') +
          r(16, 35, 8, 6, '#0f172a') + r(18, 36, 4, 4, cy) + r(17, 37, 6, 2, cy) + r(19, 37, 2, 2, '#cffafe') +       // glowing core
          r(6, 42, 28, 1, cyD) + r(20, 41, 1, 7, cyD) +                                                            // seams
          r(26, 37, 8, 3, '#0f172a') + r(27, 38, 5, 1, C.mint) + r(32, 38, 1, 1, '#ef4444') +                       // HP bar
          pin(6, 36);
      },
      sleeve: { base: '#475569', light: '#94a3b8', cuff: '#22d3ee', cuff2: '#0e7490' } },
  };

  /* ---------- head ---------- */
  const seg = (x, y, w, h) => [x, y, w, h];
  const PONY_SEGS = [seg(28, 2, 5, 4), seg(31, 0, 5, 4), seg(34, 1, 4, 5), seg(35, 5, 4, 6), seg(36, 10, 3, 6), seg(37, 15, 2, 4)];
  const PONY =
    PONY_SEGS.map(([x, y, w, h]) => r(x - 1, y - 1, w + 2, h + 2, C.ol)).join('') +
    PONY_SEGS.map(([x, y, w, h]) => r(x, y, w, h, C.hair)).join('') +
    r(32, 1, 3, 1, C.hairL) + r(35, 2, 2, 1, C.hairL) + r(38, 6, 1, 9, C.hairD) + r(37, 12, 1, 4, C.hairD) +
    r(28, 3, 2, 4, C.mint) + r(28, 4, 2, 1, '#16a34a');                                   // mint hair-tie gadget
  const HEAD =
    rr(7, 3, 26, 25, C.ol) + rr(8, 4, 24, 23, C.hair) +                                  // back hair mass
    r(12, 5, 8, 1, C.hairL) + r(10, 6, 3, 1, C.hairL) + r(21, 5, 3, 1, C.hairL2) + r(9, 22, 2, 5, C.hairD) + r(29, 22, 2, 5, C.hairD) +
    r(12, 10, 16, 15, C.skin) + r(13, 25, 14, 1, C.skin) + r(14, 26, 12, 1, C.skin) + r(16, 27, 8, 1, C.skin) +   // face
    r(26, 19, 1, 5, C.skinD) + r(25, 24, 2, 1, C.skinD) +
    pts([[12, 25], [13, 26], [14, 27], [15, 27], [27, 25], [26, 26], [25, 27], [24, 27]], C.ol) +
    r(11, 7, 18, 6, C.hair) + r(12, 12, 2, 1, C.hairD) + r(17, 12, 3, 1, C.hairD) + r(22, 12, 1, 1, C.hairD) + r(25, 12, 2, 1, C.hairD) +   // bangs meet the visor
    pts([[13, 11], [19, 11], [24, 11]], C.hairD) +
    r(12, 8, 4, 1, C.hairL) + r(20, 8, 5, 1, C.hairL) +
    pts([[15, 7], [15, 8], [15, 9], [16, 10], [16, 11], [16, 12]], C.mint) +                   // mint streak
    r(9, 10, 3, 15, C.hair) + r(9, 25, 2, 2, C.hair) + r(10, 27, 1, 1, C.hair) + r(11, 13, 1, 11, C.hairD) +   // side locks
    r(28, 10, 3, 15, C.hair) + r(29, 25, 2, 2, C.hair) + r(29, 27, 1, 1, C.hair) + r(28, 13, 1, 11, C.hairD) +
    r(10, 13, 20, 6, C.frame) + r(11, 19, 8, 1, C.frame) + r(21, 19, 8, 1, C.frame) + r(10, 13, 20, 1, C.frameL) +   // LED visor shades
    r(12, 14, 7, 5, C.lens) + r(21, 14, 7, 5, C.lens) + pts([[13, 14], [14, 14], [22, 14], [23, 14]], C.glint) + r(29, 15, 1, 2, C.mint) +
    pts([[20, 21]], C.skinD) + r(13, 21, 2, 1, C.blush) + r(25, 21, 2, 1, C.blush) +       // nose + blush
    rr(7, 14, 4, 6, C.ol) + r(8, 15, 2, 4, C.dark) + r(8, 16, 1, 2, C.mint) +               // headset + mic boom
    pts([[9, 20], [10, 21], [11, 22], [12, 23]], C.metal) + r(13, 23, 2, 2, C.mint) + r(30, 14, 2, 5, C.dark);

  /* ---------- drone sidekick ---------- */
  const DRONE = rr(1, 4, 6, 3, C.ol) + r(2, 4, 4, 2, '#46515a') + r(2, 6, 4, 1, '#2c3338') + r(0, 3, 2, 1, C.metal) + r(6, 3, 2, 1, C.metal) + r(3, 7, 2, 1, C.metalD);
  const ROTORS = [r(-1, 2, 4, 1, '#c7d0d6') + r(5, 2, 4, 1, '#c7d0d6'), r(0, 2, 2, 1, '#8a949b') + r(6, 2, 2, 1, '#8a949b')];

  /* ---------- waving arm: skin hand + mint wrist gadget ---------- */
  const hand = (lean) => {
    const rows = ['.####.', '######', '######', '######', '.####.'];
    let out = rr(36, 8, 8, 7, C.ol);
    rows.forEach((row, j) => { const dx = j < 2 ? lean : 0;
      [...row].forEach((ch, i) => { if (ch === '#') out += r(37 + dx + i, 9 + j, 1, 1, C.skin); }); });
    out += r(39 + lean, 9, 1, 2, C.skinD) + r(41 + lean, 9, 1, 2, C.skinD) + r(36, 11, 1, 2, C.skin) + r(37, 12, 1, 1, C.skinD);
    return out;
  };
  const sleeve = s => rr(37, 15, 6, 17, C.ol) + r(38, 16, 4, 16, s.base) + r(38, 16, 1, 16, s.light) +
    r(38, 14, 4, 1, s.cuff) + r(38, 15, 4, 1, s.cuff2) + (s.dot ? pts([[40, 20], [39, 25], [40, 29]], s.dot) : '');
  const watch = r(37, 13, 6, 2, C.ol) + r(38, 13, 4, 1, '#1f2937') + r(39, 13, 2, 1, C.mint);
  const waveFrames = id => { const s = sleeve((OUTFITS[id] || OUTFITS.classic).sleeve); return [s + hand(0) + watch, s + hand(1) + watch]; };

  /* ---------- expressions: LED eyes live in the visor lenses (x 12..18 and 21..27, y 14..18) ---------- */
  const G = C.glow;
  const EYES = {
    normal: (lx) => r(lx + 2, 15, 3, 3, G) + r(lx + 2, 15, 1, 1, C.glowHi),
    blink: (lx) => r(lx + 1, 17, 5, 1, G),
    happy: (lx) => pts([[lx + 1, 17], [lx + 2, 16], [lx + 3, 15], [lx + 4, 16], [lx + 5, 17]], G),
    worried: (lx, side) => (side === 'L'
      ? pts([[lx + 1, 16], [lx + 2, 16], [lx + 3, 15], [lx + 4, 15], [lx + 5, 14]], G)
      : pts([[lx + 1, 14], [lx + 2, 15], [lx + 3, 15], [lx + 4, 16], [lx + 5, 16]], G)) + r(lx + 2, 18, 3, 1, G),
    dollar: (lx) => glyph(['.##', '#..', '.#.', '..#', '##.'], lx + 2, 14, C.gold),
    shocked: (lx) => glyph(['###', '#.#', '###'], lx + 2, 15, G),
    star: (lx) => glyph(['.#.', '###', '.#.', '#.#'], lx + 2, 14, C.gold),
    down: (lx) => r(lx + 2, 17, 3, 2, G) + r(lx + 2, 17, 1, 1, C.glowHi),
    wink: (lx, side) => side === 'R' ? pts([[lx + 1, 17], [lx + 2, 16], [lx + 3, 16], [lx + 4, 16], [lx + 5, 17]], G) : r(lx + 2, 15, 3, 3, G) + r(lx + 2, 15, 1, 1, C.glowHi),
    heart: (lx) => glyph(['#.#', '###', '.#.'], lx + 2, 15, '#ff6fa3'),
  };
  const MOUTH = {
    closed: r(18, 23, 4, 1, C.lip),
    smile: r(18, 23, 4, 1, C.lip) + pts([[17, 22], [22, 22]], C.lip),
    frown: r(18, 22, 4, 1, C.lip) + pts([[17, 23], [22, 23]], C.lip),
    m1: r(18, 22, 4, 2, C.mouthIn) + r(19, 23, 2, 1, C.tongue),
    m2: r(18, 22, 4, 3, C.mouthIn) + r(18, 22, 4, 1, C.teeth) + r(19, 24, 2, 1, C.tongue),
    m3: r(17, 22, 6, 3, C.mouthIn) + r(17, 22, 6, 1, C.teeth) + r(18, 24, 4, 1, C.tongue),
    O: r(19, 22, 2, 1, C.mouthIn) + r(18, 23, 4, 1, C.mouthIn) + r(19, 24, 2, 1, C.mouthIn) + r(19, 23, 2, 1, '#3a0f16'),
    grin: r(17, 22, 6, 2, C.teeth) + r(17, 24, 6, 1, C.lip) + pts([[16, 21], [23, 21]], C.lip),
    pout: r(19, 23, 2, 1, C.lip) + pts([[18, 22], [21, 22]], C.lip),
  };

  /* ---------- arms + props (v3) ---------- */
  // limb: outline pass (each rect grown by 1), then fill, then a 1px highlight on the left edge
  const limb = (rects, fill, light) => rects.map(([x, y, w, h]) => r(x - 1, y - 1, w + 2, h + 2, C.ol)).join('') +
    rects.map(([x, y, w, h]) => r(x, y, w, h, fill)).join('') + (light ? rects.map(([x, y, w, h]) => r(x, y, 1, h, light)).join('') : '');
  const handAt = (x, y, w = 4, h = 3) => r(x - 1, y - 1, w + 2, h + 2, C.ol) + r(x, y, w, h, C.skin) + r(x, y + h - 1, w, 1, C.skinD);
  const WATCH = (x, y) => r(x, y, 4, 1, C.ol) + r(x + 1, y, 2, 1, C.mint);           // mint wrist gadget on her left arm
  const MUG = (x, y) => r(x - 1, y - 1, 7, 8, C.ol) + r(x + 5, y + 1, 2, 4, C.ol) + r(x, y, 5, 6, '#f4f1ea') + r(x + 5, y + 2, 1, 2, '#f4f1ea') +
    r(x, y, 5, 1, '#6b3f22') + r(x, y + 2, 5, 2, C.mint) + r(x + 1, y + 2, 1, 2, '#16a34a') + r(x + 4, y + 1, 1, 5, '#cfcac0');
  const PAPERS = (x, y, w = 12, h = 10) => r(x, y - 2, w + 2, h + 2, C.ol) + r(x + 1, y - 1, w, h, '#d9dee3') +            // back sheet
    r(x - 1, y - 1, w + 2, h + 2, C.ol) + r(x, y, w, h, '#f8fafc') + r(x, y, w, 1, '#ffffff') +
    [2, 4, 6].map(k => r(x + 2, y + k, w - 4 - (k === 6 ? 3 : 0), 1, '#9aa5b1')).join('') + r(x + 2, y + 1, 4, 1, C.mint);
  const TABLET = (x, y, swipe) => r(x - 1, y - 1, 16, 11, C.ol) + r(x, y, 14, 9, '#1f2937') + r(x + 1, y + 1, 12, 7, '#0b3b2a') +
    r(x + 2, y + 2, 6, 1, C.mint) + r(x + 2, y + 4, 9, 1, '#2f8f5b') + r(x + 2, y + 6, 7, 1, '#2f8f5b') + r(x + 9 + (swipe ? -3 : 0), y + 2, 2, 2, '#e0ffec');
  const PEN = (x, y) => r(x, y, 1, 6, C.ol) + r(x, y + 1, 1, 4, '#4ade80') + r(x, y, 1, 1, '#e5e7eb');
  // forearms resting on the desk (desk top sits around y 41 in sprite units)
  const restL = (s, dy = 0) => limb([[3, 33, 4, 7], [5, 39 + dy, 9, 3]], s.base, s.light) + r(13, 39 + dy, 1, 3, s.cuff) + handAt(14, 39 + dy);
  const restR = (s, dy = 0) => limb([[33, 33, 4, 7], [26, 39 + dy, 9, 3]], s.base, s.light) + r(26, 39 + dy, 1, 3, s.cuff) + handAt(22, 39 + dy) + WATCH(27, 39 + dy);
  const POSES = {
    rest: s => restL(s) + restR(s),
    papers: (s, f) => { const dy = f ? -2 : 0;      // tidying the script: tap-tap on the desk
      return PAPERS(14, 28 + dy) + limb([[3, 33, 4, 6], [6, 36 + dy, 7, 3]], s.base, s.light) + handAt(12, 34 + dy, 3, 4) +
             limb([[33, 33, 4, 6], [27, 36 + dy, 7, 3]], s.base, s.light) + handAt(25, 34 + dy, 3, 4) + WATCH(28, 36 + dy); },
    read: s => PAPERS(14, 35) + restL(s, 1) + restR(s, 1),
    sip: s => limb([[3, 33, 4, 6], [6, 35, 3, 4], [8, 31, 3, 4], [10, 27, 3, 4]], s.base, s.light) + r(9, 27, 5, 1, s.cuff) +
              MUG(15, 20) + handAt(13, 21, 4, 4) + restR(s),
    tablet: (s, f) => limb([[3, 33, 4, 6], [6, 37, 6, 3]], s.base, s.light) + limb([[33, 33, 4, 6], [28, 37, 6, 3]], s.base, s.light) +
              TABLET(13, 32, f) + handAt(11, 36, 3, 4) + handAt(26 - (f ? 3 : 0), 34, 3, 3) + WATCH(29, 37),
    headset: s => limb([[3, 33, 4, 6], [3, 28, 4, 6], [5, 23, 3, 6]], s.base, s.light) + r(5, 23, 3, 1, s.cuff) + handAt(5, 19, 4, 4) + restR(s),
    tuck: s => restL(s) + limb([[33, 33, 4, 6], [33, 27, 4, 7], [31, 22, 3, 6]], s.base, s.light) + r(31, 22, 3, 1, s.cuff) + WATCH(31, 23) +
              handAt(28, 17, 4, 5) + r(29, 15, 2, 2, C.hair),
    point: s => limb([[1, 33, 4, 5], [-5, 32, 8, 3]], s.base, s.light) + r(-5, 32, 1, 3, s.cuff) + handAt(-9, 32, 4, 3) + r(-12, 33, 3, 1, C.skin) + restR(s),
    pen: (s, f) => restL(s) + limb([[33, 33, 4, 6], [29, 30, 4, 5], [26, 27, 3, 4]], s.base, s.light) + WATCH(28, 29) +
              handAt(23, 25, 4, 3) + PEN(24 + (f ? 1 : 0), 20),
    write: (s, f) => PAPERS(15, 37, 11, 6) + restL(s) + limb([[33, 33, 4, 7], [26, 38, 9, 3]], s.base, s.light) + WATCH(27, 38) +
              handAt(21 + (f ? 2 : 0), 37) + PEN(23 + (f ? 2 : 0), 33),
    thumb: s => limb([[3, 33, 4, 5], [4, 26, 4, 8]], s.base, s.light) + r(4, 26, 4, 1, s.cuff) + handAt(3, 21, 5, 5) + r(5, 18, 2, 3, C.skin) + r(4, 17, 4, 1, C.ol) + restR(s),
    heart: s => limb([[3, 33, 4, 6], [7, 31, 6, 3]], s.base, s.light) + limb([[33, 33, 4, 6], [27, 31, 6, 3]], s.base, s.light) +
              handAt(13, 29, 4, 4) + handAt(23, 29, 4, 4) + glyph(['##.##', '#####', '.###.', '..#..'], 18, 27, '#ff6fa3') + WATCH(28, 31),
    visor: s => restL(s) + limb([[33, 33, 4, 6], [33, 26, 4, 8], [32, 21, 3, 6]], s.base, s.light) + WATCH(32, 22) +
              handAt(30, 17, 3, 4) + r(30, 15, 1, 2, C.skin),
    fist: s => limb([[3, 33, 4, 5], [3, 24, 4, 10]], s.base, s.light) + r(3, 24, 4, 1, s.cuff) + handAt(2, 19, 6, 5) + r(3, 20, 4, 1, C.skinD) + restR(s),
    wave: s => restL(s),       // the waving arm itself is drawn by the k-wave layer
  };

  function svg(uid, outfit = 'classic', layer = 'all') {
    const o = OUTFITS[outfit] || OUTFITS.classic;
    const base = layer !== 'arms', arms = layer !== 'base';
    return `<svg viewBox="0 0 40 48" shape-rendering="crispEdges" overflow="visible" data-outfit="${outfit}" xmlns="http://www.w3.org/2000/svg">
      <defs><filter id="glow-${uid}" x="-30%" y="-30%" width="160%" height="160%">
        <feGaussianBlur stdDeviation="0.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
      ${base ? `<g class="k-body">${NECK}${o.body()}</g>
      <g class="k-head"><g class="k-pony">${PONY}</g>${HEAD}
        <g class="k-eyes" filter="url(#glow-${uid})"></g><g class="k-mouth"></g></g>
      <g class="k-drone">${DRONE}<rect class="k-led" x="3" y="5" width="2" height="1" fill="${C.mint}"/><g class="k-rot"></g></g>` : ''}
      ${arms ? '<g class="k-arms"></g><g class="k-wave"></g>' : ''}
    </svg>`;
  }

  const waveCache = {};
  function update(root, s) {
    const q = sel => root.querySelector(sel);
    const outfit = q('svg').dataset.outfit || 'classic';
    const sl = (OUTFITS[outfit] || OUTFITS.classic).sleeve;
    const set = (sel, html) => { const el = q(sel); if (el && el.__h !== html) { el.innerHTML = html; el.__h = html; } };
    const attr = (sel, a, v) => { const el = q(sel); if (el && el.getAttribute(a) !== v) el.setAttribute(a, v); };
    const lk = s.look > 0 ? 1 : s.look < 0 ? -1 : 0;
    attr('.k-head', 'transform', `translate(${lk} ${-(s.bob || 0)})`);
    attr('.k-pony', 'transform', `translate(${Math.floor(s.t * 2.5) % 2 + (s.pose === 'tuck' ? 1 : 0)} ${s.pose === 'tuck' ? -1 : 0})`);
    const eyeFn = EYES[s.eyes] || EYES.normal;
    set('.k-eyes', eyeFn(12 + lk, 'L') + eyeFn(21 + lk, 'R'));
    set('.k-mouth', s.pose === 'sip' ? '' : (MOUTH[s.mouth] || MOUTH.closed));
    attr('.k-led', 'fill', s.led || C.mint);
    // the drone hovers top-left; s.drone = {x, y} moves it (e.g. down onto its desk dock)
    const dx = s.drone ? s.drone.x : 0, dy = s.drone ? s.drone.y : Math.round(Math.sin(s.t * 3.1));
    attr('.k-drone', 'transform', `translate(${dx} ${dy})`);
    set('.k-rot', (s.drone && s.drone.parked) ? '' : ROTORS[Math.floor(s.t * 12) % 2]);
    const pose = s.wave ? 'wave' : (s.pose || 'rest');
    set('.k-arms', (POSES[pose] || POSES.rest)(sl, s.frame || 0));
    const frames = waveCache[outfit] || (waveCache[outfit] = waveFrames(outfit));
    set('.k-wave', s.wave ? frames[(s.wave - 1) % 2] : '');
  }
  return { svg, update, C, OUTFITS, POSES: Object.keys(POSES), MUG, PAPERS, TABLET, PEN };
})();
