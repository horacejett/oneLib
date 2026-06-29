"""Tiny dependency-free RGBA PNG toolkit: load, save, crop, resize (bilinear),
composite, rounded-rect tile, recolor. Enough to build app icons + logos."""
import struct, zlib

def load_rgba(path):
    d = open(path, 'rb').read()
    assert d[:8] == b'\x89PNG\r\n\x1a\n', path
    pos = 8; w = h = bd = ct = 0; idat = b''; plte = b''; trns = b''
    while pos < len(d):
        ln = struct.unpack('>I', d[pos:pos+4])[0]; typ = d[pos+4:pos+8]
        chunk = d[pos+8:pos+8+ln]; pos += 12 + ln
        if typ == b'IHDR': w, h, bd, ct = struct.unpack('>IIBB', chunk[:10])
        elif typ == b'IDAT': idat += chunk
        elif typ == b'PLTE': plte = chunk
        elif typ == b'tRNS': trns = chunk
        elif typ == b'IEND': break
    raw = zlib.decompress(idat)
    ch = {0:1, 2:3, 3:1, 4:2, 6:4}[ct]
    bpp = ch * (bd // 8); stride = w * bpp
    out = bytearray(); prev = bytearray(stride); i = 0
    for y in range(h):
        f = raw[i]; i += 1; line = bytearray(raw[i:i+stride]); i += stride
        for x in range(stride):
            a = line[x-bpp] if x >= bpp else 0
            b = prev[x]; c = prev[x-bpp] if x >= bpp else 0
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + ((a+b) >> 1)) & 255
            elif f == 4:
                p = a + b - c; pa = abs(p-a); pb = abs(p-b); pc = abs(p-c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        out += line; prev = line
    # to RGBA
    px = bytearray(w*h*4)
    for idx in range(w*h):
        s = idx*ch
        if ct == 6: r,g,b,a = out[s],out[s+1],out[s+2],out[s+3]
        elif ct == 2: r,g,b,a = out[s],out[s+1],out[s+2],255
        elif ct == 0: r=g=b=out[s]; a=255
        elif ct == 4: r=g=b=out[s]; a=out[s+1]
        elif ct == 3:
            pi = out[s]*3; r,g,b = plte[pi],plte[pi+1],plte[pi+2]
            a = trns[out[s]] if out[s] < len(trns) else 255
        d4 = idx*4; px[d4]=r; px[d4+1]=g; px[d4+2]=b; px[d4+3]=a
    return {'w': w, 'h': h, 'px': px}

def save_rgba(img, path):
    w, h, px = img['w'], img['h'], img['px']
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += px[y*w*4:(y+1)*w*4]
    comp = zlib.compress(bytes(raw), 9)
    def chunk(typ, data):
        return struct.pack('>I', len(data)) + typ + data + struct.pack('>I', zlib.crc32(typ+data) & 0xffffffff)
    out = b'\x89PNG\r\n\x1a\n'
    out += chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
    out += chunk(b'IDAT', comp)
    out += chunk(b'IEND', b'')
    open(path, 'wb').write(out)

def get(img, x, y):
    w, h = img['w'], img['h']
    if x < 0: x = 0
    if y < 0: y = 0
    if x >= w: x = w-1
    if y >= h: y = h-1
    i = (y*w+x)*4; p = img['px']
    return p[i], p[i+1], p[i+2], p[i+3]

def resize(img, nw, nh):
    w, h = img['w'], img['h']
    out = bytearray(nw*nh*4)
    for y in range(nh):
        sy = (y+0.5)*h/nh - 0.5
        y0 = int(sy) if sy >= 0 else int(sy)-1
        fy = sy - y0
        for x in range(nw):
            sx = (x+0.5)*w/nw - 0.5
            x0 = int(sx) if sx >= 0 else int(sx)-1
            fx = sx - x0
            c00 = get(img, x0, y0);   c10 = get(img, x0+1, y0)
            c01 = get(img, x0, y0+1); c11 = get(img, x0+1, y0+1)
            di = (y*nw+x)*4
            for k in range(4):
                top = c00[k]*(1-fx)+c10[k]*fx
                bot = c01[k]*(1-fx)+c11[k]*fx
                out[di+k] = int(top*(1-fy)+bot*fy + 0.5)
    return {'w': nw, 'h': nh, 'px': out}

def tight_bbox(img, x0=0, y0=0, x1=None, y1=None, athr=40):
    w, h, p = img['w'], img['h'], img['px']
    x1 = w if x1 is None else x1; y1 = h if y1 is None else y1
    minx=miny=10**9; maxx=maxy=-1
    for y in range(y0, y1):
        for x in range(x0, x1):
            if p[(y*w+x)*4+3] > athr:
                if x<minx:minx=x
                if x>maxx:maxx=x
                if y<miny:miny=y
                if y>maxy:maxy=y
    return minx, miny, maxx, maxy

def crop(img, x0, y0, x1, y1):
    w = img['w']; nw = x1-x0+1; nh = y1-y0+1
    out = bytearray(nw*nh*4)
    for y in range(nh):
        src = ((y+y0)*w + x0)*4
        out[y*nw*4:(y+1)*nw*4] = img['px'][src:src+nw*4]
    return {'w': nw, 'h': nh, 'px': out}

def blank(w, h, rgba=(0,0,0,0)):
    px = bytearray(w*h*4)
    for i in range(w*h):
        px[i*4:i*4+4] = bytes(rgba)
    return {'w': w, 'h': h, 'px': px}

def composite(dst, src, ox, oy):
    """alpha-over src onto dst at (ox,oy)."""
    dw, dh, dp = dst['w'], dst['h'], dst['px']
    sw, sh, sp = src['w'], src['h'], src['px']
    for y in range(sh):
        dy = oy+y
        if dy < 0 or dy >= dh: continue
        for x in range(sw):
            dx = ox+x
            if dx < 0 or dx >= dw: continue
            si = (y*sw+x)*4; sa = sp[si+3]
            if sa == 0: continue
            di = (dy*dw+dx)*4
            a = sa/255.0; ia = 1-a
            for k in range(3):
                dp[di+k] = int(sp[si+k]*a + dp[di+k]*ia + 0.5)
            dp[di+3] = min(255, sp[si+3] + int(dp[di+3]*ia + 0.5))
    return dst

def rounded_rect(w, h, rx, rgba):
    """solid rounded-rect tile with anti-aliased corners (supersample corners)."""
    img = blank(w, h, (rgba[0], rgba[1], rgba[2], 0))
    p = img['px']
    for y in range(h):
        for x in range(w):
            # distance into nearest corner
            cx = None; cy = None
            if x < rx and y < rx: cx, cy = rx, rx
            elif x >= w-rx and y < rx: cx, cy = w-rx-1, rx
            elif x < rx and y >= h-rx: cx, cy = rx, h-rx-1
            elif x >= w-rx and y >= h-rx: cx, cy = w-rx-1, h-rx-1
            if cx is None:
                a = 255
            else:
                d = ((x-cx)**2 + (y-cy)**2) ** 0.5
                if d <= rx-0.5: a = 255
                elif d >= rx+0.5: a = 0
                else: a = max(0, min(255, int(255*(rx+0.5-d) + 0.5)))
            i = (y*w+x)*4
            p[i]=rgba[0]; p[i+1]=rgba[1]; p[i+2]=rgba[2]; p[i+3]=a
    return img

def recolor(img, rgb):
    """keep alpha, set all RGB to rgb (for monochrome/template + solid-color marks)."""
    p = img['px']
    out = bytearray(p)
    for i in range(0, len(p), 4):
        out[i]=rgb[0]; out[i+1]=rgb[1]; out[i+2]=rgb[2]
    return {'w': img['w'], 'h': img['h'], 'px': out}
