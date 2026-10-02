/* Desk props for the Built at KD studio, drawn as pixel art on a unit grid (scale them by whole numbers). */
const PROPS = (() => {
  const INK = '#16131c';
  const r = (x, y, w, h, c, extra = '') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${c}"${extra}/>`;
  const rr = (x, y, w, h, c) => r(x + 1, y, w - 2, h, c) + r(x, y + 1, w, h - 2, c);
  const glyph = (rows, x0, y0, c) => rows.map((row, j) => [...row].map((ch, i) => ch === '#' ? r(x0 + i, y0 + j, 1, 1, c) : '').join('')).join('');
  const svg = (w, h, body) => `<svg viewBox="0 0 ${w} ${h}" shape-rendering="crispEdges" overflow="visible" xmlns="http://www.w3.org/2000/svg">${body}</svg>`;

  /* mechanical keyboard 30x9; KEYS lists every cap so typing can light a few up */
  const KEYS = [];
  for (let x = 2; x <= 26; x += 3) KEYS.push([x, 2, 2]);
  for (let x = 3; x <= 23; x += 3) KEYS.push([x, 4, 2]);
  KEYS.push([26, 4, 2]);
  KEYS.push([2, 6, 3], [7, 6, 14], [23, 6, 2], [26, 6, 2]);
  const capColor = (i, k) => (i === 0 ? '#c9b8ff' : k[1] === 4 && k[0] === 26 ? '#4ade80' : k[2] === 3 ? '#c9b8ff' : (i % 5 === 2 ? '#ffe8a3' : '#f1e9d8'));
  const keyboard = () => svg(30, 9,
    rr(0, 0, 30, 9, INK) + r(1, 1, 28, 7, '#2a2e38') + r(1, 1, 28, 1, '#3a3f4c') +
    KEYS.map((k, i) => r(k[0], k[1], k[2], 1, capColor(i, k))).join('') +
    `<g class="kb-hot"></g>` + `<rect class="kb-rgb" x="1" y="7" width="28" height="1" fill="#4ade80"/>`);
  const hotKeys = (list) => list.map(i => { const k = KEYS[i % KEYS.length]; return r(k[0], k[1], k[2], 1, '#ffffff') + r(k[0], k[1] + 1, k[2], 1, '#4ade80', ' fill-opacity="0.6"'); }).join('');

  /* teh tarik glass 6x9 (sits on the desk until Kenji picks it up) */
  const glass = () => svg(6, 9,
    rr(0, 0, 6, 9, INK) + r(1, 1, 4, 7, '#e8edf2') + r(1, 3, 4, 5, '#d4a26c') + r(1, 6, 4, 2, '#bf8750') +
    r(1, 2, 4, 1, '#fff6e3') + r(4, 3, 1, 4, '#f0d2a8') + r(1, 1, 4, 1, '#ffffff', ' fill-opacity="0.7"'));

  /* laptop seen from behind, lid covered in stickers 34x22 */
  const laptop = () => svg(34, 22,
    rr(0, 0, 34, 20, INK) + r(1, 1, 32, 18, '#d7dce4') + r(1, 1, 32, 1, '#eef1f5') + r(1, 16, 32, 3, '#bcc4cf') +
    rr(3, 3, 8, 6, INK) + r(4, 4, 6, 4, '#4ade80') + glyph(['.#..#.', '#.##.#', '.#..#.'], 4, 4, INK) +            // </> sticker
    rr(12, 5, 11, 9, INK) + r(13, 6, 9, 7, '#101216') +
    `<image href="brand/kd_logo.png" x="13.5" y="6.8" width="8" height="5.4" preserveAspectRatio="xMidYMid meet" style="image-rendering:pixelated"/>` +
    glyph(['.#.#.', '#####', '#####', '.###.', '..#..'], 26, 3, '#ff7aa8') +                                        // heart
    glyph(['..#..', '.###.', '#####', '.###.', '.#.#.'], 4, 11, '#f5b400') +                                        // star
    rr(24, 11, 7, 4, INK) + r(25, 12, 5, 2, '#c9b8ff') +                                                           // lilac tag
    rr(-2, 19, 38, 3, INK) + r(-1, 20, 36, 1, '#9aa3b0'));

  /* succulent in a terracotta pot 10x14 */
  const plant = () => svg(10, 14,
    glyph(['....#.....', '...###..#.', '.#.###.##.', '.##.#.##..', '..#####...', '...###....'], 0, 0, '#16a34a') +
    glyph(['....#.....', '...#......', '.#...#.#..', '.#......#.', '..#.#.....'], 0, 1, '#4ade80') +
    rr(1, 6, 8, 2, INK) + r(2, 6, 6, 2, '#e07a52') + rr(2, 8, 6, 6, INK) + r(3, 8, 4, 5, '#c9643f') + r(3, 8, 1, 5, '#e58b63'));

  /* RGB cube lamp 7x9 (colour set per frame) */
  const cube = () => svg(7, 9,
    rr(0, 0, 7, 7, INK) + `<rect class="cube-in" x="1" y="1" width="5" height="5" fill="#4ade80"/>` + r(1, 1, 5, 1, '#ffffff', ' fill-opacity="0.45"') +
    r(2, 3, 1, 1, '#ffffff', ' fill-opacity="0.6"') + rr(0, 7, 7, 2, INK) + r(1, 7, 5, 1, '#3a3f4c'));

  /* rubber debugging duck 9x8 */
  const duck = () => svg(9, 8,
    glyph(['...###...', '..#####..', '..##.##..', '..#####..', '########.', '#########', '.#######.', '..#####..'], 0, 0, INK) +
    glyph(['.........', '...###...', '...#.#...', '...###...', '.######..', '.#######.', '..#####..', '.........'], 0, 0, '#facc15') +
    r(4, 2, 1, 1, INK) + r(6, 3, 2, 1, '#fb923c') + r(3, 1, 1, 1, '#fef08a') + r(2, 5, 2, 1, '#eab308'));

  /* 4-point pixel sparkle 7x7 */
  const sparkle = (c = '#4ade80') => svg(7, 7, r(3, 0, 1, 7, c) + r(0, 3, 7, 1, c) + r(2, 2, 3, 3, c) + r(3, 3, 1, 1, '#ffffff'));

  /* "!" pop above a head 3x7 */
  const bang = () => svg(5, 9, rr(0, 0, 5, 6, INK) + r(1, 1, 3, 4, '#ffe8a3') + rr(0, 6, 5, 3, INK) + r(1, 7, 3, 1, '#ffe8a3'));

  return { keyboard, hotKeys, KEYS, glass, laptop, plant, cube, duck, sparkle, bang };
})();
