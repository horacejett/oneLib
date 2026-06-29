"""
oneLib 品牌资源生成器（无第三方依赖，纯 Python + macOS 自带 sips）。

用法：
    cd brand-source/tools
    python3 gen_assets.py all      # 生成全部品牌资源
    python3 gen_assets.py web      # 仅生成当前 Web 项目使用的资源
    python3 gen_assets.py readme   # 仅生成 README/OG 展示图
    python3 gen_assets.py svg      # 仅生成 svg 母版

母版图标：brand-source/onelib-mark-white.png（oneLib 纯图标，alpha）。
品牌色：藏青 #091842 / 绛红 #94122C。
"""
import imglib as I
import sys, os, base64, struct, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))          # 仓库根
GEN = os.path.join(ROOT, "brand-source", "generated")
RESLOGO = os.path.join(GEN, "variants")
MODELS = os.path.join(GEN, "models")
PLATFORM_ONELIB = os.path.join(ROOT, "src/frontend/platform/public/assets/onelib")
PLATFORM_ASSETS = os.path.join(ROOT, "src/frontend/platform/public/assets")
CLIENT_ASSETS = os.path.join(ROOT, "src/frontend/client/public/assets")
MARK = os.path.join(HERE, "..", "onelib-mark-white.png")

NAVY = (9, 24, 66)
MAROON = (148, 18, 44)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

mark = I.load_rgba(MARK)
MW, MH = mark["w"], mark["h"]

def ensure_dirs():
    for path in (GEN, RESLOGO, MODELS, PLATFORM_ONELIB, PLATFORM_ASSETS, CLIENT_ASSETS):
        os.makedirs(path, exist_ok=True)

def placed(cw, ch, markcolor, frac):
    m = I.recolor(mark, markcolor)
    target = int(cw * frac); s = target / MW
    nw, nh = int(MW * s), int(MH * s)
    return I.resize(m, nw, nh), (cw - int(MW*s)) // 2, (ch - int(MH*s)) // 2

def placed_fit(cw, ch, markcolor, max_w_frac=0.72, max_h_frac=0.72, cx=0.5, cy=0.5):
    m = I.recolor(mark, markcolor)
    scale = min((cw * max_w_frac) / MW, (ch * max_h_frac) / MH)
    nw, nh = max(1, int(MW * scale)), max(1, int(MH * scale))
    ox = int(cw * cx - nw / 2)
    oy = int(ch * cy - nh / 2)
    return I.resize(m, nw, nh), ox, oy

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i]-a[i])*t + 0.5) for i in range(3))

def gradient_bg(w, h, c1, c2):
    img = I.blank(w, h, (0,0,0,255)); p = img["px"]
    for y in range(h):
        for x in range(w):
            r,g,b = lerp(c1, c2, (x+y)/(w+h-2)); i=(y*w+x)*4
            p[i]=r; p[i+1]=g; p[i+2]=b; p[i+3]=255
    return img

def variant(size, bg, markcolor, frac=0.60):
    if bg == "transparent": canvas = I.blank(size, size, (0,0,0,0))
    elif isinstance(bg, tuple) and bg[0] == "grad": canvas = gradient_bg(size, size, bg[1], bg[2])
    else: canvas = I.blank(size, size, (bg[0], bg[1], bg[2], 255))
    m, ox, oy = placed(size, size, markcolor, frac)
    I.composite(canvas, m, ox, oy); return canvas

def app_icon():
    icon = variant(1024, ("grad", NAVY, MAROON), WHITE, frac=0.60)
    I.save_rgba(icon, os.path.join(GEN, "onelib-app-icon.png"))
    print("onelib-app-icon.png")

def tray():
    for size,name in [(22,"iconTemplate.png"),(44,"iconTemplate@2x.png"),(66,"iconTemplate@3x.png")]:
        I.save_rgba(variant(size,"transparent",BLACK,frac=0.92), os.path.join(RESLOGO,name))
    print("tray templates")

VARIANTS = {
    "onelib-transparent.png": ("transparent", NAVY),
    "onelib-white.png": (WHITE, NAVY),
    "onelib-black.png": (BLACK, WHITE),
    "onelib-blue.png": (NAVY, WHITE),
    "onelib-gradient.png": (("grad", NAVY, MAROON), WHITE),
    "onelib-purple.png": (MAROON, WHITE),
    "onelib-coral.png": (MAROON, WHITE),
    "onelib-veri-peri.png": (NAVY, WHITE),
    "onelib-viva-magenta.png": (MAROON, WHITE),
    "onelib-mocha-mousse.png": (NAVY, WHITE),
    "onelib-emerald.png": (NAVY, WHITE),
    "onelib-8bit.png": (NAVY, WHITE),
    "onelib-cyberpunk.png": (BLACK, WHITE),
    "onelib-futuristic.png": (NAVY, WHITE),
}
def variants():
    cache={}
    for fn,(bg,mc) in VARIANTS.items():
        key=(str(bg),mc)
        if key not in cache: cache[key]=variant(512,bg,mc,frac=0.60)
        I.save_rgba(cache[key], os.path.join(RESLOGO,fn))
    print(len(VARIANTS),"variants")

def model_icon():
    I.save_rgba(variant(256,"transparent",NAVY,frac=0.78), os.path.join(MODELS,"onelib.png")); print("models/onelib.png")

def svgs():
    b64 = base64.b64encode(open(MARK,"rb").read()).decode()
    iw=int(1024*0.56); ih=int(iw*MH/MW); ix=(1024-iw)//2; iy=(1024-ih)//2
    svg1024 = (
f'''<svg width="1024" height="1024" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect width="1024" height="1024" rx="180" ry="180" fill="#091842"/>
  <image x="{ix}" y="{iy}" width="{iw}" height="{ih}" xlink:href="data:image/png;base64,{b64}"/>
</svg>
''')
    open(os.path.join(GEN,"onelib-app-icon.svg"),"w").write(svg1024)
    open(os.path.join(CLIENT_ASSETS,"logo.svg"),"w").write(svg1024.replace('width="1024" height="1024"', 'width="512" height="512"'))
    tw=int(32*0.92); th=int(tw*MH/MW); tx=(32-tw)//2; ty=(32-th)//2
    open(os.path.join(RESLOGO,"icon.svg"),"w").write(
f'''<svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <image x="{tx}" y="{ty}" width="{tw}" height="{th}" xlink:href="data:image/png;base64,{b64}"/>
</svg>
''')
    print("svg masters")

def make_banner():
    for w, h, name in ((1600, 520, "onelib-banner.png"), (1200, 630, "onelib-og-image.png")):
        canvas = gradient_bg(w, h, NAVY, (24, 29, 50))
        m, ox, oy = placed_fit(w, h, WHITE, max_w_frac=0.36, max_h_frac=0.64, cx=0.5, cy=0.5)
        I.composite(canvas, m, ox, oy)
        I.save_rgba(canvas, os.path.join(GEN, name))
        print(name)

def make_login_art(w, h, dark=False):
    if dark:
        canvas = gradient_bg(w, h, NAVY, MAROON)
        m, ox, oy = placed_fit(w, h, WHITE, max_w_frac=0.62, max_h_frac=0.62, cx=0.5, cy=0.5)
    else:
        canvas = gradient_bg(w, h, (246, 248, 252), (229, 235, 244))
        m, ox, oy = placed_fit(w, h, MAROON, max_w_frac=0.66, max_h_frac=0.66, cx=0.5, cy=0.5)
    I.composite(canvas, m, ox, oy)
    return canvas

def make_wordmark(w, h, dark=False):
    canvas = I.blank(w, h, (0, 0, 0, 0))
    color = WHITE if dark else MAROON
    m, ox, oy = placed_fit(w, h, color, max_w_frac=0.74, max_h_frac=0.78, cx=0.5, cy=0.5)
    I.composite(canvas, m, ox, oy)
    return canvas

def maybe_jpeg(src_png, out_jpeg):
    try:
        subprocess.run(
            ["sips", "-s", "format", "jpeg", src_png, "--out", out_jpeg],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except Exception:
        I.save_rgba(I.load_rgba(src_png), out_jpeg)

def web_assets():
    app = variant(1024, ("grad", NAVY, MAROON), WHITE, frac=0.60)
    I.save_rgba(app, os.path.join(GEN, "onelib-app-icon.png"))
    I.save_rgba(I.resize(app, 512, 512), os.path.join(CLIENT_ASSETS, "maskable-icon.png"))
    I.save_rgba(I.resize(app, 192, 192), os.path.join(CLIENT_ASSETS, "icon-192x192.png"))
    I.save_rgba(I.resize(app, 180, 180), os.path.join(CLIENT_ASSETS, "apple-touch-icon-180x180.png"))
    I.save_rgba(I.resize(app, 512, 512), os.path.join(PLATFORM_ASSETS, "application-start-logo.png"))
    I.save_rgba(I.resize(app, 48, 48), os.path.join(PLATFORM_ONELIB, "favicon.ico"))

    I.save_rgba(make_login_art(840, 1408, dark=False), os.path.join(PLATFORM_ONELIB, "login-logo-big.png"))
    I.save_rgba(make_login_art(420, 704, dark=True), os.path.join(PLATFORM_ONELIB, "login-logo-dark.png"))
    I.save_rgba(make_wordmark(410, 120, dark=False), os.path.join(PLATFORM_ONELIB, "login-logo-small.png"))
    I.save_rgba(make_wordmark(342, 108, dark=True), os.path.join(PLATFORM_ONELIB, "logo-small-dark.png"))

    report_png = os.path.join(GEN, "onelib-report-logo.png")
    I.save_rgba(I.resize(app, 512, 512), report_png)
    maybe_jpeg(report_png, os.path.join(PLATFORM_ONELIB, "logo.jpeg"))
    print("web assets")

def build_ico(src_png_path, out_path, sizes=(16,32,48,64,128,256)):
    """用 sips 切多尺寸 png 后组装 PNG-in-ICO。需要 macOS sips。"""
    import subprocess, tempfile
    tmp = tempfile.mkdtemp()
    imgs=[]
    for s in sizes:
        p=os.path.join(tmp,f"{s}.png")
        subprocess.run(["sips","-z",str(s),str(s),src_png_path,"--out",p],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        imgs.append((s, open(p,"rb").read()))
    n=len(imgs); out=struct.pack('<HHH',0,1,n); offset=6+16*n; entries=b''; blobs=b''
    for s,data in imgs:
        wv=0 if s>=256 else s
        entries+=struct.pack('<BBBBHHII', wv,wv,0,0,1,32,len(data),offset)
        offset+=len(data); blobs+=data
    open(out_path,'wb').write(out+entries+blobs); print("icon.ico")

if __name__ == "__main__":
    ensure_dirs()
    step = sys.argv[1] if len(sys.argv)>1 else "all"
    if step in ("all","icon"): app_icon()
    if step in ("all","tray"): tray()
    if step in ("all","variants"): variants()
    if step in ("all","model"): model_icon()
    if step in ("all","readme"): make_banner()
    if step in ("all","web"): web_assets()
    if step in ("all","svg"): svgs()
    print("DONE", step)
