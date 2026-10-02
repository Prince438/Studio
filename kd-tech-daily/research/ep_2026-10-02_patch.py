"""Patch index.html from the 01.10.26 episode to the 02.10.26 episode (content only, layout unchanged)."""
import re
p = 'index.html'; s = open(p, encoding='utf8').read()


def swap(start, end, new):
    global s
    a = s.index(start); b = s.index(end, a)
    s = s[:a] + new + s[b:]


# ---------- CSS: new overlay styles ----------
s = s.replace('/* studio cam (packages) */', '''.chips{position:absolute;left:20px;right:20px;top:56px;display:flex;flex-wrap:wrap;gap:8px;z-index:2}
.chips span{font-family:"Pix";font-weight:700;font-size:21px;color:#07090c;background:var(--add);padding:5px 11px 3px;box-shadow:4px 4px 0 #0b3a1f}
.bill{position:absolute;left:56px;top:150px;width:420px;padding:18px 26px 20px;background:#fbf8f0;border:2px solid #d8d2c4;box-shadow:0 18px 40px rgba(0,0,0,.6);transform:rotate(-3deg);z-index:2;color:#1a1a1a;font-family:Georgia,serif}
.bill .cap{font-family:"Pix";font-size:16px;color:#7a6f5a;letter-spacing:1px}
.bill .q{font-size:64px;font-weight:700;margin-top:6px;line-height:1}
.bill .w{font-size:21px;color:#444;margin-top:8px;line-height:1.25}
.bill .stamp{position:absolute;right:-34px;top:34px;font-family:"Pix";font-weight:700;font-size:46px;color:#e11d48;border:6px solid #e11d48;padding:8px 14px 4px;transform:rotate(-12deg);background:rgba(251,248,240,.9)}
.counter.red .to{color:var(--del)}
.badge img{height:22px;vertical-align:-4px;margin-right:8px}

/* studio cam (packages) */''', 1)

# ---------- DATA ----------
swap('const STORIES = [', '\nconst $ = (s, r = document)', r'''const STORIES = [
  { sign:'+', tag:'MODELS', short:'DECISION MODELS', lines:['AMAZON +','CLOUDFLARE','OPEN DECIDERS'], mood:'star',
    bullets:['Strands Decider 2B: picks from your options with odds, ~106 ms on a 3090',
             'Clef-flash: 39 ms median vs Jev at 524 ms; both Apache 2.0'],
    term:['decide "ship it?" --opts yes,no','yes: 0.97  no: 0.03','zero essays were harmed'],
    sticker:'13X FASTER', logo:'logos/cloudflare.svg', logo2:'logos/strands.png', co:'MODELS', media:{type:'img', src:'img/clef_latency.jpg'}, credit:'IMAGE: CLOUDFLARE', label:'CLOUDFLARE BLOG' },
  { sign:'-', tag:'SECURITY', short:'PENTAGON BREACH', lines:['HACKERS STOLE','3M MILITARY','RECORDS'], mood:'shocked',
    bullets:['Defense Manpower Data Center: SSNs, names, birth dates, service info',
             'unencrypted; hackers inside Oct 2025 to July 2026; culprit unknown'],
    term:['cat /dmdc/share/records.csv','ssn,name,dob,race,service...','encryption: never heard of it'],
    sticker:'UNENCRYPTED', logo:'logos/lock.svg', co:'DEFENSE', media:{type:'img', src:'img/pentagon.jpg'}, credit:'IMAGE: DOD / SSGT JOHN WRIGHT', label:'THE PENTAGON' },
  { sign:'+', tag:'OPEN SOURCE', short:'DEEPSEEK x ASCEND', lines:['DEEPSEEK','OPEN-SOURCES','ASCEND TOOLS'], mood:'happy',
    bullets:['six tools for Huawei Ascend 950: DeepGEMM, DeepEP, FlashMLA, TileLang +2',
             'key libs keep their Nvidia APIs; GEMM hits 99.8% of hardware peak'],
    term:['git clone DeepGEMM-Ascend','BF16: 431 of 432 TFLOPS','nvidia-smi: command not found'],
    sticker:'99.8% PEAK', logo:'logos/deepseek.svg', logo2:'logos/huawei.svg', co:'DEEPSEEK', media:{type:'img', src:'img/deepgemm_perf.jpg'}, credit:'IMAGE: GITHUB / DEEPSEEK-AI', label:'DEEPGEMM-ASCEND' },
  { sign:'-', tag:'POLICY', short:'SMART GLASS VETO', lines:['NEWSOM','VETOES SMART','GLASSES BILL'], mood:'worried',
    bullets:['SB 1130 would have banned secretly recording people with wearable cams',
             'Newsom: definition too broad; Meta sold 7M+ smart glasses last year'],
    term:['glasses --record --quietly','capture LED: on (no off switch)','smile, you might be on camera'],
    sticker:'VETOED', logo:'logos/glasses.svg', mlogo:'logos/meta.svg', co:'POLICY', media:{type:'clip', name:'glasses', n:280}, credit:'VIDEO: META', label:'AI GLASSES CAPTURE LED' },
  { sign:'+', tag:'COMMERCE', short:'SHOPIFY CANVAS', lines:['SHOPIFY','LETS YOU CHAT','UP A STORE'], mood:'dollar',
    bullets:['Canvas: describe the vibe, Sidekick edits the real theme code live',
             'desktop-only, no third-party themes yet; rolling out in the coming days'],
    term:['sidekick "make the logo bigger"','theme updated, preview live','the classic client request'],
    sticker:'CHAT TO SHIP', logo:'logos/shopify.svg', co:'SHOPIFY', media:{type:'clip', name:'canvas', n:300}, credit:'VIDEO: SHOPIFY', label:'SHOPIFY CANVAS' },
];
const THUMBS = ['img/clef_latency.jpg','img/pentagon.jpg','img/deepgemm_repo.jpg','clips/glasses/0140.jpg','img/canvas_thumb.jpg'];
''')

# ---------- sources line ----------
swap('<div class="src" id="srcline">', '</div>\n', '<div class="src" id="srcline">src: Cloudflare, AWS via VentureBeat, TechCrunch, Military Times, DeepSeek (GitHub), GIGAZINE, Shopify, Meta.<br>video: Shopify, Meta. photo: U.S. DoD (public domain). Logos are trademarks of their owners; no endorsement implied.')

# ---------- media panel overlays ----------
swap('function mediaHTML(s, i) {', '\nSTORIES.forEach((s, i) => {', r'''function mediaHTML(s, i) {
  const m = s.media; let inner = '';
  if (m.type === 'img') inner = `<div class="kb"><div class="ph" style="background-image:url(${m.src})"></div>${i === 0 ? `
      <div class="hlbox" id="hbJev" style="left:684px;top:146px;width:92px;height:38px;border-color:#ffc940;box-shadow:0 0 22px rgba(255,201,64,.7)"></div><div class="hltag" id="htJev" style="left:684px;top:106px;background:#ffc940">JEV · 524 MS</div>
      <div class="hlbox" id="hbClef" style="left:76px;top:150px;width:74px;height:48px"></div><div class="hltag" id="htClef" style="left:76px;top:206px">CLEF-FLASH · 39 MS</div>` : ''}${i === 2 ? `
      <div class="hlbox" id="hbRow" style="left:30px;top:374px;width:800px;height:42px"></div><div class="hltag" id="htRow" style="left:560px;top:334px">99.8% OF PEAK</div>` : ''}</div>`;
  if (m.type === 'clip') inner = `<div class="kb"><img class="vf" src="clips/${m.name}/0001.jpg"></div>`;
  let extra = '';
  if (i === 0) extra = `<div class="badge" id="awsB" style="left:24px;bottom:58px;background:#232f3e"><img src="logos/strands.png">AWS STRANDS DECIDER 2B · OPEN</div>`;
  if (i === 1) extra = `<div class="badge" id="brB" style="left:24px;top:64px;background:#d7263d">INSIDE FROM OCT 2025 TO JUL 2026</div><div class="badge" id="encB" style="left:24px;top:64px;background:#d7263d">ENCRYPTION AT REST: NONE</div>
      <div class="counter red" id="ctr2"><div class="to">~<span class="cv">0.0</span>M</div><div class="lbl">RECORDS TAKEN · 2.8M LIVING + ~300K DECEASED</div></div>`;
  if (i === 2) extra = `<div class="chips" id="chips">${['DeepGEMM', 'DeepEP', 'TileLang', 'TileKernels', 'FlashMLA', 'DeepSelect'].map(t => `<span>${t}</span>`).join('')}</div>`;
  if (i === 3) extra = `<div class="bill" id="bill"><div class="cap">CALIFORNIA SENATE BILL</div><div class="q">SB 1130</div><div class="w">no secret recording with wearable cameras</div><div class="stamp" id="vetoS">VETOED</div></div>
      <div class="badge" id="vetoB" style="left:24px;bottom:58px;background:#d7263d">NEWSOM: TOO BROAD + ALREADY COVERED</div>`;
  if (i === 4) extra = `<div class="badge" id="skB" style="left:24px;bottom:58px;background:#5e8e3e">SIDEKICK: 25M+ THEME EDITS IN H1 2026</div><div class="badge" id="roB" style="left:24px;bottom:58px;background:#5e8e3e">DESKTOP ONLY · ROLLING OUT NOW</div>`;
  return `<div class="photo">${inner}<div class="phscan"></div>${extra}
    <div class="corner" style="left:-2px;top:-2px;border-right:none;border-bottom:none"></div><div class="corner" style="right:-2px;bottom:-2px;border-left:none;border-top:none"></div>
    <div class="phlbl"><i></i><img src="${s.mlogo || s.logo}" alt="">${s.label}</div>${m.type === 'clip' ? '<div class="rec">● VIDEO</div>' : ''}<div class="credit">${s.credit}</div></div>`;
}''')

# ---------- ticker ----------
s = re.sub(r"const tickUnit = '.*?';", lambda m: "const tickUnit = '+++ KD TECH DAILY +++ FRI 02 OCT 2026 +++ AMAZON + CLOUDFLARE OPEN-SOURCE DECISION MODELS +++ HACKERS STOLE 3M MILITARY RECORDS +++ DEEPSEEK OPEN-SOURCES ASCEND TOOLS +++ NEWSOM VETOES SMART GLASSES BILL +++ SHOPIFY CANVAS: CHAT UP A STORE +++ LEARN. BUILD. SHIP. ';", s, count=1)

# ---------- outro diff stat from the data ----------
old = "typeAt($('.a', st), '3 insertions(+), 2 deletions(-)', a + 1.0 + 19 / 70, 70, { cursor: false });"
assert old in s
s = s.replace(old, "const nAdd = STORIES.filter(x => x.sign === '+').length;\n  typeAt($('.a', st), `${nAdd} insertions(+), ${5 - nAdd} deletions(-)`, a + 1.0 + 19 / 70, 70, { cursor: false });")

# ---------- per-story media moments ----------
swap('// per-story media moments, timed to the voice', "tl.set('#cam', { visibility: 'hidden' }, 0);", r'''// per-story media moments, timed to the voice
(function () {
  const pop = (sel, t, from = { autoAlpha: 0, scale: 1.4 }, sfx = 'blip', extra = {}) => { tl.fromTo(sel, from, { autoAlpha: 1, scale: 1, x: 0, y: 0, duration: 0.3, ease: 'back.out(2)', immediateRender: false }, t); if (sfx) ev(t, sfx, extra); };
  const hide = (sel, t) => tl.to(sel, { autoAlpha: 0, duration: 0.2 }, t);
  // 1: Jev vs Clef-flash on Cloudflare's chart, AWS badge
  tl.set(['#hbJev', '#htJev', '#hbClef', '#htClef', '#awsB'], { autoAlpha: 0 }, 0);
  pop('#hbJev', WT('s1', 'jev')); tl.fromTo('#htJev', { autoAlpha: 0, y: 10 }, { autoAlpha: 1, y: 0, duration: 0.25, immediateRender: false }, WT('s1', 'jev') + 0.15);
  pop('#awsB', WT('s1', 'amazon'), { autoAlpha: 0, y: 20 }, 'pop');
  pop('#hbClef', WT('s1', 'clef'), { autoAlpha: 0, scale: 1.4 }, 'blip', { pitch: 1 }); tl.fromTo('#htClef', { autoAlpha: 0, y: -10 }, { autoAlpha: 1, y: 0, duration: 0.25, immediateRender: false }, WT('s1', 'clef') + 0.15);
  // 2: breach window, record counter, no encryption
  tl.set(['#brB', '#encB', '#ctr2'], { autoAlpha: 0 }, 0);
  pop('#brB', WT('s2', 'nine'), { autoAlpha: 0, x: -40 }, 'err'); hide('#brB', WT('s2', 'social') - 0.1);
  tl.fromTo('#ctr2', { autoAlpha: 0, x: -40 }, { autoAlpha: 1, x: 0, duration: 0.35, ease: 'back.out(2)', immediateRender: false }, WT('s2', 'three') - 0.25); ev(WT('s2', 'three') - 0.25, 'pop');
  const c2 = { v: 0 }; tl.to(c2, { v: 3.1, duration: 1.0, ease: 'power2.out', onUpdate: () => { $('#ctr2 .cv').textContent = c2.v.toFixed(1); } }, WT('s2', 'three'));
  for (let k = 0; k < 10; k++) ev(WT('s2', 'three') + k * 0.09, 'blip', { pitch: 3, soft: 1 });
  pop('#encB', WT('s2', 'unencrypted'), { autoAlpha: 0, x: -40 }, 'stamp');
  // 3: the six tools, then the 99.8% row
  tl.set(['#hbRow', '#htRow'], { autoAlpha: 0 }, 0);
  $$('#chips span').forEach((c, k) => { tl.from(c, { autoAlpha: 0, y: -16, scale: 0.6, duration: 0.25, ease: 'back.out(2.4)' }, WT('s3', 'six') + k * 0.16); ev(WT('s3', 'six') + k * 0.16, 'blip', { pitch: k % 2 }); });
  pop('#hbRow', WT('s3', 'ninety-nine'), { autoAlpha: 0, scale: 1.08 }, 'blip', { pitch: 1 }); tl.fromTo('#htRow', { autoAlpha: 0, y: 10 }, { autoAlpha: 1, y: 0, duration: 0.25, immediateRender: false }, WT('s3', 'ninety-nine') + 0.15);
  // 4: the bill gets vetoed on the word
  tl.set(['#bill', '#vetoS', '#vetoB'], { autoAlpha: 0 }, 0);
  tl.fromTo('#bill', { autoAlpha: 0, scale: 0.5, rotation: -14 }, { autoAlpha: 1, scale: 1, rotation: -3, duration: 0.35, ease: 'back.out(2)', immediateRender: false }, WT('s4', 'newsom') - 0.2); ev(WT('s4', 'newsom') - 0.2, 'pop');
  tl.fromTo('#vetoS', { autoAlpha: 0, scale: 2.6 }, { autoAlpha: 1, scale: 1, duration: 0.22, ease: 'power4.in', immediateRender: false }, WT('s4', 'vetoed')); ev(WT('s4', 'vetoed') + 0.2, 'stamp');
  hide('#bill', WT('s4', 'smart') - 0.1);
  pop('#vetoB', WT('s4', 'broad') - 0.25, { autoAlpha: 0, y: 20 }, 'err');
  // 5: Sidekick facts
  tl.set(['#skB', '#roB'], { autoAlpha: 0 }, 0);
  pop('#skB', WT('s5', 'sidekick'), { autoAlpha: 0, y: 20 }, 'blip', { pitch: 1 }); hide('#skB', WT('s5', 'rolling') - 0.15);
  pop('#roB', WT('s5', 'rolling'), { autoAlpha: 0, y: 20 }, 'pop');
})();
''')

# ---------- Kopi's action schedule ----------
swap('  // story 1 (', '];\nfunction moodAt', r'''  // story 1 (decision models)
  { a: S(0), b: WT('s1', 'decision') - 0.05, pose: 'headset', eyes: 'normal' },
  { a: WT('s1', 'decision') - 0.05, b: S(0) + 2.95, pose: 'point', look: -1, eyes: 'star' },
  { a: WT('s1', 'after') - 0.05, b: WT('s1', 'amazon') - 0.05, pose: 'tablet', fr: 2, eyes: 'down' },
  { a: WT('s1', 'they') - 0.05, b: WT('s1', 'they', 1) - 0.05, pose: 'pen', fr: 3, eyes: 'normal' },
  { a: WT('s1', 'pick') - 0.05, b: WT('s1', 'milliseconds') + 0.4, pose: 'thumb', eyes: 'wink' },
  { a: VEND('s1') + 0.1, b: S(1), pose: 'papers', fr: 7, eyes: 'happy' },
  // story 2 (Pentagon breach)
  { a: S(1), b: S(1) + 1.2, pose: 'headset', eyes: 'worried' },
  { a: S(1) + 1.2, b: S(1) + 2.95, pose: 'point', look: -1, eyes: 'shocked' },
  { a: WT('s2', 'taking') - 0.05, b: WT('s2', 'social') - 0.05, pose: 'read', eyes: 'down' },
  { a: WT('s2', 'unencrypted') - 0.05, b: WT('s2', 'and') - 0.02, pose: 'visor', eyes: 'shocked' },
  { a: WT('s2', 'nobody') - 0.05, b: VEND('s2') + 0.2, pose: 'pen', fr: 3, eyes: 'worried' },
  { a: VEND('s2') + 0.2, b: S(2), pose: 'papers', fr: 7, eyes: 'normal' },
  // story 3 (DeepSeek x Huawei)
  { a: S(2), b: S(2) + 1.15, pose: 'fist', eyes: 'happy' },
  { a: S(2) + 1.15, b: S(2) + 2.95, pose: 'point', look: -1, eyes: 'star' },
  { a: WT('s3', 'key') - 0.05, b: WT('s3', 'and') - 0.05, pose: 'tablet', fr: 2, eyes: 'down' },
  { a: WT('s3', 'ninety-nine') - 0.05, b: VEND('s3') + 0.3, pose: 'thumb', eyes: 'wink' },
  { a: VEND('s3') + 0.3, b: VEND('s3') + 1.3, pose: 'sip', eyes: 'happy' },
  { a: VEND('s3') + 1.3, b: S(3), pose: 'papers', fr: 7, eyes: 'normal' },
  // story 4 (smart-glasses veto): she taps her own LED visor on "smart glasses"
  { a: S(3), b: S(3) + 1.3, pose: 'tuck', eyes: 'worried' },
  { a: S(3) + 1.3, b: S(3) + 2.95, pose: 'point', look: -1, eyes: 'worried' },
  { a: WT('s4', 'smart') - 0.05, b: WT('s4', 'wearables') + 0.4, pose: 'visor', eyes: 'normal' },
  { a: WT('s4', 'he') - 0.05, b: WT('s4', 'current') - 0.05, pose: 'headset', eyes: 'worried' },
  { a: WT('s4', 'already') - 0.05, b: VEND('s4') + 0.2, pose: 'write', fr: 5, eyes: 'down' },
  { a: VEND('s4') + 0.2, b: S(4), pose: 'papers', fr: 7, eyes: 'normal' },
  // story 5 (Shopify Canvas)
  { a: S(4), b: S(4) + 1.2, pose: 'heart', eyes: 'heart' },
  { a: S(4) + 1.2, b: S(4) + 2.95, pose: 'point', look: -1, eyes: 'dollar' },
  { a: WT('s5', 'just') - 0.05, b: WT('s5', 'and', 1) - 0.05, pose: 'tablet', fr: 2, eyes: 'down' },
  { a: WT('s5', 'real') - 0.05, b: WT('s5', 'watch') + 0.3, pose: 'fist', eyes: 'dollar' },
  { a: VEND('s5') + 0.15, b: VEND('s5') + 1.15, pose: 'sip', eyes: 'happy' },
  { a: VEND('s5') + 1.15, b: S(5), pose: 'papers', fr: 7, eyes: 'happy' },
  // outro
  { a: T_OUTRO[0], b: T_OUTRO[0] + 0.55, pose: 'papers', fr: 7, eyes: 'happy' },
  { a: WT('out', 'now') - 0.05, b: WT('out', 'and') - 0.02, pose: 'thumb', eyes: 'wink' },
  { a: WT('out', 'happy') - 0.1, b: VEND('out') + 1.3, wave: true, eyes: 'happy' },
  { a: VEND('out') + 1.3, b: VEND('out') + 2.3, pose: 'sip', eyes: 'happy' },
  { a: VEND('out') + 2.3, b: 99, pose: 'heart', eyes: 'heart' },
''')

# ---------- preload ----------
old = "const pre = [...THUMBS, 'img/elevenlabs_team.jpg']"
assert old in s
s = s.replace(old, "const pre = [...new Set([...THUMBS, ...STORIES.filter(x => x.media.type === 'img').map(x => x.media.src)])]")
open(p, 'w', encoding='utf8').write(s)
print('patched', len(s))
