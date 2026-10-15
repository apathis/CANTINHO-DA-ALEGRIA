from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BOARD = Image.open(ROOT / "referencias/svg-convert-preview.png").convert("RGBA")
OUT = ROOT / "dist" / "assets" / "elementos"
OUT.mkdir(parents=True, exist_ok=True)

# Regiões lógicas do segundo SVG, rasterizado em 2560 × 1440. Cada saída é
# um PNG independente; a página mantém títulos, botões e links em HTML.
REGIONS = {
    "casinha-e-criancas": (400, 365, 602, 583),
    "nuvem-hero": (948, 451, 1018, 503),
    "post-it-alegria": (1167, 457, 1258, 553),
    "estrela-hero": (1164, 447, 1202, 481),
    "estrela-hero-baixo": (1150, 532, 1190, 570),
    "nuvem-contorno": (1195, 548, 1260, 590),
    "coracao-pequeno": (843, 451, 872, 482),
    "grama-pequena": (728, 651, 777, 693),
    "coracao-rabiscado": (416, 782, 501, 855),
    "arco-iris-estrela": (544, 740, 647, 855),
    "grama-larga": (503, 892, 630, 951),
    "menina-acenando": (482, 1000, 593, 1127),
    "fundo-card-amarelo": (1300, 334, 1441, 476),
    "fundo-card-verde": (1518, 226, 1655, 372),
    "fundo-card-rosa": (1467, 405, 1601, 543),
    "fundo-card-azul": (1446, 600, 1579, 739),
    "icone-coracao": (414, 782, 501, 854),
    "icone-casinha": (877, 747, 957, 815),
    "icone-paleta": (1388, 783, 1477, 856),
    "icone-prato": (1325, 597, 1430, 667),
    "estrela-pequena": (1530, 781, 1562, 813),
    "onda-azul": (1321, 1068, 1812, 1196),
    "grama-rodape": (1313, 992, 1477, 1062),
    "aviao-papel": (1208, 886, 1261, 933),
    "coracao-contorno": (1173, 895, 1205, 930),
}

saved = []
for name, box in REGIONS.items():
    crop = BOARD.crop(box)
    if name == "post-it-alegria":
        mask = Image.new("L", crop.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.polygon([(1170-box[0],481-box[1]),(1239-box[0],460-box[1]),(1257-box[0],530-box[1]),(1190-box[0],552-box[1])],fill=255)
        draw.polygon([(1215-box[0],457-box[1]),(1244-box[0],457-box[1]),(1245-box[0],482-box[1]),(1213-box[0],480-box[1])],fill=255)
        crop.putalpha(Image.composite(crop.getchannel("A"),Image.new("L",crop.size,0),mask))
    elif name in ("estrela-hero", "estrela-hero-baixo"):
        pix = crop.load()
        for y in range(crop.height):
            for x in range(crop.width):
                r,g,b,a = pix[x,y]
                if not ((r>205 and g>165 and b<170) or (r>225 and g>225 and b>225)):
                    pix[x,y]=(r,g,b,0)
    elif name == "nuvem-hero":
        pix = crop.load()
        for y in range(crop.height):
            for x in range(crop.width):
                r,g,b,a = pix[x,y]
                if r<95 and g<160 and b<185:
                    pix[x,y]=(r,g,b,0)
    alpha_bbox = crop.getchannel("A").getbbox()
    if alpha_bbox:
        crop = crop.crop(alpha_bbox)
        crop.save(OUT / f"{name}.png", optimize=True)
        saved.append((name, crop))

logo = Image.open(ROOT / "dist/assets/logo-original.png").convert("RGBA")
logo = logo.crop((250, 140, 850, 535))
pixels = logo.load()
for y in range(logo.height):
    for x in range(logo.width):
        r, g, b, _ = pixels[x, y]
        # A imagem fornecida tem papel quase branco; remover só essa área.
        whiteness = min(r, g, b)
        if whiteness > 244 and max(r, g, b) - whiteness < 15:
            pixels[x, y] = (r, g, b, 0)
logo.save(OUT / "logo-desenho.png", optimize=True)
saved.append(("logo-desenho", logo))

# Ilustração principal: o segundo SVG perde parte do desenho à direita.
# A referência completa enviada pelo usuário fornece essa peça inteira.
reference = Image.open(ROOT / "referencias/referencia-pagina.png").convert("RGBA")
hero = reference.crop((518, 96, 1122, 579))
px = hero.load()
for y in range(hero.height):
    for x in range(hero.width):
        edge = min(1, x / 55, y / 24, (hero.height - 1 - y) / 28)
        r, g, b, _ = px[x, y]
        px[x, y] = (r, g, b, max(0, min(255, round(255 * edge))))
hero.save(OUT / "ilustracao-principal.png", optimize=True)
saved.append(("ilustracao-principal", hero))

# Pequenos pictogramas da faixa de atividades e do botão de contato.
REFERENCE_ICONS = {
    "icone-relogio": (194, 1027, 233, 1068),
    "icone-bale": (442, 1025, 484, 1069),
    "icone-cross-kids": (590, 1023, 638, 1070),
    "icone-maca": (765, 1025, 808, 1069),
    "icone-instagram": (343, 459, 380, 497),
}
for name, box in REFERENCE_ICONS.items():
    icon = reference.crop(box)
    rgba = icon.load()
    for y in range(icon.height):
        for x in range(icon.width):
            r, g, b, _ = rgba[x, y]
            if min(r, g, b) > 243 and max(r, g, b) - min(r, g, b) < 20:
                rgba[x, y] = (r, g, b, 0)
    icon.save(OUT / f"{name}.png", optimize=True)
    saved.append((name, icon))

thumb_w, thumb_h = 190, 150
columns = 5
rows = (len(saved) + columns - 1) // columns
sheet = Image.new("RGB", (columns * thumb_w, rows * thumb_h), "#fffaf2")
draw = ImageDraw.Draw(sheet)
for i, (name, im) in enumerate(saved):
    x = (i % columns) * thumb_w
    y = (i // columns) * thumb_h
    preview = im.copy()
    preview.thumbnail((thumb_w - 20, thumb_h - 40))
    sheet.paste(preview, (x + (thumb_w - preview.width) // 2, y + 5), preview)
    draw.text((x + 8, y + thumb_h - 26), name, fill="#123c59")
sheet.save(ROOT / "elementos-extraidos-contato.png")
print(f"{len(saved)} PNGs: {OUT}")
