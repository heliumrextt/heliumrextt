from PIL import Image, ImageFilter
import numpy as np, html

COLS = 60
RAMP = ".,-:;=+!1ItfLCG08#@"
im = Image.open('/mnt/user-data/uploads/profile_face_ready.jpg').convert('RGB')
im = im.crop((120, 40, 480, 540))
cw, ch = im.size
ROWS = int(COLS*(ch/cw)*0.5)
arr = np.asarray(im).astype(float)
R, G, B = arr[...,0], arr[...,1], arr[...,2]
lum = 0.299*R + 0.587*G + 0.114*B
bg = (lum > 150) & (B >= R - 8)
bg = np.asarray(Image.fromarray((bg*255).astype('uint8')).filter(ImageFilter.MedianFilter(7))) > 127
fgmean = lum[~bg].mean(); lum2 = np.where(bg, fgmean, lum)
blur = np.asarray(Image.fromarray(lum2.astype('uint8')).filter(ImageFilter.GaussianBlur(cw/12))).astype(float)
loc = lum2 - 0.8*blur
fg = loc[~bg]; lo, hi = np.percentile(fg,2), np.percentile(fg,98)
g = 0.7*np.clip((loc-lo)/(hi-lo),0,1) + 0.3*np.clip((lum2-20)/200,0,1)
gi = Image.fromarray((np.clip(g,0,1)*255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.4)).resize((COLS,ROWS), Image.LANCZOS)
bi = Image.fromarray((bg*255).astype('uint8')).resize((COLS,ROWS), Image.BOX)
ga = np.asarray(gi)/255.0; ba = np.asarray(bi)/255.0 > 0.5

def art(invert):
    out=[]
    for y in range(ROWS):
        row=''
        for x in range(COLS):
            if ba[y,x]: row+=' '; continue
            v = 1-ga[y,x] if invert else ga[y,x]
            row += RAMP[int(v*(len(RAMP)-1))]
        out.append(row.rstrip())
    return out

THEMES = {
 'dark':  dict(bg='#0d1117', art='#c9d1d9', key='#ffa657', val='#a5d6ff', dim='#8b949e', head='#7ee787', invert=False),
 'light': dict(bg='#ffffff', art='#24292f', key='#953800', val='#0a3069', dim='#57606a', head='#116329', invert=True),
}

# Edit these! (section, [(key, value, optional_id)])
USER = 'heliumrextt'
INFO = [
 ('head', f'{USER}@github'),
 ('kv', 'OS', 'iOS'),
 ('kv', 'Uptime', '21 years'),
 ('kv', 'IDE', 'VSCode'),
 ('gap',),
 ('sec', 'Languages'),
 ('kv', 'Programming', 'Python, JavaScript'),
 ('kv', 'Real', 'English, Hindi'),
 ('gap',),
 ('sec', 'Hobbies'),
 ('kv', 'Software', 'Open Source, Web Dev'),
 ('kv', 'Hardware', 'Tinkering'),
 ('gap',),
 ('sec', 'Contact'),
 ('kv', 'Email', 'harshittrivedi5257@gmail.com'),
 ('kv', 'LinkedIn', 'linkedin.com/in/harshit-trivedi-050a822b6'),
 ('kv', 'Discord', 'your-discord'),
 ('gap',),
 ('sec', 'GitHub Stats'),
 ('kv', 'Repos', '0', 'repo_data'),
 ('kv', 'Stars', '0', 'star_data'),
 ('kv', 'Followers', '0', 'follower_data'),
 ('kv', 'Commits', '0', 'commit_data'),
]
LINE_W = 56  # width of dotted lines

def svg(theme):
    t = THEMES[theme]; lines = art(t['invert'])
    fs, lh, cwid = 12, 15, 7.2
    ax, ay = 20, 30
    ix = ax + COLS*cwid + 30
    height = max(len(lines)*lh, len(INFO)*20) + 60
    width = int(ix + LINE_W*8.6 + 24)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="ConsolasFallback,Consolas,\'DejaVu Sans Mono\',\'Courier New\',monospace" font-size="{fs}px">',
         f'<rect width="100%" height="100%" rx="8" fill="{t["bg"]}"/>',
         f'<text x="{ax}" y="{ay}" fill="{t["art"]}" xml:space="preserve">']
    for i,l in enumerate(lines):
        o.append(f'<tspan x="{ax}" y="{ay+i*lh}">{html.escape(l)}</tspan>')
    o.append('</text>')
    o.append(f'<text x="{ix}" y="{ay}" font-size="14px" xml:space="preserve">')
    y = ay
    for item in INFO:
        kind = item[0]
        if kind=='head':
            o.append(f'<tspan x="{ix}" y="{y}" fill="{t["head"]}">{html.escape(item[1])}</tspan><tspan fill="{t["dim"]}"> {"-"*(LINE_W-len(item[1])-1)}</tspan>')
        elif kind=='sec':
            o.append(f'<tspan x="{ix}" y="{y}" fill="{t["dim"]}">- </tspan><tspan fill="{t["head"]}">{item[1]}</tspan><tspan fill="{t["dim"]}"> {"-"*(LINE_W-len(item[1])-3)}</tspan>')
        elif kind=='kv':
            k, v = item[1], html.escape(item[2]); vid = f' id="{item[3]}"' if len(item)>3 else ''
            dots = '.'*max(2, LINE_W-len(k)-len(item[2])-2)
            o.append(f'<tspan x="{ix}" y="{y}" fill="{t["key"]}">{k}</tspan><tspan fill="{t["dim"]}">:{dots}</tspan><tspan{vid} fill="{t["val"]}">{v}</tspan>')
        y += 20 if kind!='gap' else 12
    o.append('</text></svg>')
    open(f'out/{theme}_mode.svg','w').write('\n'.join(o))

for th in THEMES: svg(th)
print('ok', ROWS)
