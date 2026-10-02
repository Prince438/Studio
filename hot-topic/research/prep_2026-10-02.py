"""Media for KD Hot Topic EP.01 (The Decision Model Wars): clip frame sequences (30 fps), stills and logos."""
import os, subprocess, shutil
from PIL import Image, ImageOps
R = 'research/raw-2026-10-02'
for d in ('img', 'clips', 'logos'): os.makedirs(d, exist_ok=True)

def frames(src, name, vf, n, ss=None):
    d = f'clips/{name}'; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    cmd = ['ffmpeg', '-v', 'error', '-y'] + (['-ss', str(ss)] if ss is not None else []) + ['-i', src, '-vf', vf, '-frames:v', str(n), '-q:v', '3', f'{d}/%04d.jpg']
    subprocess.run(cmd, check=True); print(name, len(os.listdir(d)), 'frames')

# TypeSafe's own site animations (official): decision grid, error-rate chart, cube -> checkmark
frames(f'{R}/ts_wx5AYiR3CjcGDBUp13nd6ZiWI.webm', 'ts_grid', 'setpts=1.25*PTS,fps=30,scale=750:900:flags=lanczos', 320)
frames(f'{R}/ts_x91HFTGruL0hfUurYgWL66amfM.mp4', 'ts_chart', 'setpts=1.5*PTS,fps=30,scale=830:898:flags=lanczos', 240)
frames(f'{R}/ts_6dlt0WfUmvQHhwOb6UEI5rNPNc.webm', 'ts_cube', 'fps=30,scale=720:720:flags=lanczos', 162)
# OpenAI DevDay 2026 keynote, Decisions API segment (official OpenAI YouTube), from 3.5 s into the downloaded section
frames(f'{R}/openai_devday_decisions.mp4', 'oa_demo', 'fps=30,scale=1280:720:flags=lanczos', 420, ss=3.5)

# stills
Image.open(f'{R}/ts_RtIGTDwO43jR4ZDilesXiR5znc.jpg').convert('RGB').save('img/ts_card.jpg', quality=92)
j = Image.open(f'{R}/jevons.jpg').convert('L'); j = ImageOps.autocontrast(j, cutoff=1).resize((j.width * 2, j.height * 2), Image.LANCZOS)
j.convert('RGB').save('img/jevons.jpg', quality=92)                                   # public domain engraving (G. J. Stodart)
shutil.copy('../kd-tech-daily/img/clef_latency.jpg', 'img/clef_latency.jpg')           # Cloudflare blog chart
shutil.copy(f'../kd-tech-daily/research/raw-2026-10-02/clef_fig2.png', 'img/clef_flow.png')

# logos: TypeSafe mark (black on pink) -> white on transparent; others reused
m = Image.open(f'{R}/ts_kcuF2BEp5XaVfkmFB634IPRKQH0.png').convert('RGB'); px = m.load()
out = Image.new('RGBA', m.size, (0, 0, 0, 0)); po = out.load()
for y in range(m.height):
    for x in range(m.width):
        r, g, b = px[x, y]
        if r + g + b < 200: po[x, y] = (255, 255, 255, 255)
out.crop(out.getbbox()).save('logos/typesafe.png')
for k in ['cloudflare']:
    svg = open(f'node_modules/simple-icons/icons/{k}.svg', encoding='utf8').read()
    open(f'logos/{k}.svg', 'w', encoding='utf8').write(svg.replace('<svg ', '<svg fill="#ffffff" ', 1))
shutil.copy('../kd-tech-daily/logos/openai_wordmark_white.svg', 'logos/openai.svg')
shutil.copy('../kd-tech-daily/logos/strands.png', 'logos/strands.png')
print('done')
