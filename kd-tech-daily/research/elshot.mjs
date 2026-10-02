// screenshot one element at time t: node research/elshot.mjs <t> <selector> <out.png>
let pw; try { pw = await import('playwright'); } catch { pw = await import('/home/claude/.npm-global/lib/node_modules/playwright/index.mjs'); }
import path from 'path';
const [,, t, sel, out] = process.argv;
const b = await pw.chromium.launch(); const p = await b.newPage({viewport:{width:1920,height:1080}});
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+path.resolve('index.html')); await p.waitForFunction(()=>window.__ready===true,null,{timeout:30000});
await p.evaluate(t=>window.__seek(+t), t); await p.locator(sel).screenshot({path:out}); await b.close();
