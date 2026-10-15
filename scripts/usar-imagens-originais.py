"""Extrai as imagens PNG originais incorporadas no SVG enviado pelo cliente.

O SVG é apenas uma fonte de edição: a página final serve arquivos PNG separados.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "referencias" / "embutidos"
OUT = ROOT / "public" / "assets" / "elementos"
OUT.mkdir(parents=True, exist_ok=True)

ITEMS = {
    "logo-desenho": 73,
    "nuvem-hero": 84,
    "estrela-hero": 87,
    "estrela-hero-baixo": 90,
    "nuvem-contorno": 91,
    "coracao-pequeno": 76,
    "grama-pequena": 93,
    "coracao-rabiscado": 97,
    "arco-iris-estrela": 113,
    "grama-larga": 133,
    "menina-acenando": 140,
    "fundo-card-amarelo": 103,
    "fundo-card-verde": 107,
    "fundo-card-rosa": 96,
    "fundo-card-azul": 99,
    "icone-coracao": 97,
    "icone-casinha": 100,
    "icone-paleta": 104,
    "icone-prato": 108,
    "estrela-pequena": 106,
    "onda-azul": 127,
    "grama-rodape": 139,
    "aviao-papel": 126,
    "coracao-contorno": 128,
    "icone-relogio": 116,
    "icone-bale": 119,
    "icone-cross-kids": 122,
    "icone-maca": 124,
    "icone-instagram": 130,
    "icone-instagram-rodape": 135,
    "icone-whatsapp-rodape": 136,
    "tracos-amarelos-esquerda": 77,
    "tracos-amarelos-direita": 78,
    "coracao-lateral": 79,
    "rabisco-amarelo": 92,
    "trilha-lateral": 95,
    "nuvem-lateral": 111,
    "trilha-grama-lateral": 112,
    "arco-pontilhado": 114,
    "linha-pontilhada-amarela": 125,
    "coracao-grande": 132,
    "trilha-rosa": 143,
}

for name, number in ITEMS.items():
    color = Image.open(SOURCE / f"{number:03}.png").convert("RGBA")
    mask = Image.open(SOURCE / f"{number - 72:03}.png").convert("L")
    if color.size != mask.size:
        raise ValueError(f"Máscara incompatível: {name} ({color.size} / {mask.size})")
    color.putalpha(mask)
    color.save(OUT / f"{name}.png", optimize=True)

assets = sorted(OUT.glob("*.png"))
tile_w, tile_h, columns = 190, 155, 5
sheet = Image.new("RGB", (tile_w * columns, tile_h * ((len(assets) + columns - 1) // columns)), "#fffaf2")
draw = ImageDraw.Draw(sheet)
for index, path in enumerate(assets):
    preview = Image.open(path).convert("RGBA")
    preview.thumbnail((tile_w - 16, tile_h - 40))
    x, y = (index % columns) * tile_w, (index // columns) * tile_h
    sheet.paste(preview, (x + (tile_w - preview.width) // 2, y + 5), preview)
    draw.text((x + 7, y + tile_h - 27), path.stem, fill="#123c59")
sheet.save(ROOT / "elementos-extraidos-contato.png")

with zipfile.ZipFile(ROOT / "elementos-png.zip", "w", zipfile.ZIP_DEFLATED) as archive:
    for image in assets:
        archive.write(image, f"elementos/{image.name}")

print(f"{len(ITEMS)} PNGs originais extraídos; pacote atualizado.")
