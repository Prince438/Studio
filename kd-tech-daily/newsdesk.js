/* KD Tech Daily news desk: pixel-art desk + props, drawn in Kopi's sprite units (Kopi occupies x 0..40, y 0..48).
   The desk top surface sits at y 41..44; the front panel runs from y 44 down.
   DESK.svg(x0, x1, y1, opts) -> SVG markup covering units x0..x1 and y 26..y1 (scale it by the same factor as Kopi)
   Props Kopi picks up have classes so the page can hide them while they are in her hands:
     .d-mug (sip), .d-papers (papers / read / write), .d-pen (pen / write), .d-tablet (tablet)
   Other classes: .steam0/.steam1 (mug steam frames), .d-dock (drone pad light), .d-clock (LED clock text), .d-mon (monitor glow) */
const DESK = (() => {
  const OL = '#0a0a14';
  const r = (x, y, w, h, c, extra = '') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${c}"${extra}/>`;
  const glyph = (rows, x0, y0, c) => rows.map((row, j) => [...row].map((ch, i) => ch === '#' ? r(x0 + i, y0 + j, 1, 1, c) : '').join('')).join('');

  // desk mic on a short stand with a KD mic flag
  const MIC = (x) => r(x - 1, 40, 7, 2, OL) + r(x, 40, 5, 1, '#2b3238') +             // base
    r(x + 2, 34, 1, 6, '#6b757c') +                                                      // stem
    r(x, 30, 5, 5, OL) + r(x + 1, 30, 3, 4, '#1f2933') + r(x + 1, 30, 3, 1, '#4b5560') +   // head
    r(x - 1, 34, 7, 4, OL) + r(x, 34, 5, 3, '#0f3a20') + glyph(['#.##', '##.#', '#.##'], x + 1, 34, '#4ade80');  // flag
  // laptop seen from behind: lid with a KD sticker; .d-mon glows on the desk
  const LAPTOP = (x) => r(x - 1, 27, 17, 14, OL) + r(x, 28, 15, 12, '#c5ccd3') + r(x, 28, 15, 1, '#e3e8ec') + r(x, 38, 15, 2, '#a9b2bb') +
    r(x + 4, 31, 7, 5, OL) + `<image href="brand/kd_logo.png" x="${x + 4.5}" y="${31.4}" width="6" height="4.2" style="image-rendering:pixelated"/>` +
    r(x + 1, 30, 2, 2, '#ff6fa3') + r(x + 12, 34, 2, 2, '#ffc940') +                    // stickers
    r(x - 3, 40, 21, 2, OL) + r(x - 2, 40, 19, 1, '#8a949b') +
    `<rect class="d-mon" x="${x - 3}" y="41" width="21" height="1" fill="#4ade80" opacity="0.35"/>`;
  // LED desk clock
  const CLOCK = (x) => r(x - 1, 34, 12, 8, OL) + r(x, 35, 10, 6, '#05140b') + r(x, 35, 10, 1, '#0f2a18') +
    `<text class="d-clock" x="${x + 5}" y="39.6" font-family="Pix" font-size="3.6" text-anchor="middle" fill="#4ade80">08:00</text>`;
  // script papers: a short stack lying on the desk, with a pen on top
  const PAPERS = (x) => `<g class="d-papers">${r(x - 0.5, 39.2, 13, 2.6, OL)}${r(x, 39.6, 12, 0.7, '#f8fafc')}${r(x + 0.4, 40.3, 11.6, 0.7, '#dfe5ea')}${r(x, 41, 12, 0.5, '#c7ced5')}</g>` +
    `<g class="d-pen">${r(x + 3, 38.6, 7, 0.9, OL)}${r(x + 3.3, 38.7, 5, 0.6, '#4ade80')}${r(x + 8.3, 38.7, 1.4, 0.6, '#e5e7eb')}</g>`;
  // tablet lying flat
  const TABLET = (x) => `<g class="d-tablet">${r(x - 0.5, 39.6, 10, 2, OL)}${r(x, 40, 9, 1.2, '#1f2937')}${r(x + 1, 40.2, 7, 0.6, '#2f8f5b')}</g>`;
  // the KOPI mug (coffee, obviously) + two steam frames
  const MUG = (x) => `<g class="d-mug">${r(x - 1, 33.5, 7, 8.5, OL)}${r(x + 5, 35, 2.5, 4, OL)}${r(x, 34, 5, 7, '#f4f1ea')}${r(x + 5, 36, 1.2, 2, '#f4f1ea')}` +
    `${r(x, 34, 5, 1, '#6b3f22')}${r(x, 36, 5, 2, '#4ade80')}${r(x + 1, 36, 1, 2, '#16a34a')}${r(x + 4, 35, 1, 6, '#cfcac0')}` +
    `<g class="steam0">${r(x + 1, 31, 1, 1, '#8a969e')}${r(x + 2, 32, 1, 1, '#8a969e')}${r(x + 3, 30, 1, 1, '#8a969e')}</g>` +
    `<g class="steam1" display="none">${r(x + 2, 31, 1, 1, '#8a969e')}${r(x + 1, 32, 1, 1, '#8a969e')}${r(x + 3, 31, 1, 1, '#8a969e')}${r(x + 2, 29, 1, 1, '#8a969e')}</g></g>`;
  // succulent in a pot
  const PLANT = (x) => glyph(['...#....', '..###.#.', '#.###.##', '##.#.##.', '.#####..', '..###...'], x, 30, '#16a34a') +
    glyph(['...#....', '..#.....', '#...#.#.', '.#....#.'], x, 31, '#4ade80') +
    r(x, 36, 8, 2, OL) + r(x + 1, 36, 6, 1, '#e07a52') + r(x + 1, 37, 6, 5, OL) + r(x + 2, 37, 4, 4, '#c9643f') + r(x + 2, 37, 1, 4, '#e58b63');
  // drone dock pad with a ring light
  const DOCK = (x) => r(x - 1, 39, 11, 3, OL) + r(x, 39.5, 9, 1.6, '#2b3238') + `<rect class="d-dock" x="${x + 1}" y="39.5" width="7" height="0.7" fill="#4ade80"/>`;

  function svg(x0, x1, y1 = 74, opts = {}) {
    const W = x1 - x0, H = y1 - 26;
    const front = opts.front || '';
    return `<svg viewBox="${x0} 26 ${W} ${H}" width="100%" height="100%" shape-rendering="crispEdges" overflow="visible" xmlns="http://www.w3.org/2000/svg">
      ${opts.clock !== false ? CLOCK(-37) : ''}${LAPTOP(-25)}${MIC(-8)}${PAPERS(8)}${MUG(40)}${TABLET(48)}${PLANT(59)}${DOCK(68)}
      ${r(x0, 41, W, 1, '#7b868e')}${r(x0, 42, W, 2, '#46515a')}${r(x0, 44, W, 1, OL)}
      ${r(x0, 45, W, y1 - 45, 'url(#dfg)')}
      <defs><linearGradient id="dfg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#11241a"/><stop offset="1" stop-color="#050a07"/></linearGradient></defs>
      ${r(x0, 45, W, 0.6, '#4ade80', ' opacity="0.55"')}${front}
    </svg>`;
  }
  return { svg };
})();
