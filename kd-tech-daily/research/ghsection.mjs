// Screenshot a page scrolled to the first heading matching text: node research/ghsection.mjs <url> <out> <text> [w h] [dark]
import { chromium } from 'playwright';
const [url, out, text, w = '1600', h = '900', dark = 'dark'] = process.argv.slice(2);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 2, colorScheme: dark ? 'dark' : 'light' });
await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
const y = await p.evaluate(t => { const el = [...document.querySelectorAll('h1,h2,h3,h4')].find(e => e.textContent.toLowerCase().includes(t.toLowerCase())); if (!el) return -1; el.scrollIntoView(); window.scrollBy(0, -40); return scrollY; }, text);
await p.waitForTimeout(800); await p.screenshot({ path: out }); await b.close(); console.log('y', y, 'saved', out);
