"""Gera fundos raster responsivos de papel pautado para a landing page."""

from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1] / "public" / "assets"
ROOT.mkdir(parents=True, exist_ok=True)


def make_background(width: int, height: int, mobile: bool, filename: str) -> None:
    yy, xx = np.mgrid[0:height, 0:width].astype(np.float32)
    nx, ny = xx / width, yy / height
    warm = np.array([255.0, 250.0, 240.0], dtype=np.float32)
    blue = np.array([205.0, 240.0, 250.0], dtype=np.float32)
    if mobile:
        wash = 0.40 * np.exp(-(((nx - .56) / .72) ** 2 + ((ny - .08) / .25) ** 2) * 1.4)
        wash += 0.18 * np.exp(-(((nx - .90) / .35) ** 2 + ((ny - .49) / .32) ** 2) * 2.0)
    else:
        wash = 0.38 * np.exp(-(((nx - .72) / .58) ** 2 + ((ny - .01) / .28) ** 2) * 1.5)
        wash += 0.14 * np.exp(-(((nx - .88) / .34) ** 2 + ((ny - .44) / .40) ** 2) * 2.0)
    wash = np.clip(wash, 0, .48)[..., None]
    pixels = warm * (1 - wash) + blue * wash
    rng = np.random.default_rng(21 if mobile else 12)
    paper = rng.normal(0, 1.15, (height, width, 1))
    pixels = np.clip(pixels + paper, 0, 255).astype(np.uint8)
    im = Image.fromarray(pixels, "RGB")
    ruling = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(ruling)
    spacing = 80 if mobile else 91
    for y in range(60, height + 120, spacing):
        rise = int(width * .028)
        draw.line((0, y + rise, width, y - rise), fill=(104, 185, 205, 27), width=2)
    ruling = ruling.filter(ImageFilter.GaussianBlur(.5))
    im = Image.alpha_composite(im.convert("RGBA"), ruling)
    im.save(ROOT / filename, optimize=True)


make_background(2048, 1100, False, "fundo-hero-desktop.png")
make_background(900, 1600, True, "fundo-hero-mobile.png")
print("Fundos desktop e mobile gerados em", ROOT)
