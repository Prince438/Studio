/* KD Hot Topic newsroom (original art).
   ROOM.sky(ctx, W, H, t, opts)  paints the view through the giant window: Kuala Lumpur at dusk in pixel art
                                 (Petronas Twin Towers, Menara KL, Merdeka 118 and the city), drawn into a small
                                 canvas that the page scales up with image-rendering: pixelated.
                                 opts: { horizon, petronas: x, menara: x, merdeka: x }  (all in canvas pixels)
   ROOM.desk(x0, x1, y1)         curved anchor desk + props as SVG in sprite units: Kopi sits at x 0..40, Kenji at
                                 x 64..104 (both 48 units tall, desk top at y 41). Props the anchors pick up carry
                                 classes so the page can hide them: .d-mug .d-papers .d-pen .d-tablet (Kopi), .d-tea (Kenji). */
const ROOM = (() => {
  /* ---------------- the window view ---------------- */
  const rnd = seed => () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  const SKY = ['#120f2e', '#1b1640', '#2a1b55', '#3f1f66', '#5b2470', '#7d2c72', '#a43a6c', '#c94e63', '#e4675a', '#f58a55', '#ffb066'];
  const BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]];
  let cache = null;
  function build(W, H, o) {
    const hz = o.horizon, R = rnd(11), city = [];
    // background city blocks (two layers), skipping the landmark slots
    for (const layer of [0, 1]) {
      let x = -4;
      while (x < W + 4) {
        const w = 6 + Math.floor(R() * (layer ? 14 : 10)), h = (layer ? 18 : 10) + Math.floor(R() * (layer ? 46 : 30));
        city.push({ x, w, h, layer, seed: Math.floor(R() * 1e6) }); x += w + (layer ? 1 + Math.floor(R() * 4) : 0);
      }
    }
    const stars = Array.from({ length: Math.round(W * H / 900) }, () => ({ x: Math.floor(R() * W), y: Math.floor(R() * hz * 0.45), p: R() }));
    const clouds = Array.from({ length: 5 }, (_, i) => ({ x: R() * W, y: Math.floor(hz * (0.18 + R() * 0.32)), w: 26 + Math.floor(R() * 40), v: 0.6 + R() * 0.8 }));
    return { W, H, o, city, stars, clouds };
  }
  function px(g, x, y, w, h, c) { g.fillStyle = c; g.fillRect(Math.round(x), Math.round(y), Math.round(w), Math.round(h)); }
  function windows(g, x, y, w, h, seed, t, cols = ['rgba(255,214,140,.85)', 'rgba(150,220,255,.7)']) {
    for (let wy = y + 2; wy < y + h - 1; wy += 3) for (let wx = x + 1; wx < x + w - 1; wx += 2) {
      const k = Math.sin(wx * 12.9898 + wy * 78.233 + seed) * 43758.5453, f = k - Math.floor(k);
      if (f > 0.58 && Math.sin(t * 0.5 + f * 50) > -0.9) px(g, wx, wy, 1, 1, f > 0.92 ? cols[1] : cols[0]);
    }
  }
  function petronas(g, cx, hz, t) {
    // twin 88-storey towers: stacked tiers that step in, pinnacles, double-decker skybridge
    const tiers = [[16, 46], [14, 22], [12, 16], [10, 12], [8, 9], [6, 7], [4, 5]];
    for (const dx of [-15, 15]) {
      let y = hz;
      for (const [w, h] of tiers) {
        px(g, cx + dx - w / 2, y - h, w, h, '#8e98ad'); px(g, cx + dx - w / 2, y - h, 2, h, '#c9d2e3'); px(g, cx + dx + w / 2 - 2, y - h, 2, h, '#5d6578');
        for (let wy = y - h + 1; wy < y - 1; wy += 2) px(g, cx + dx - w / 2 + 3, wy, w - 6, 1, (Math.floor(wy + t * 2) % 7) ? 'rgba(255,244,214,.55)' : 'rgba(255,255,255,.95)');
        y -= h;
      }
      px(g, cx + dx - 1, y - 20, 2, 20, '#c9d2e3'); px(g, cx + dx - 2, y - 9, 4, 3, '#dfe6f2'); px(g, cx + dx, y - 26, 1, 6, '#e5ebf5');
      if (Math.floor(t * 1.4 + (dx > 0 ? 0.5 : 0)) % 2) px(g, cx + dx, y - 27, 1, 1, '#ff3b3b');
    }
    const by = hz - 52; px(g, cx - 8, by, 16, 3, '#aab3c5'); px(g, cx - 8, by + 1, 16, 1, 'rgba(255,240,200,.9)');
    for (let i = 0; i < 6; i++) { px(g, cx - 8 + i, by + 3 + i, 1, 1, '#7b8498'); px(g, cx + 7 - i, by + 3 + i, 1, 1, '#7b8498'); }
  }
  function menara(g, cx, hz, t) {
    // Menara KL: tapering shaft, the head pod, antenna
    px(g, cx - 4, hz - 6, 8, 6, '#6f6a86'); px(g, cx - 2, hz - 78, 4, 72, '#8a84a3'); px(g, cx - 2, hz - 78, 1, 72, '#b3add0');
    px(g, cx - 6, hz - 92, 12, 3, '#9c96b8'); px(g, cx - 8, hz - 89, 16, 7, '#a7a1c4'); px(g, cx - 7, hz - 87, 14, 2, 'rgba(160,255,230,.9)');
    px(g, cx - 6, hz - 82, 12, 4, '#7f799b'); px(g, cx - 4, hz - 96, 8, 4, '#8a84a3'); px(g, cx - 1, hz - 122, 2, 26, '#c7c1e0'); px(g, cx, hz - 130, 1, 8, '#e6e1ff');
    if (Math.floor(t * 1.7) % 2) px(g, cx, hz - 131, 1, 1, '#ff3b3b');
  }
  function merdeka(g, cx, hz, t) {
    // Merdeka 118: faceted glass tower narrowing into a long spire
    for (let y = 0; y < 140; y++) {
      const w = Math.max(4, Math.round(18 - y * 0.1 - (y > 110 ? (y - 110) * 0.35 : 0)));
      const facet = (Math.floor((y + 3) / 9) % 2) ? '#6c86a8' : '#5a7396';
      px(g, cx - w / 2, hz - y - 1, w, 1, facet); px(g, cx - w / 2, hz - y - 1, 1, 1, '#a9c2e2');
      if (y % 3 === 0 && y < 120) px(g, cx - w / 2 + 2, hz - y - 1, Math.max(1, w - 4), 1, (Math.floor(y / 3 + t) % 5) ? 'rgba(170,215,255,.45)' : 'rgba(255,250,220,.9)');
    }
    px(g, cx - 1, hz - 178, 2, 38, '#b9cbe2'); px(g, cx, hz - 186, 1, 8, '#e3ecf8');
    if (Math.floor(t * 1.2 + 0.3) % 2) px(g, cx, hz - 187, 1, 1, '#ff3b3b');
  }
  function sky(g, W, H, t, opts = {}) {
    const o = Object.assign({ horizon: Math.round(H * 0.7), petronas: Math.round(W * 0.82), menara: Math.round(W * 0.2), merdeka: Math.round(W * 0.09) }, opts);
    if (!cache || cache.W !== W || cache.H !== H) cache = build(W, H, o);
    const hz = o.horizon;
    // static sky (dusk gradient with ordered dithering + sun glow), painted once into an offscreen canvas
    if (!cache.bg) {
      const cv = document.createElement('canvas'); cv.width = W; cv.height = H; const b = cv.getContext('2d'), im = b.createImageData(W, H);
      const hex = c => [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16)), band = hz / (SKY.length - 1);
      for (let y = 0; y < hz; y++) {
        const f = y / band, i = Math.min(SKY.length - 2, Math.floor(f)), a = f - i;
        for (let x = 0; x < W; x++) { const c = hex(a > BAYER[y % 4][x % 4] / 16 ? SKY[i + 1] : SKY[i]), p = (y * W + x) * 4; im.data[p] = c[0]; im.data[p + 1] = c[1]; im.data[p + 2] = c[2]; im.data[p + 3] = 255; }
      }
      b.putImageData(im, 0, 0);
      const sx = W * 0.62;
      for (let rr = 26; rr > 0; rr -= 2) { b.fillStyle = `rgba(255,${150 + rr * 2},${90 + rr},${0.05 + (26 - rr) * 0.006})`; b.beginPath(); b.arc(sx, hz - 4, rr * 1.6, 0, Math.PI * 2); b.fill(); }
      cache.bg = cv;
    }
    g.drawImage(cache.bg, 0, 0);
    // stars, drifting clouds, a plane
    for (const s of cache.stars) if (Math.sin(t * 2 + s.p * 40) > -0.2) px(g, s.x, s.y, 1, 1, s.p > 0.8 ? '#ffffff' : 'rgba(255,255,255,.55)');
    for (const c of cache.clouds) {
      const x = ((c.x + t * c.v) % (W + c.w * 2)) - c.w;
      px(g, x, c.y, c.w, 2, 'rgba(255,170,190,.35)'); px(g, x + 6, c.y - 2, c.w - 14, 2, 'rgba(255,190,200,.28)'); px(g, x + 3, c.y + 2, c.w - 8, 1, 'rgba(120,70,140,.35)');
    }
    const pxp = ((t * 9) % (W + 60)) - 30, pyp = hz * 0.22 + Math.sin(t * 0.3) * 2;
    px(g, pxp, pyp, 3, 1, '#d9dce8'); if (Math.floor(t * 2.5) % 2) px(g, pxp + 3, pyp, 1, 1, '#ff4d5e'); else px(g, pxp - 1, pyp, 1, 1, '#4ade80');
    // far hills + haze, then the city
    for (let x = 0; x < W; x++) { const h = 6 + Math.round(4 * Math.sin(x * 0.03) + 3 * Math.sin(x * 0.11 + 1)); px(g, x, hz - h, 1, h, '#3b2457'); }
    for (const b of cache.city) if (!b.layer) { px(g, b.x, hz - b.h, b.w, b.h, '#4a2e63'); windows(g, b.x, hz - b.h, b.w, b.h, b.seed, t, ['rgba(255,190,140,.35)', 'rgba(200,170,255,.3)']); }
    merdeka(g, o.merdeka, hz, t); menara(g, o.menara, hz, t);
    for (const b of cache.city) if (b.layer) {
      if (Math.abs(b.x + b.w / 2 - o.petronas) < 34 || Math.abs(b.x + b.w / 2 - o.merdeka) < 12 || Math.abs(b.x + b.w / 2 - o.menara) < 8) continue;
      px(g, b.x, hz - b.h, b.w, b.h, '#2a1d40'); px(g, b.x, hz - b.h, b.w, 1, '#3d2c5a'); windows(g, b.x, hz - b.h, b.w, b.h, b.seed, t);
      if (b.h > 48 && Math.floor(t * 1.3 + b.seed) % 2) px(g, b.x + Math.floor(b.w / 2), hz - b.h - 1, 1, 1, '#ff3b3b');
    }
    petronas(g, o.petronas, hz, t);
    // street glow
    for (let y = hz; y < H; y++) px(g, 0, y, W, 1, y === hz ? '#ffb066' : `rgba(${40 + (H - y)},${20 + (H - y) / 2},60,1)`);
  }

  /* ---------------- the curved desk ---------------- */
  const OL = '#0a0a14';
  const r = (x, y, w, h, c, extra = '') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${c}"${extra}/>`;
  const glyph = (rows, x0, y0, c) => rows.map((row, j) => [...row].map((ch, i) => ch === '#' ? r(x0 + i, y0 + j, 1, 1, c) : '').join('')).join('');
  const CX = 52, HALF = 76, DEPTH = 6, L0 = -24, R0 = 128;
  const front = x => { const u = Math.max(-1, Math.min(1, (x - CX) / HALF)); return 44 + DEPTH * (1 - u * u); };   // front edge bulges toward camera
  const arc = (y, d = DEPTH) => `M${L0} ${y} Q${CX} ${y + 2 * d} ${R0} ${y}`;                                    // a curve parallel to the front edge
  // Kopi's props (same spots as her Tech Daily desk, so her poses pick them up naturally)
  const MIC = (x, flag) => r(x - 1, 40, 7, 2, OL) + r(x, 40, 5, 1, '#2b3238') + r(x + 2, 34, 1, 6, '#6b757c') +
    r(x, 30, 5, 5, OL) + r(x + 1, 30, 3, 4, '#1f2933') + r(x + 1, 30, 3, 1, '#4b5560') + r(x - 1, 34, 7, 4, OL) + r(x, 34, 5, 3, flag) +
    glyph(['#.##', '##.#', '#.##'], x + 1, 34, '#ffffff');
  const PAPERS = x => `<g class="d-papers">${r(x - 0.5, 39.2, 13, 2.6, OL)}${r(x, 39.6, 12, 0.7, '#f8fafc')}${r(x + 0.4, 40.3, 11.6, 0.7, '#dfe5ea')}${r(x, 41, 12, 0.5, '#c7ced5')}</g>` +
    `<g class="d-pen">${r(x + 3, 38.6, 7, 0.9, OL)}${r(x + 3.3, 38.7, 5, 0.6, '#ff7a3d')}${r(x + 8.3, 38.7, 1.4, 0.6, '#e5e7eb')}</g>`;
  const TABLET = x => `<g class="d-tablet">${r(x - 0.5, 39.6, 10, 2, OL)}${r(x, 40, 9, 1.2, '#1f2937')}${r(x + 1, 40.2, 7, 0.6, '#ff7a3d')}</g>`;
  const MUG = x => `<g class="d-mug">${r(x - 1, 33.5, 7, 8.5, OL)}${r(x + 5, 35, 2.5, 4, OL)}${r(x, 34, 5, 7, '#f4f1ea')}${r(x + 5, 36, 1.2, 2, '#f4f1ea')}` +
    `${r(x, 34, 5, 1, '#6b3f22')}${r(x, 36, 5, 2, '#4ade80')}${r(x + 1, 36, 1, 2, '#16a34a')}${r(x + 4, 35, 1, 6, '#cfcac0')}` +
    `<g class="steam0">${r(x + 1, 31, 1, 1, '#8a969e')}${r(x + 2, 32, 1, 1, '#8a969e')}${r(x + 3, 30, 1, 1, '#8a969e')}</g>` +
    `<g class="steam1" display="none">${r(x + 2, 31, 1, 1, '#8a969e')}${r(x + 1, 32, 1, 1, '#8a969e')}${r(x + 3, 31, 1, 1, '#8a969e')}${r(x + 2, 29, 1, 1, '#8a969e')}</g></g>`;
  // Kenji's props: teh tarik (glass, layered tea + foam), RGB keyboard, rubber duck
  const TEA = x => `<g class="d-tea">${r(x - 1, 33, 6, 9, OL)}${r(x, 34, 4, 7, '#e5e7eb')}${r(x, 35, 4, 6, '#e8c9a0')}${r(x, 34, 4, 1, '#fffaf0')}${r(x + 3, 35, 1, 6, '#f8fafc')}</g>`;
  const KEYS = x => r(x - 1, 39.5, 22, 3, OL) + r(x, 40, 20, 2, '#23262d') +
    Array.from({ length: 10 }, (_, i) => r(x + 0.5 + i * 2, 40.3, 1.4, 0.7, ['#ff4d6d', '#ff9f43', '#ffd84d', '#4ade80', '#22d3ee', '#818cf8', '#c084fc', '#ff4d6d', '#ff9f43', '#4ade80'][i])).join('') +
    `<rect class="d-rgb" x="${x}" y="41.2" width="20" height="0.5" fill="#4ade80" opacity="0.7"/>`;
  const DUCK = x => r(x - 1, 35, 8, 7, OL) + r(x, 37, 6, 4, '#ffd84d') + r(x + 3, 35, 3, 3, '#ffd84d') + r(x + 6, 36, 2, 1, '#ff9f43') + r(x + 4, 36, 1, 1, OL) + r(x, 40, 6, 1, '#e8b923');
  // the topic props: a magic 8-ball (decisions!) and YES / NO buzzers
  const EIGHT = x => r(x + 1, 34, 6, 1, OL) + r(x, 35, 8, 6, OL) + r(x + 1, 41, 6, 1, OL) + r(x + 1, 35, 6, 6, '#16161d') + r(x + 2, 35, 2, 1, '#4a4a58') +
    r(x + 3, 37, 2, 2, '#f4f1ea') + `<text x="${x + 4}" y="38.75" font-family="Pix" font-size="1.7" text-anchor="middle" fill="#16161d">8</text>` + r(x + 1, 42, 6, 0.6, 'rgba(0,0,0,.4)');
  const BUZZ = (x, c, label, d = 3.5) => r(x - 1, 42 + d, 9, 2.4, OL) + r(x, 42.4 + d, 7, 1.6, '#2b3238') + r(x + 1, 40.6 + d, 5, 2, OL) + `<rect class="d-buzz" x="${x + 1.5}" y="${41 + d}" width="4" height="1.4" fill="${c}"/>` +
    `<text x="${x + 3.5}" y="${43.75 + d}" font-family="Pix" font-size="1.2" text-anchor="middle" fill="#cfd8dc">${label}</text>`;

  function desk(x0, x1, y1 = 74) {
    const W = x1 - x0, H = y1 - 26, cf = front(CX), P = 17;     // P = front panel height
    // smooth vector body (top surface, curved front panel, LED strips); the props stay pixel art
    const body = `<g shape-rendering="geometricPrecision">
      <defs><linearGradient id="dtop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b4756"/><stop offset="1" stop-color="#232c37"/></linearGradient>
        <linearGradient id="dfr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c2531"/><stop offset=".55" stop-color="#121922"/><stop offset="1" stop-color="#0a0e13"/></linearGradient>
        <filter id="dglow" x="-5%" y="-200%" width="110%" height="500%"><feGaussianBlur stdDeviation="0.6"/></filter></defs>
      <path d="M${L0} 41 L${R0} 41 L${R0} 44 Q${CX} ${44 + 2 * DEPTH} ${L0} 44 Z" fill="url(#dtop)" stroke="${OL}" stroke-width="0.4"/>
      <path d="M${L0} 41.3 L${R0} 41.3" stroke="#56657a" stroke-width="0.5"/>
      <path d="${arc(44)} L${R0} ${44 + P} Q${CX} ${44 + P + 2 * DEPTH} ${L0} ${44 + P} Z" fill="url(#dfr)" stroke="${OL}" stroke-width="0.5"/>
      <path d="${arc(44.3)}" stroke="#b9c6d3" stroke-width="0.5" fill="none"/>
      <path d="${arc(46.4)}" stroke="#4ade80" stroke-width="1.6" fill="none" opacity="0.45" filter="url(#dglow)"/><path d="${arc(46.4)}" stroke="#86efac" stroke-width="0.45" fill="none"/>
      <path d="${arc(44 + P - 2.4)}" stroke="#ff7a3d" stroke-width="1.4" fill="none" opacity="0.4" filter="url(#dglow)"/><path d="${arc(44 + P - 2.4)}" stroke="#ffb38a" stroke-width="0.4" fill="none"/>
      <path d="${arc(48.5)} L${R0} ${44 + P - 4} Q${CX} ${44 + P - 4 + 2 * DEPTH} ${L0} ${44 + P - 4} Z" fill="rgba(255,255,255,0.025)"/>
    </g>`;
    const plate = (x, name) => { const y = front(x) + 7; return r(x - 10, y, 20, 5, '#0b0f14') + r(x - 10, y, 20, 0.5, '#4ade80') + `<text x="${x}" y="${y + 3.6}" font-family="Pix" font-weight="700" font-size="2.4" text-anchor="middle" fill="#e8f0ea">${name}</text>`; };
    return `<svg viewBox="${x0} 26 ${W} ${H}" width="100%" height="100%" shape-rendering="crispEdges" overflow="visible" xmlns="http://www.w3.org/2000/svg">
      ${MIC(-9, '#0f3a20')}${TABLET(-21)}${PAPERS(8)}${MUG(40)}${EIGHT(48)}
      ${TEA(62)}${KEYS(72)}${MIC(97, '#7c2d12')}${DUCK(106)}
      ${body}
      ${BUZZ(42, '#22c55e', 'YES')}${BUZZ(55, '#ef4444', 'NO')}
      <image href="brand/kd_logo.png" x="${CX - 9}" y="${cf + 4}" width="7" height="5.4" style="image-rendering:pixelated"/>
      <text x="${CX + 4}" y="${cf + 7.2}" font-family="Pix" font-weight="700" font-size="2.6" text-anchor="middle" fill="#ff7a3d">HOT</text>
      <text x="${CX + 4}" y="${cf + 9.8}" font-family="Pix" font-weight="700" font-size="2.6" text-anchor="middle" fill="#e8f0ea">TOPIC</text>
      ${plate(20, 'KOPI')}${plate(84, 'KENJI')}
    </svg>`;
  }
  return { sky, desk, front };
})();
