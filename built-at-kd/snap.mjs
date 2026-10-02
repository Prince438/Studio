// Grab still frames at given times: node snap.mjs 1.5 8 13.9 ...
let pw; try { pw = await import('playwright'); } catch { pw = await import('/home/claude/.npm-global/lib/node_modules/playwright/index.mjs'); }
const { chromium } = pw;
import path from 'path';
import { pathToFileURL } from 'url';
const times = process.argv.slice(2).map(Number);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
const errs = [];
page.on('pageerror', e => errs.push(e.message));
page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
await page.goto(pathToFileURL(path.resolve(process.env.PAGE || 'index.html')).href);
await page.waitForFunction(() => window.__ready === true, null, { timeout: 20000 });
const [vw, vh] = await page.evaluate(() => [window.__W || 1080, window.__H || 1920]);
await page.setViewportSize({ width: vw, height: vh });
for (const t of times) {
  await page.evaluate(t => window.__seek(t), t);
  await page.screenshot({ path: `snaps/t${String(t).padStart(5, '0')}.png`, type: 'png' });
}
if (errs.length) console.log('ERRORS:\n' + errs.join('\n'));
console.log('events:', await page.evaluate(() => window.__EVENTS.length));
await browser.close();
