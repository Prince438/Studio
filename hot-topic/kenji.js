/* KENJI NEO — host of "Built at KD" (original character).
   Casual-techy pixel anime host: messy black hair with lime-dyed tips, smart glasses with a HUD glint,
   headphones around the neck, and a glass of teh tarik never far away.
   Pixel grid is 40 x 48 (arms may overflow the box); whole units keep it crisp at any integer scale.
   API:  KENJI.svg(uid, outfit)       -> SVG markup
         KENJI.update(rootEl, state)  -> state = {t, mouth, eyes, look, brow, bob, pose, frame}
   poses: rest, type, sip, glasses, thumb, point, stretch, wave
   Wardrobe (rotate one per episode): overshirt, windbreaker, blackout, denim, techwear */
const KENJI = (() => {
  const C = {
    ol:'#141018', skin:'#c58b5c', skinD:'#9f6a42', skinL:'#d9a273',
    hair:'#18161f', hairL:'#3a3550', hairD:'#0d0c12', tip:'#a3e635', tipL:'#d9f99d',
    pupil:'#1b1b22', white:'#ffffff', frame:'#111318', lens:'#bfe3ff', hud:'#4ade80',
    lip:'#6b3a2c', mouthIn:'#4a1820', tongue:'#d9606e', teeth:'#f4f1ea',
    phones:'#22252b', phonesL:'#3a3f47', mint:'#4ade80', tee:'#f1f1ec', teeD:'#cfcfc6',
    glass:'#e5e7eb', tea:'#e8c9a0', foam:'#fffaf0'
  };
  const r = (x, y, w, h, c, extra = '') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${c}"${extra}/>`;
  const rr = (x, y, w, h, c) => r(x + 1, y, w - 2, h, c) + r(x, y + 1, w, h - 2, c);
  const pts = (list, c) => list.map(([x, y]) => r(x, y, 1, 1, c)).join('');
  const glyph = (rows, x0, y0, c) => rows.map((row, j) => [...row].map((ch, i) => ch === '#' ? r(x0 + i, y0 + j, 1, 1, c) : '').join('')).join('');
  const pin = (x, y, w = 7) => `<image href="brand/kd_logo.png" x="${x}" y="${y}" width="${w}" height="${w * 0.77}" preserveAspectRatio="xMidYMid meet" style="image-rendering:pixelated"/>`;
  // a limb: outline pass (each rect grown by 1), then fill, then a 1px highlight on the first rect
  const limb = (rects, fill, light) => rects.map(([x, y, w, h]) => r(x - 1, y - 1, w + 2, h + 2, C.ol)).join('') +
    rects.map(([x, y, w, h]) => r(x, y, w, h, fill)).join('') + (light ? rects.map(([x, y, w, h]) => r(x, y, 1, h, light)).join('') : '');
  const handAt = (x, y, w = 4, h = 3) => r(x - 1, y - 1, w + 2, h + 2, C.ol) + r(x, y, w, h, C.skin) + r(x, y + h - 1, w, 1, C.skinD);

  /* ---------- body ---------- */
  const NECK = r(16, 26, 8, 6, C.ol) + r(17, 26, 6, 6, C.skin) + r(17, 26, 6, 2, C.skinD);
  const torso = (base, light, dark) =>
    r(8, 30, 24, 1, C.ol) + r(5, 31, 30, 1, C.ol) + r(3, 32, 34, 1, C.ol) + r(2, 33, 36, 15, C.ol) +
    r(8, 31, 24, 1, base) + r(5, 32, 30, 1, base) + r(3, 33, 34, 15, base) +
    r(8, 31, 24, 1, light) + r(5, 32, 3, 1, light) + r(32, 32, 3, 1, light) + r(3, 34, 2, 14, dark) + r(35, 34, 2, 14, dark);
  const PHONES = rr(6, 27, 6, 6, C.ol) + r(7, 28, 4, 4, C.phones) + r(8, 29, 1, 2, C.mint) + r(7, 28, 4, 1, C.phonesL) +
                 rr(28, 27, 6, 6, C.ol) + r(29, 28, 4, 4, C.phones) + r(31, 29, 1, 2, C.mint) + r(29, 28, 4, 1, C.phonesL) +
                 r(12, 30, 16, 1, C.phones);

  const OUTFITS = {
    // 1 — olive overshirt open over a white tee with a KD print
    overshirt: { name: 'Studio Overshirt',
      body: () => torso('#556b2f', '#6b8e23', '#3f5222') +
        r(14, 31, 12, 17, C.tee) + r(14, 31, 1, 17, C.teeD) + r(25, 31, 1, 17, C.teeD) + r(16, 31, 8, 1, C.teeD) +
        pts([[13, 32], [13, 33], [26, 32], [26, 33], [12, 34], [27, 34]], '#3f5222') +             // collar edges
        pts([[12, 38], [12, 42], [12, 46], [27, 38], [27, 42], [27, 46]], '#d6d3c4') +             // buttons
        r(5, 36, 6, 4, '#4b5e27') + r(5, 36, 6, 1, '#3f5222') + pin(16, 35, 8),
      sleeve: { base: '#556b2f', light: '#6b8e23', cuff: '#3f5222' } },

    // 2 — retro two-tone windbreaker: mint body, cream chest band, violet stripe
    windbreaker: { name: 'Retro Windbreaker',
      body: () => torso('#34d399', '#6ee7b7', '#059669') +
        r(3, 34, 34, 5, '#f3ead3') + r(3, 39, 34, 1, '#7c3aed') + r(3, 40, 34, 1, '#a78bfa') +
        r(13, 30, 14, 2, '#f3ead3') + r(13, 31, 14, 1, '#e2d6b8') +                                  // collar stand
        r(20, 31, 1, 17, '#e2e8f0') + r(19, 33, 3, 2, '#94a3b8') + pin(6, 35, 6),
      sleeve: { base: '#34d399', light: '#6ee7b7', cuff: '#f3ead3' } },

    // 3 — black hoodie, lime lightning graphic, silver chain
    blackout: { name: 'Blackout Hoodie',
      body: () => torso('#1c1c22', '#2e2e38', '#0f0f14') +
        r(10, 29, 20, 1, C.ol) + r(10, 30, 20, 3, '#26262e') + r(15, 31, 10, 2, '#0a0a0e') +          // hood rim
        r(16, 33, 1, 5, C.tip) + r(23, 33, 1, 5, C.tip) +                                           // lime strings
        pts([[14, 32], [15, 33], [16, 34], [17, 35], [18, 36], [21, 36], [22, 35], [23, 34], [24, 33], [25, 32]], '#cbd5e1') +
        r(19, 37, 2, 2, '#e5e7eb') +                                                                  // chain pendant
        glyph(['..##', '.##.', '####', '.##.', '##..'], 26, 38, C.tip) + pin(6, 36, 6),               // lightning
      sleeve: { base: '#1c1c22', light: '#2e2e38', cuff: C.tip } },

    // 4 — denim jacket with enamel pins over a white tee
    denim: { name: 'Denim + Pins',
      body: () => torso('#3b5b8c', '#5b7fb5', '#2b4468') +
        r(15, 31, 10, 17, C.tee) + r(15, 31, 10, 1, C.teeD) +
        pts([[14, 32], [13, 33], [13, 34], [25, 32], [26, 33], [26, 34]], '#2b4468') +               // collar folds
        r(14, 35, 1, 13, '#c9a15b') + r(25, 35, 1, 13, '#c9a15b') + r(5, 37, 7, 1, '#c9a15b') + r(28, 37, 7, 1, '#c9a15b') +
        pin(5, 38, 6) + glyph(['#.#.#', '.#.#.'], 29, 39, C.mint) + glyph(['.#', '##', '#.'], 32, 42, '#facc15'),
      sleeve: { base: '#3b5b8c', light: '#5b7fb5', cuff: '#2b4468' } },

    // 5 — techwear: black vest with straps and buckles over a grey long-sleeve, orange tag
    techwear: { name: 'Techwear Vest',
      body: () => torso('#6b7280', '#9ca3af', '#4b5563') +
        r(7, 32, 26, 16, '#111827') + r(7, 32, 26, 1, '#1f2937') + r(15, 31, 10, 2, '#374151') +
        pts([[9, 34], [10, 35], [11, 36], [12, 37], [13, 38], [14, 39], [15, 40], [16, 41], [17, 42]], '#4b5563') +   // strap
        r(17, 42, 3, 2, '#9ca3af') + r(26, 35, 5, 3, '#fb923c') + r(27, 36, 3, 1, '#7c2d12') +          // buckle + tag
        r(8, 44, 24, 1, C.mint) + r(22, 38, 6, 4, '#1f2937') + pin(9, 36, 5),
      sleeve: { base: '#6b7280', light: '#9ca3af', cuff: '#111827' } },
  };

  /* ---------- head ---------- */
  // swept anime spikes, each a small stack of rects; the last rect of each spike gets the lime dye
  const HAIR_SPIKES = [
    [[10, 2, 5, 3], [9, 0, 3, 2], [8, -1, 2, 1]],
    [[15, 1, 5, 3], [15, -1, 3, 2], [14, -2, 2, 1]],
    [[21, 1, 5, 3], [22, -1, 3, 2], [23, -3, 2, 2]],
    [[26, 2, 4, 3], [27, 0, 3, 2], [29, -1, 2, 1]],
    [[29, 5, 3, 4], [31, 4, 2, 2], [32, 3, 1, 1]],
  ];
  const ALL = HAIR_SPIKES.flat();
  const HEAD =
    // hair mass + spikes (outline pass then fill)
    r(9, 3, 22, 12, C.ol) + r(10, 2, 20, 1, C.ol) + ALL.map(([x, y, w, h]) => r(x - 1, y - 1, w + 2, h + 2, C.ol)).join('') +
    r(10, 3, 20, 11, C.hair) + ALL.map(([x, y, w, h]) => r(x, y, w, h, C.hair)).join('') +
    HAIR_SPIKES.map(sp => { const [x, y, w, h] = sp[sp.length - 1]; return r(x, y, w, h, C.tip); }).join('') +
    pts([[9, 0], [15, -1], [23, -2], [27, 0], [31, 4]], C.tipL) +
    pts([[13, 4], [14, 4], [15, 5], [21, 3], [22, 3], [23, 4], [18, 6], [19, 6]], C.hairL) +       // shine flicks
    // ears
    rr(8, 14, 4, 6, C.ol) + r(9, 15, 2, 4, C.skin) + r(9, 16, 1, 2, C.skinD) + rr(28, 14, 4, 6, C.ol) + r(29, 15, 2, 4, C.skin) + r(30, 16, 1, 2, C.skinD) +
    // face + jaw
    r(11, 9, 18, 16, C.skin) + r(12, 25, 16, 1, C.skin) + r(13, 26, 14, 1, C.skin) + r(15, 27, 10, 1, C.skin) +
    pts([[11, 25], [12, 26], [13, 27], [14, 27], [28, 25], [27, 26], [26, 27], [25, 27]], C.ol) + r(15, 28, 10, 1, C.ol) +
    r(27, 18, 1, 6, C.skinD) + r(12, 23, 1, 2, C.skinD) + r(27, 23, 1, 2, C.skinD) +
    // fringe swept left, lime tips
    r(11, 8, 18, 3, C.hair) + r(11, 11, 6, 1, C.hair) + r(11, 12, 4, 1, C.hair) + r(22, 11, 3, 1, C.hair) + r(26, 11, 3, 2, C.hair) +
    pts([[11, 12], [12, 12], [13, 12], [26, 12], [27, 12]], C.tip) + pts([[11, 13]], C.tipL) +
    r(10, 9, 1, 6, C.hairD) + r(29, 9, 1, 6, C.hairD) +                                            // undercut sideburns
    // nose
    pts([[21, 20], [20, 21]], C.skinD);
  const GLASSES =
    r(12, 14, 7, 1, C.frame) + r(12, 18, 7, 1, C.frame) + r(12, 15, 1, 3, C.frame) + r(18, 15, 1, 3, C.frame) +
    r(21, 14, 7, 1, C.frame) + r(21, 18, 7, 1, C.frame) + r(21, 15, 1, 3, C.frame) + r(27, 15, 1, 3, C.frame) +
    r(19, 15, 2, 1, C.frame) + r(10, 15, 2, 1, C.frame) + r(28, 15, 2, 1, C.frame) +
    r(13, 15, 5, 3, C.lens, ' fill-opacity="0.22"') + r(22, 15, 5, 3, C.lens, ' fill-opacity="0.22"') +
    pts([[13, 15]], '#ffffff') + pts([[26, 15], [26, 16]], C.hud);

  /* ---------- expressions ---------- */
  const P = C.pupil;
  const eyeL = 15, eyeR = 23;
  const EYES = {
    normal: dx => r(eyeL + dx, 15, 2, 3, P) + r(eyeR + dx, 15, 2, 3, P) + pts([[eyeL + dx, 15], [eyeR + dx, 15]], C.white),
    blink: () => r(14, 17, 4, 1, P) + r(22, 17, 4, 1, P),
    happy: () => pts([[14, 17], [15, 16], [16, 16], [17, 17], [22, 17], [23, 16], [24, 16], [25, 17]], P),
    wide: dx => r(14, 15, 4, 3, C.white) + r(22, 15, 4, 3, C.white) + r(15 + dx, 16, 2, 2, P) + r(23 + dx, 16, 2, 2, P),
    wink: dx => r(eyeL + dx, 15, 2, 3, P) + pts([[eyeL + dx, 15]], C.white) + pts([[22, 17], [23, 16], [24, 16], [25, 17]], P),
  };
  const BROWS = {
    normal: r(13, 12, 5, 1, C.hair) + r(22, 12, 5, 1, C.hair),
    up: r(13, 11, 5, 1, C.hair) + r(22, 11, 5, 1, C.hair),
    focus: pts([[13, 12], [14, 12], [15, 13], [16, 13], [17, 13], [22, 13], [23, 13], [24, 13], [25, 12], [26, 12]], C.hair),
  };
  const MOUTH = {
    closed: r(18, 23, 4, 1, C.lip),
    smile: r(18, 23, 4, 1, C.lip) + pts([[17, 22], [22, 22]], C.lip),
    grin: r(17, 22, 6, 2, C.teeth) + r(17, 24, 6, 1, C.lip) + pts([[16, 21], [23, 21]], C.lip),
    m1: r(18, 22, 4, 2, C.mouthIn) + r(19, 23, 2, 1, C.tongue),
    m2: r(18, 22, 4, 3, C.mouthIn) + r(18, 22, 4, 1, C.teeth) + r(19, 24, 2, 1, C.tongue),
    m3: r(17, 22, 6, 3, C.mouthIn) + r(17, 22, 6, 1, C.teeth) + r(18, 24, 4, 1, C.tongue),
    O: r(19, 22, 2, 1, C.mouthIn) + r(18, 23, 4, 1, C.mouthIn) + r(19, 24, 2, 1, C.mouthIn),
  };

  /* ---------- poses (arms layer) ---------- */
  const TEA = (x, y) => r(x - 1, y - 1, 6, 8, C.ol) + r(x, y, 4, 6, C.glass) + r(x, y + 1, 4, 5, C.tea) + r(x, y, 4, 1, C.foam) + r(x + 3, y + 1, 1, 5, '#f8fafc');
  const armL_rest = (s, dy = 0) => limb([[3, 33, 4, 8], [5, 39 + dy, 9, 3]], s.base, s.light) + handAt(13, 39 + dy);
  const armR_rest = (s, dy = 0) => limb([[33, 33, 4, 8], [26, 39 + dy, 9, 3]], s.base, s.light) + handAt(23, 39 + dy);
  const POSES = {
    rest: s => armL_rest(s) + armR_rest(s),
    type: (s, f) => armL_rest(s, f ? -1 : 0) + armR_rest(s, f ? 0 : -1),
    sip: s => limb([[3, 33, 4, 6], [6, 35, 3, 4], [8, 31, 3, 4], [10, 27, 3, 4]], s.base, s.light) + r(9, 27, 5, 1, s.cuff) +
              handAt(12, 23, 4, 4) + TEA(14, 19) + armR_rest(s),
    glasses: s => armL_rest(s) + limb([[33, 33, 4, 6], [31, 32, 3, 4], [29, 28, 3, 4], [27, 24, 3, 4], [25, 21, 3, 3]], s.base, s.light) +
              handAt(21, 18, 4, 3) + r(20, 15, 1, 3, C.skin) + r(19, 14, 1, 1, C.ol),
    thumb: s => limb([[3, 33, 4, 5], [4, 26, 4, 8]], s.base, s.light) + r(4, 26, 4, 1, s.cuff) + handAt(3, 21, 5, 5) + r(5, 18, 2, 3, C.skin) + r(4, 17, 4, 1, C.ol) + armR_rest(s),
    point: s => limb([[1, 33, 4, 5], [-5, 32, 8, 3]], s.base, s.light) + r(-5, 32, 1, 3, s.cuff) + handAt(-9, 32, 4, 3) + r(-12, 33, 3, 1, C.skin) + armR_rest(s),
    stretch: s => limb([[3, 24, 4, 10], [5, 14, 4, 10], [33, 24, 4, 10], [31, 14, 4, 10]], s.base, s.light) + handAt(7, 9, 4, 5) + handAt(29, 9, 4, 5),
    wave: (s, f) => armL_rest(s) + limb([[37, 15, 4, 17]], s.base, s.light) + r(37, 14, 4, 1, s.cuff) + handAt(36 + (f ? 1 : 0), 9, 6, 5) +
              r(37 + (f ? 1 : 0), 7, 1, 2, C.skin) + r(39 + (f ? 1 : 0), 6, 1, 3, C.skin) + r(41 + (f ? 1 : 0), 7, 1, 2, C.skin),
  };

  // layer: 'all' (default), 'base' (body + head only) or 'arms' (arms only) — split so desk props can sit between them
  function svg(uid, outfit = 'overshirt', layer = 'all') {
    const o = OUTFITS[outfit] || OUTFITS.overshirt;
    const base = layer !== 'arms', arms = layer !== 'base';
    return `<svg viewBox="0 0 40 48" shape-rendering="crispEdges" overflow="visible" data-outfit="${outfit}" xmlns="http://www.w3.org/2000/svg">
      ${base ? `<g class="n-body">${NECK}${o.body()}${PHONES}</g>
      <g class="n-head">${HEAD}<g class="n-brows"></g><g class="n-eyes"></g>${GLASSES}<g class="n-mouth"></g></g>` : ''}
      ${arms ? '<g class="n-arms"></g>' : ''}
    </svg>`;
  }
  function update(root, s) {
    const q = sel => root.querySelector(sel);
    const outfit = q('svg').dataset.outfit || 'overshirt';
    const sl = (OUTFITS[outfit] || OUTFITS.overshirt).sleeve;
    const lookX = s.look || 0;
    const set = (sel, html) => { const el = q(sel); if (el && el.__h !== html) { el.innerHTML = html; el.__h = html; } };
    const head = q('.n-head');
    if (head) head.setAttribute('transform', `translate(${lookX > 0 ? 1 : lookX < 0 ? -1 : 0} ${-(s.bob || 0)})`);
    set('.n-brows', BROWS[s.brow] || BROWS.normal);
    set('.n-eyes', (EYES[s.eyes] || EYES.normal)(lookX));
    set('.n-mouth', s.pose === 'sip' ? '' : (MOUTH[s.mouth] || MOUTH.closed));
    set('.n-arms', (POSES[s.pose] || POSES.rest)(sl, s.frame || 0));
  }
  return { svg, update, C, OUTFITS, POSES: Object.keys(POSES) };
})();
