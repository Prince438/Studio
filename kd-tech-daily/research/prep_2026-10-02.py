"""Prepare media for the 02.10.26 episode: crops to 1600x900 JPEGs, clip frames, logos."""
import os, re, subprocess
from PIL import Image
R = 'research/raw-2026-10-02'
os.makedirs('img', exist_ok=True)

def crop169(im, cx=0.5, cy=0.5, zoom=1.0):
    w, h = im.size; tw = min(w, h * 16 / 9) / zoom; th = tw * 9 / 16
    x0 = max(0, min(w - tw, cx * w - tw / 2)); y0 = max(0, min(h - th, cy * h - th / 2))
    return im.crop((int(x0), int(y0), int(x0 + tw), int(y0 + th))).resize((1600, 900), Image.LANCZOS)

# 1. Cloudflare latency chart, letterboxed on white
ch = Image.open(f'{R}/clef_latency.png').convert('RGB'); s = 1560 / ch.width
ch = ch.resize((1560, round(ch.height * s)), Image.LANCZOS)
bg = Image.new('RGB', (1600, 900), (255, 255, 255)); bg.paste(ch, (20, (900 - ch.height) // 2)); bg.save('img/clef_latency.jpg', quality=92)
print('chart scale', s, 'top', (900 - ch.height) // 2)
# 2. Pentagon aerial (public domain, DoD / SSgt John Wright)
crop169(Image.open(f'{R}/pentagon_a.jpg').convert('RGB'), 0.5, 0.56).save('img/pentagon.jpg', quality=90)
# 3. DeepGEMM-Ascend README performance table (GitHub)
gh = Image.open(f'{R}/gh_deepgemm_perf.png').convert('RGB')
gh.crop((380, 40, 2200, 40 + 1024)).resize((1600, 900), Image.LANCZOS).save('img/deepgemm_perf.jpg', quality=92)
top = Image.open(f'{R}/gh_deepgemm_top.png').convert('RGB'); top.crop((0, 150, 3200, 1950)).resize((1600, 900), Image.LANCZOS).save('img/deepgemm_repo.jpg', quality=90)
# 4. thumbs
Image.open(f'{R}/canvas_header.jpg').convert('RGB').save('img/canvas_header.jpg', quality=88)

# 5. clips -> 30 fps JPEG frame sequences (Chromium can't play H.264)
def frames(src, name, vf, n):
    d = f'clips/{name}'; os.makedirs(d, exist_ok=True)
    for f in os.listdir(d): os.remove(os.path.join(d, f))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', vf, '-frames:v', str(n), '-q:v', '3', f'{d}/%04d.jpg'], check=True)
    print(name, len(os.listdir(d)), 'frames')
frames(f'{R}/canvas_coding.gif', 'canvas', 'fps=30,scale=1280:720:flags=lanczos', 300)
# Meta capture-LED clip: 1920x1672 -> 16:9 crop on the glasses, slowed to ~2.2x with motion interpolation
frames(f'{R}/meta_led.mp4', 'glasses', 'crop=1920:1080:0:180,scale=1280:720:flags=lanczos,setpts=2.2*PTS,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1', 300)

# 6. logos: simple-icons recolored white
for k in ['cloudflare', 'deepseek', 'huawei', 'shopify', 'meta']:
    svg = open(f'node_modules/simple-icons/icons/{k}.svg', encoding='utf8').read()
    open(f'logos/{k}.svg', 'w', encoding='utf8').write(svg.replace('<svg ', '<svg fill="#ffffff" ', 1))
# Strands Agents (AWS) logo: drop the black square
st = Image.open(f'{R}/strands_avatar.png').convert('RGBA'); px = st.load()
for y in range(st.height):
    for x in range(st.width):
        r, g, b, a = px[x, y]
        if max(r, g, b) < 40: px[x, y] = (0, 0, 0, 0)
st.crop(st.getbbox()).save('logos/strands.png')
print('done')
