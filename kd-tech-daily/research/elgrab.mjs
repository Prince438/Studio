// Screenshot a web page region: node research/elgrab.mjs <url> <out.png> [w h] [selector] [dark]
import { chromium } from 'playwright';
const [url, out, w = '1600', h = '900', sel = '', dark = ''] = process.argv.slice(2);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 2, colorScheme: dark ? 'dark' : 'light' });
await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
await p.waitForTimeout(1500);
if (sel) { const el = await p.$(sel); await el.scrollIntoViewIfNeeded(); await el.screenshot({ path: out }); }
else await p.screenshot({ path: out });
await b.close(); console.log('saved', out);
