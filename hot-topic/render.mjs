// Frame-accurate renderer: seeks the page's timeline frame by frame and pipes JPEGs into ffmpeg.
// usage: node render.mjs [workers=2]        (FMT=916 renders the 9:16 version into out-916/)
let pw; try { pw = await import('playwright'); } catch { pw = await import('/home/claude/.npm-global/lib/node_modules/playwright/index.mjs'); }
const { chromium } = pw;
import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
import { pathToFileURL } from 'url';

const WORKERS = Number(process.argv[2] || 2);
const OUT = process.env.FMT === '916' ? 'out-916' : 'out';
fs.mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch();

async function openPage() {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('pageerror', e => console.error('PAGE ERROR', e.message));
  await page.goto(pathToFileURL(path.resolve(process.env.PAGE || 'index.html')).href + (process.env.FMT === '916' ? '?fmt=916' : ''));
  await page.waitForFunction(() => window.__ready === true, null, { timeout: 30000 });
  const [w, h] = await page.evaluate(() => [window.__W || 1080, window.__H || 1920]);
  await page.setViewportSize({ width: w, height: h });
  return page;
}

const probe = await openPage();
const { dur, fps, events, music } = await probe.evaluate(() => ({ dur: window.__DURATION, fps: window.__FPS, events: window.__EVENTS, music: window.__MUSIC || null }));
fs.writeFileSync(`${OUT}/events.json`, JSON.stringify(events));
if (music) fs.writeFileSync(`${OUT}/music.json`, JSON.stringify(music));   // song length + sections for audio.py
await probe.close();
const total = Math.round(dur * fps);
const per = Math.ceil(total / WORKERS);
console.log(`frames=${total} fps=${fps} workers=${WORKERS}`);

let done = 0; const t0 = Date.now();
async function worker(w) {
  const page = await openPage();
  const a = w * per, b = Math.min(total, a + per);
  const seg = `${OUT}/seg${w}.mp4`;
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-tune', 'animation', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', String(fps), seg], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = a; f < b; f++) {
    await page.evaluate(t => window.__seek(t), f / fps);
    const buf = await page.screenshot({ type: 'jpeg', quality: 93 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (++done % 100 === 0) console.log(`${done}/${total}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await page.close();
  return seg;
}
const segs = await Promise.all(Array.from({ length: WORKERS }, (_, w) => worker(w)));
await browser.close();
fs.writeFileSync(`${OUT}/list.txt`, segs.map(s => `file '${path.basename(s)}'`).join('\n'));
await new Promise(r => spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', `${OUT}/list.txt`, '-c', 'copy', `${OUT}/video_silent.mp4`], { stdio: 'inherit' }).on('close', r));
console.log(`DONE in ${((Date.now() - t0) / 1000).toFixed(0)}s -> ${OUT}/video_silent.mp4`);
