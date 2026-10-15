"""Fundos raster para a faixa do menu e a divisória curva do hero."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math
import random

OUT = Path(__file__).resolve().parents[1] / 'public' / 'assets'
OUT.mkdir(parents=True, exist_ok=True)

W, H = 2400, 150
sky = Image.new('RGBA', (W, H), (0, 0, 0, 0))
px = sky.load()
for y in range(102):
    t = y / 101
    for x in range(W):
        noise = 2 * math.sin(x / 43) + 2 * math.sin(x / 101 + y / 26)
        px[x, y] = (int(190 + 42*t + noise), int(237 + 14*t + noise/2), 252, 255)
clouds = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(clouds)
random.seed(12)
for cx in range(-60, W+100, 95):
    cy = random.randint(77, 96)
    rx = random.randint(43, 72)
    ry = random.randint(27, 39)
    d.ellipse((cx-rx, cy-ry, cx+rx, cy+ry), fill=(255, 253, 246, 252))
    d.ellipse((cx-35, cy-51, cx+28, cy+24), fill=(255, 253, 246, 252))
d.rectangle((0, 100, W, H), fill=(255, 250, 241, 255))
clouds = clouds.filter(ImageFilter.GaussianBlur(1.4))
sky.alpha_composite(clouds)
sky.save(OUT / 'ceu-atras-menu.png', optimize=True)

W, H = 2400, 100
curve = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(curve)
anchors = [(0, 72),(.11, 83),(.27, 32),(.38, 43),(.49, 27),(.62, 62),(.79, 64),(1, 19)]
def catmull(t):
    for i in range(len(anchors)-1):
        a,b=anchors[i],anchors[i+1]
        if a[0] <= t <= b[0]:
            p0=anchors[max(0,i-1)][1];p1=a[1];p2=b[1];p3=anchors[min(len(anchors)-1,i+2)][1]
            u=(t-a[0])/(b[0]-a[0]);u2=u*u;u3=u2*u
            return .5*((2*p1)+(-p0+p2)*u+(2*p0-5*p1+4*p2-p3)*u2+(-p0+3*p1-3*p2+p3)*u3)
    return anchors[-1][1]
points=[(x,round(catmull(x/(W-1)))) for x in range(W)]
d.polygon(points+[(W-1,H),(0,H)],fill=(255,250,241,255))
distance=0
last=points[0]
segments=[]
for point in points[1:]:
    length=math.hypot(point[0]-last[0],point[1]-last[1])
    distance+=length
    if distance % 25 < 13:
        segments.append(point)
    elif len(segments)>1:
        d.line(segments,fill=(244,204,88,235),width=3,joint='curve')
        segments=[]
    last=point
if len(segments)>1:d.line(segments,fill=(244,204,88,235),width=3,joint='curve')
curve.save(OUT / 'curva-amarela-hero.png', optimize=True)
print('Faixa do menu e curva do hero geradas em PNG.')
