let pw; try { pw = await import('playwright'); } catch { pw = await import('/home/claude/.npm-global/lib/node_modules/playwright/index.mjs'); }
import path from 'path';
const [,, html, out, w, h] = process.argv;
const b = await pw.chromium.launch(); const p = await b.newPage({viewport:{width:+w,height:+h}});
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+path.resolve(html)); await p.waitForTimeout(600);
await p.screenshot({path:out}); await b.close();
