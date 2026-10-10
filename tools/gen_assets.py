#!/usr/bin/env python3
"""Generates ShalomCraft textures, models, lang and recipes. Run from the project root."""
import json, math, os
from PIL import Image

ROOT = os.path.join("src", "main", "resources")
ASSETS = os.path.join(ROOT, "assets", "shalomcraft")
DATA = os.path.join(ROOT, "data", "shalomcraft", "recipe")
TEX = os.path.join(ASSETS, "textures", "item")
for d in (TEX, os.path.join(ASSETS, "textures", "block"), os.path.join(ASSETS, "models", "item"),
          os.path.join(ASSETS, "models", "block"), os.path.join(ASSETS, "blockstates"),
          os.path.join(ASSETS, "lang"), DATA):
    os.makedirs(d, exist_ok=True)

# ---------- pixel helpers ----------
OUT = (68, 40, 24, 255)

def canvas():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 0))

def mix(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3]) + (255,)

def blob(img, cx, cy, rx, ry, base, outline=OUT, hole=None):
    """Shaded ellipse with outline. hole=(rx, ry) cuts a centre hole (bagels)."""
    px = img.load()
    def inside(x, y, rx_, ry_):
        return ((x + .5 - cx) / rx_) ** 2 + ((y + .5 - cy) / ry_) ** 2 <= 1.0
    for y in range(16):
        for x in range(16):
            if hole and inside(x, y, *hole):
                continue
            if inside(x, y, rx, ry):
                edge = False
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    out_ = not (0 <= nx < 16 and 0 <= ny < 16) or not inside(nx, ny, rx, ry) or \
                        (hole and inside(nx, ny, *hole))
                    if out_:
                        edge = True
                if edge:
                    px[x, y] = outline
                else:
                    shade = 1.12 if (x - cx) + (y - cy) < -1 else (0.86 if (x - cx) + (y - cy) > 2 else 1.0)
                    px[x, y] = mix(base, shade)

def dots(img, pts, c):
    px = img.load()
    for x, y in pts:
        if 0 <= x < 16 and 0 <= y < 16 and px[x, y][3]:
            px[x, y] = c

def rect(img, x0, y0, x1, y1, c):
    px = img.load()
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px[x, y] = c

def outline_rect(img, x0, y0, x1, y1, fill, o=OUT):
    rect(img, x0, y0, x1, y1, o)
    rect(img, x0 + 1, y0 + 1, x1 - 1, y1 - 1, fill)

GOLDEN = (214, 148, 70, 255)
DOUGH = (236, 214, 166, 255)
CREAM = (250, 246, 236, 255)
SALMON = (236, 122, 92, 255)
BROWN = (150, 92, 48, 255)
CHOC = (92, 52, 34, 255)

# ---------- item art ----------
art = {}

def challah_dough():
    i = canvas(); blob(i, 8, 8, 7, 4.2, DOUGH)
    for k in range(-5, 6, 3):
        dots(i, [(8 + k, 6), (9 + k, 7), (10 + k, 8), (9 + k, 9)], mix(DOUGH, .8))
    return i
art["challah_dough"] = challah_dough

def challah():
    i = canvas(); blob(i, 8, 8, 7.2, 4.6, GOLDEN)
    for k in range(-6, 7, 3):
        dots(i, [(8 + k, 5), (9 + k, 6), (10 + k, 7), (9 + k, 8), (8 + k, 9), (9 + k, 10)], mix(GOLDEN, .72))
    dots(i, [(5, 6), (8, 5), (11, 6), (7, 7)], (255, 226, 150, 255))
    return i
art["challah"] = challah

def bagel_dough():
    i = canvas(); blob(i, 8, 8, 6, 5.5, DOUGH, hole=(1.6, 1.6)); return i
art["bagel_dough"] = bagel_dough

def raw_latke():
    i = canvas(); blob(i, 8, 9, 6.4, 3.8, (222, 204, 160, 255))
    dots(i, [(5, 8), (8, 7), (10, 9), (7, 10), (11, 8)], (180, 150, 100, 255)); return i
art["raw_latke"] = raw_latke

def latke():
    i = canvas(); blob(i, 6, 10, 5.2, 3.2, (196, 128, 56, 255)); blob(i, 9, 7, 5.6, 3.4, GOLDEN)
    dots(i, [(8, 6), (11, 7), (7, 8), (10, 9), (5, 10), (8, 11)], mix(GOLDEN, .7))
    dots(i, [(7, 5), (10, 6)], (255, 214, 130, 255)); return i
art["latke"] = latke

def matzo():
    i = canvas(); outline_rect(i, 2, 2, 13, 13, (232, 208, 160, 255))
    for (x, y) in [(4, 4), (7, 4), (10, 4), (5, 7), (8, 7), (11, 7), (4, 10), (7, 10), (10, 10)]:
        dots(i, [(x, y)], (176, 128, 72, 255))
    rect(i, 12, 3, 12, 12, (200, 160, 100, 255)); rect(i, 3, 12, 12, 12, (200, 160, 100, 255))
    dots(i, [(3, 3), (4, 3), (3, 4)], (250, 234, 196, 255)); return i
art["matzo"] = matzo

def matzo_ball_soup():
    i = canvas()
    blob(i, 8, 9, 7, 5, (236, 232, 222, 255))      # bowl
    blob(i, 8, 8, 5.4, 3.0, (230, 178, 70, 255))   # broth
    blob(i, 7, 7, 2.2, 1.8, CREAM)                 # matzo ball
    dots(i, [(11, 8), (5, 9)], (240, 140, 50, 255))  # carrot bits
    dots(i, [(10, 7)], (90, 150, 60, 255)); return i
art["matzo_ball_soup"] = matzo_ball_soup

def gefilte_fish():
    i = canvas(); blob(i, 5.5, 10, 4.2, 2.8, (232, 226, 208, 255)); blob(i, 10, 8, 4.6, 3.0, (240, 234, 216, 255))
    blob(i, 10, 6, 1.7, 1.5, (240, 134, 40, 255)); dots(i, [(10, 6)], (255, 190, 100, 255))
    dots(i, [(8, 9), (12, 9), (4, 10)], (200, 190, 168, 255)); return i
art["gefilte_fish"] = gefilte_fish

def rugelach():
    i = canvas()
    for (cx, cy) in [(5, 9), (8, 7), (11, 9)]:
        blob(i, cx, cy, 3.2, 2.6, GOLDEN)
        dots(i, [(cx - 1, cy), (cx, cy - 1), (cx + 1, cy)], CHOC)
    dots(i, [(4, 8), (8, 6), (10, 8), (6, 10)], (252, 246, 236, 255)); return i
art["rugelach"] = rugelach

def babka():
    i = canvas(); blob(i, 8, 8, 7, 5, (190, 118, 60, 255))
    for k in range(-5, 6):
        y = 8 + (1 if k % 2 else -1)
        dots(i, [(8 + k, y), (8 + k, y + 1)], CHOC)
    dots(i, [(5, 5), (9, 5), (12, 6)], (240, 190, 120, 255)); return i
art["babka"] = babka

def gelt():
    i = canvas(); blob(i, 6, 9, 4.2, 4.2, (240, 190, 40, 255)); blob(i, 10, 7, 4.2, 4.2, (250, 210, 60, 255))
    blob(i, 10, 7, 2.2, 2.2, (232, 168, 28, 255), outline=(250, 214, 80, 255))
    dots(i, [(8, 5), (9, 5)], (255, 250, 200, 255)); return i
art["gelt"] = gelt

def afikomen():
    i = canvas(); outline_rect(i, 3, 2, 12, 11, (232, 208, 160, 255))
    dots(i, [(5, 4), (8, 4), (6, 7), (9, 7)], (176, 128, 72, 255))
    outline_rect(i, 2, 8, 13, 14, (246, 244, 238, 255), o=(120, 130, 160, 255))
    rect(i, 3, 10, 12, 10, (70, 110, 190, 255)); rect(i, 3, 12, 12, 12, (70, 110, 190, 255))
    dots(i, [(13, 3), (14, 2)], (255, 220, 90, 255)); return i
art["afikomen"] = afikomen

def bagel_base(img, y=8):
    blob(img, 8, y, 6.8, 5.6, (212, 150, 78, 255), hole=(1.5, 1.4))
    dots(img, [(4, y - 2), (6, y - 4), (10, y - 4), (12, y - 1), (9, y + 3)], (250, 232, 180, 255))

def bagel():
    i = canvas(); bagel_base(i); return i
art["bagel"] = bagel

def cream_blob(i):
    blob(i, 8, 7, 5.2, 2.6, CREAM, outline=(176, 172, 160, 255))
    dots(i, [(6, 6), (9, 7)], (255, 255, 255, 255))

def lox_strip(i):
    blob(i, 8, 9, 5.6, 2.2, SALMON, outline=(150, 70, 56, 255))
    dots(i, [(5, 9), (8, 8), (10, 10), (7, 10)], (252, 176, 150, 255))

def bagel_with_cream_cheese():
    i = canvas(); bagel_base(i); cream_blob(i); return i
art["bagel_with_cream_cheese"] = bagel_with_cream_cheese

def bagel_with_lox():
    i = canvas(); bagel_base(i); lox_strip(i); return i
art["bagel_with_lox"] = bagel_with_lox

def bagel_with_lox_and_cream_cheese():
    i = canvas(); bagel_base(i); cream_blob(i); lox_strip(i)
    dots(i, [(7, 7), (9, 8)], (255, 255, 255, 255)); return i
art["bagel_with_lox_and_cream_cheese"] = bagel_with_lox_and_cream_cheese

def cream_cheese():
    i = canvas(); outline_rect(i, 3, 6, 12, 12, CREAM, o=(120, 118, 108, 255))
    rect(i, 3, 5, 12, 6, (190, 196, 210, 255)); rect(i, 3, 5, 12, 5, (120, 118, 108, 255))
    dots(i, [(5, 8), (6, 8), (10, 10)], (255, 255, 255, 255))
    rect(i, 5, 9, 10, 9, (200, 200, 190, 255)); return i
art["cream_cheese"] = cream_cheese

def lox():
    i = canvas(); blob(i, 6, 9, 5, 2.4, SALMON, outline=(150, 70, 56, 255))
    blob(i, 10, 6, 5, 2.4, (244, 138, 104, 255), outline=(150, 70, 56, 255))
    dots(i, [(5, 9), (8, 9), (9, 6), (12, 6)], (252, 188, 164, 255)); return i
art["lox"] = lox

for name, fn in art.items():
    fn().save(os.path.join(TEX, name + ".png"))

# ---------- menorah block texture: left half gold, right half candle ----------
b = Image.new("RGBA", (16, 16))
gold = [(168, 112, 24), (214, 160, 40), (244, 202, 80), (252, 232, 140)]
candle = [(150, 190, 226), (186, 216, 242), (216, 234, 250), (240, 248, 255)]
for y in range(16):
    for x in range(16):
        pal = gold if x < 8 else candle
        idx = (x + y * 2) % 4 if (x % 8) < 7 else 0
        b.putpixel((x, y), pal[idx] + (255,))
# wick region (uv 0,8 to 4,12): dark wick with a slightly lighter core
for y in range(8, 12):
    for x in range(0, 4):
        b.putpixel((x, y), (46, 38, 34, 255) if (x + y) % 3 else (92, 78, 66, 255))
b.save(os.path.join(ASSETS, "textures", "block", "menorah.png"))

# ---------- item models ----------
for name in list(art.keys()):
    with open(os.path.join(ASSETS, "models", "item", name + ".json"), "w") as f:
        json.dump({"parent": "minecraft:item/generated",
                   "textures": {"layer0": "shalomcraft:item/" + name}}, f, indent=2)
with open(os.path.join(ASSETS, "models", "item", "menorah.json"), "w") as f:
    json.dump({"parent": "shalomcraft:block/menorah"}, f, indent=2)

# ---------- menorah block model ----------
GOLD_UV, CANDLE_UV, WICK_UV = [0, 0, 8, 8], [8, 0, 16, 8], [0, 8, 4, 12]
def faces(uv):
    return {d: {"uv": uv, "texture": "#0"} for d in ("north", "east", "south", "west", "up", "down")}

els = []
def cube(frm, to, uv):
    els.append({"from": frm, "to": to, "faces": faces(uv)})

cube([1, 0, 6], [15, 1, 10], GOLD_UV)       # base
cube([7, 1, 7], [9, 3, 9], GOLD_UV)         # stem, centred on x=8
cube([1, 3, 7], [15, 4, 9], GOLD_UV)        # arm bar, centred on x=8
for i in range(9):
    x = 2 + i * 1.5                          # nine candles from x=2 to x=14, centred on x=8, all over the base
    top = 11 if i == 4 else 8                # the shamash (centre) stands taller
    cube([x - 0.7, 3, 7.3], [x + 0.7, 4.6, 8.7], GOLD_UV)       # cup
    cube([x - 0.5, 4, 7.5], [x + 0.5, top, 8.5], CANDLE_UV)     # candle
    cube([x - 0.2, top, 7.8], [x + 0.2, top + 1.2, 8.2], WICK_UV)  # wick
with open(os.path.join(ASSETS, "models", "block", "menorah.json"), "w") as f:
    json.dump({"parent": "minecraft:block/block",
               "textures": {"0": "shalomcraft:block/menorah", "particle": "shalomcraft:block/menorah"},
               "elements": els}, f, indent=2)

with open(os.path.join(ASSETS, "blockstates", "menorah.json"), "w") as f:
    json.dump({"variants": {
        "facing=north": {"model": "shalomcraft:block/menorah"},
        "facing=east": {"model": "shalomcraft:block/menorah", "y": 90},
        "facing=south": {"model": "shalomcraft:block/menorah", "y": 180},
        "facing=west": {"model": "shalomcraft:block/menorah", "y": 270}}}, f, indent=2)

# ---------- lang ----------
names = {n: n.replace("_", " ").title().replace(" And ", " and ").replace(" With ", " with ") for n in art}
names["menorah"] = "Menorah"
lang = {"item.shalomcraft." + n: v for n, v in names.items() if n != "menorah"}
lang["block.shalomcraft.menorah"] = "Menorah"
lang["itemGroup.shalomcraft"] = "ShalomCraft"
with open(os.path.join(ASSETS, "lang", "en_us.json"), "w") as f:
    json.dump(lang, f, indent=2, ensure_ascii=False)

# ---------- recipes ----------
def it(i):
    return {"tag": i[1:]} if i.startswith("#") else {"item": i}

def result(i, n=1):
    return {"id": i, "count": n}

def write(name, data):
    with open(os.path.join(DATA, name + ".json"), "w") as f:
        json.dump(data, f, indent=2)

def shapeless(name, ings, out, n=1, category="misc"):
    write(name, {"type": "minecraft:crafting_shapeless", "category": category,
                 "ingredients": [it(i) for i in ings], "result": result("shalomcraft:" + out, n)})

def cook(name, src, out, xp=0.35):
    for kind, t in (("smelting", 200), ("smoking", 100), ("campfire_cooking", 600)):
        write(f"{name}_from_{kind}", {"type": "minecraft:" + kind, "category": "food",
                                       "ingredient": it(src), "result": {"id": "shalomcraft:" + out},
                                       "experience": xp, "cookingtime": t})

def pot(name, ings, out, n=1, container=None, time=200):
    d = {"type": "farmersdelight:cooking", "cookingtime": time, "experience": 1.0,
         "ingredients": [it(i) for i in ings], "recipe_book_tab": "meals",
         "result": result("shalomcraft:" + out, n)}
    if container:
        d["container"] = {"id": container}
    write(name, d)

DOUGHFD = "farmersdelight:wheat_dough"
ONION = "farmersdelight:onion"

shapeless("challah_dough", [DOUGHFD, DOUGHFD, "minecraft:egg", "minecraft:honey_bottle"], "challah_dough", 1, "food")
cook("challah", "shalomcraft:challah_dough", "challah", 0.5)
shapeless("bagel_dough", [DOUGHFD, "minecraft:sugar"], "bagel_dough", 1, "food")
cook("bagel", "shalomcraft:bagel_dough", "bagel")
shapeless("raw_latke", ["minecraft:potato", ONION, "minecraft:egg"], "raw_latke", 2, "food")
cook("latke", "shalomcraft:raw_latke", "latke")
cook("matzo", DOUGHFD, "matzo")
pot("matzo_ball_soup", ["shalomcraft:matzo", "minecraft:egg", "minecraft:chicken", "minecraft:carrot", ONION],
    "matzo_ball_soup", 1, container="minecraft:bowl")
pot("gefilte_fish", ["minecraft:cod", "minecraft:egg", ONION, "minecraft:carrot", "shalomcraft:matzo"],
    "gefilte_fish", 2)
shapeless("rugelach", [DOUGHFD, "minecraft:sugar", "minecraft:cocoa_beans", "minecraft:sweet_berries"],
          "rugelach", 4, "food")
shapeless("babka", [DOUGHFD, DOUGHFD, "minecraft:cocoa_beans", "minecraft:cocoa_beans", "minecraft:sugar",
                    "minecraft:egg", "minecraft:honey_bottle"], "babka", 1, "food")
shapeless("gelt", ["minecraft:cocoa_beans", "minecraft:cocoa_beans", "minecraft:gold_nugget", "minecraft:sugar"],
          "gelt", 3, "food")
shapeless("afikomen", ["shalomcraft:matzo", "shalomcraft:matzo", "shalomcraft:matzo", "minecraft:honey_bottle",
                       "minecraft:paper"], "afikomen", 1, "food")
shapeless("cream_cheese", ["minecraft:milk_bucket"], "cream_cheese", 3, "food")
shapeless("lox", ["minecraft:salmon", "minecraft:sugar"], "lox", 2, "food")
B, CC, L = "shalomcraft:bagel", "shalomcraft:cream_cheese", "shalomcraft:lox"
BCC, BL = "shalomcraft:bagel_with_cream_cheese", "shalomcraft:bagel_with_lox"
shapeless("bagel_with_cream_cheese", [B, CC], "bagel_with_cream_cheese", 1, "food")
shapeless("bagel_with_lox", [B, L], "bagel_with_lox", 1, "food")
shapeless("bagel_with_lox_and_cream_cheese", [B, CC, L], "bagel_with_lox_and_cream_cheese", 1, "food")
shapeless("bagel_with_lox_and_cream_cheese_from_cream_cheese_bagel", [BCC, L],
          "bagel_with_lox_and_cream_cheese", 1, "food")
shapeless("bagel_with_lox_and_cream_cheese_from_lox_bagel", [BL, CC],
          "bagel_with_lox_and_cream_cheese", 1, "food")
write("menorah", {"type": "minecraft:crafting_shaped", "category": "misc",
                  "pattern": ["G G", "GGG", " G "],
                  "key": {"G": it("minecraft:gold_ingot")},
                  "result": result("shalomcraft:menorah", 1)})
print("assets generated:", len(art), "items")

# ---------- block loot table and mining tag ----------
LOOT = os.path.join(ROOT, "data", "shalomcraft", "loot_table", "blocks")
TAGS = os.path.join(ROOT, "data", "minecraft", "tags", "block", "mineable")
os.makedirs(LOOT, exist_ok=True); os.makedirs(TAGS, exist_ok=True)
with open(os.path.join(LOOT, "menorah.json"), "w") as f:
    json.dump({"type": "minecraft:block", "random_sequence": "shalomcraft:blocks/menorah",
               "pools": [{"rolls": 1.0, "bonus_rolls": 0.0,
                          "conditions": [{"condition": "minecraft:survives_explosion"}],
                          "entries": [{"type": "minecraft:item", "name": "shalomcraft:menorah"}]}]}, f, indent=2)
with open(os.path.join(TAGS, "pickaxe.json"), "w") as f:
    json.dump({"replace": False, "values": ["shalomcraft:menorah"]}, f, indent=2)

# ---------- banner patterns: Star of David and Israeli side stripes ----------
from PIL import ImageDraw
BANNER_TEX = os.path.join(ASSETS, "textures", "entity", "banner")
SHIELD_TEX = os.path.join(ASSETS, "textures", "entity", "shield")
PATTERN_DATA = os.path.join(ROOT, "data", "shalomcraft", "banner_pattern")
PATTERN_TAG = os.path.join(ROOT, "data", "shalomcraft", "tags", "banner_pattern", "pattern_item")
for d in (BANNER_TEX, SHIELD_TEX, PATTERN_DATA, PATTERN_TAG):
    os.makedirs(d, exist_ok=True)

WHITE = (255, 255, 255, 255)

def hexagram(img, ox, oy, W, H, rb_down, rb_up):
    """Upright hexagram, then thickened with a 2x2 brush so it stays bold and readable once the game
    blurs it. W and H are the largest x and y index of the thin star; the thick result is one pixel
    wider and taller, so with an odd W and H the final star has an even size and centres exactly."""
    thin = Image.new("L", (W + 1, H + 1), 0); d = ImageDraw.Draw(thin); ax = W // 2
    def L(x0, y0, x1, y1):
        d.line([(x0, y0), (x1, y1)], fill=255, width=1)
    L(ax, 0, 0, rb_up); L(ax, 0, W, rb_up); L(0, rb_up, W, rb_up)
    L(ax, H, 0, rb_down); L(ax, H, W, rb_down); L(0, rb_down, W, rb_down)
    px = thin.load(); out = img.load()
    for y in range(H + 1):
        for x in range(W + 1):
            if px[x, y]:
                for dx in (0, 1):
                    for dy in (0, 1):
                        out[ox + x + dx, oy + y + dy] = WHITE

def hstripes(img, ys, w, ox, oy):
    d = ImageDraw.Draw(img)
    for y0, y1 in ys:
        d.rectangle([ox, oy + y0, ox + w - 1, oy + y1], fill=WHITE)

def vstripes(img, xs, h, ox, oy):
    d = ImageDraw.Draw(img)
    for x0, x1 in xs:
        d.rectangle([ox + x0, oy, ox + x1, oy + h - 1], fill=WHITE)

def banner_mask(kind):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    for ox in (1, 22):                      # front and back faces of the 20x40 banner
        if kind == "star": hexagram(img, ox + 3, 1 + 13, 12, 12, 2, 10)   # 14x14, centred on (10, 20)
        elif kind == "stripes": hstripes(img, [(4, 9), (30, 35)], 20, ox, 1)
        else: vstripes(img, [(0, 1), (18, 19)], 40, ox, 1)
    return img

def shield_mask(kind):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    if kind == "star": hexagram(img, 1 + 2, 1 + 7, 6, 6, 2, 4)           # 8x8, centred on (6, 11)
    elif kind == "stripes": hstripes(img, [(2, 4), (17, 19)], 12, 1, 1)
    else: vstripes(img, [(0, 1), (10, 11)], 22, 1, 1)
    return img

for kind, name in (("star", "star_of_david"), ("stripes", "israeli_stripes"), ("side", "israeli_side_stripes")):
    banner_mask(kind).save(os.path.join(BANNER_TEX, name + ".png"))
    shield_mask(kind).save(os.path.join(SHIELD_TEX, name + ".png"))
    with open(os.path.join(PATTERN_DATA, name + ".json"), "w") as f:
        json.dump({"asset_id": "shalomcraft:" + name,
                   "translation_key": "block.shalomcraft.banner." + name}, f, indent=2)

# the loom item for the star (the stripes only exist inside the flag recipe)
with open(os.path.join(PATTERN_TAG, "star_of_david.json"), "w") as f:
    json.dump({"values": ["shalomcraft:star_of_david"]}, f, indent=2)

icon = canvas(); outline_rect(icon, 2, 1, 13, 14, (246, 240, 222, 255), o=(120, 100, 70, 255))
ic = ImageDraw.Draw(icon)
for a0 in (0, 60):
    pts = [(7.5 + 4.2 * math.cos(math.radians(a0 + 90 + k * 120)),
            7.5 + 4.2 * math.sin(math.radians(a0 + 90 + k * 120))) for k in range(3)]
    for k in range(3):
        ic.line([pts[k], pts[(k + 1) % 3]], fill=(46, 92, 190, 255), width=1)
icon.save(os.path.join(TEX, "star_of_david_banner_pattern.png"))
with open(os.path.join(ASSETS, "models", "item", "star_of_david_banner_pattern.json"), "w") as f:
    json.dump({"parent": "minecraft:item/generated",
               "textures": {"layer0": "shalomcraft:item/star_of_david_banner_pattern"}}, f, indent=2)

# language: item, hover text and a name for every banner colour
with open(os.path.join(ASSETS, "lang", "en_us.json")) as f:
    lang = json.load(f)
lang["item.shalomcraft.star_of_david_banner_pattern"] = "Banner Pattern"
lang["item.shalomcraft.star_of_david_banner_pattern.desc"] = "Star of David"
for color in ("white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray",
              "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"):
    nice = color.replace("_", " ").title()
    lang[f"block.shalomcraft.banner.star_of_david.{color}"] = f"{nice} Star of David"
    lang[f"block.shalomcraft.banner.israeli_stripes.{color}"] = f"{nice} Israeli Stripes"
with open(os.path.join(ASSETS, "lang", "en_us.json"), "w") as f:
    json.dump(lang, f, indent=2, ensure_ascii=False)

# recipes: the pattern item, and a ready made Israeli flag banner
shapeless("star_of_david_banner_pattern", ["minecraft:paper", "minecraft:blue_dye", "minecraft:gold_nugget"],
          "star_of_david_banner_pattern", 1, "misc")
write("israeli_flag_banner", {
    "type": "minecraft:crafting_shapeless", "category": "misc",
    "ingredients": [it("minecraft:white_banner"), it("minecraft:blue_dye"), it("minecraft:blue_dye")],
    "result": {"id": "minecraft:white_banner", "count": 1, "components": {
        "minecraft:banner_patterns": [
            {"pattern": "shalomcraft:israeli_stripes", "color": "blue"},
            {"pattern": "shalomcraft:star_of_david", "color": "blue"}],
        "minecraft:item_name": '{"text":"Israeli Flag"}'}}})

# ---------- kippah and tallit: dyeable worn cloth ----------
ARMOR_TEX = os.path.join(ASSETS, "textures", "models", "armor")
DYE_TAG = os.path.join(ROOT, "data", "minecraft", "tags", "item")
os.makedirs(ARMOR_TEX, exist_ok=True); os.makedirs(DYE_TAG, exist_ok=True)
CLEAR = (0, 0, 0, 0)
TRIM = (206, 164, 62, 255)
STRIPE = (34, 56, 128, 255)
THREAD = (232, 226, 212, 255)

def weave(x, y):
    v = 236 + ((x * 7 + y * 13) % 5) - 2           # neutral light grey so any dye reads true
    return (v, v, v, 255)

def fill(img, x0, y0, x1, y1):
    px = img.load()
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px[x, y] = weave(x, y)

def paint(img, x0, y0, x1, y1, c):
    px = img.load()
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px[x, y] = c

# 64x32 armor layer, shared by both items: head area for the kippah, body and arm area for the tallit
a_base = Image.new("RGBA", (64, 32), CLEAR); a_over = Image.new("RGBA", (64, 32), CLEAR)

# kippah: top of the head plus a three pixel band around the crown, gold trim on the lowest row
fill(a_base, 8, 0, 15, 7)                       # top
fill(a_base, 0, 8, 31, 9)                       # right, front, left, back sides, upper two rows
paint(a_over, 0, 10, 31, 10, TRIM)              # trim row on the same sides

# tallit: draped over the shoulders, hanging down the front, back and sides to the waist
faces = [(20, 20, 27, 31), (32, 20, 39, 31), (16, 20, 19, 31), (28, 20, 31, 31)]   # front, back, right, left
KNOT = (190, 178, 150, 255)
fill(a_base, 20, 16, 27, 19)                    # shoulders from above
for x0, y0, x1, y1 in faces:
    fill(a_base, x0, y0, x1, y0 + 7)            # cloth hangs eight rows, the hem is row y0+7
    paint(a_over, x0, y0 + 4, x1, y0 + 4, STRIPE)
    paint(a_over, x0, y0 + 6, x1, y0 + 6, STRIPE)
    # tzitzit: knots just under the hem and strands hanging below, at both corners of each face
    corner_cols = sorted({x0, min(x0 + 1, x1), max(x1 - 1, x0), x1})
    for x in corner_cols:
        a_over.putpixel((x, y0 + 8), KNOT)
        for y in range(y0 + 9, y1 + 1):
            a_over.putpixel((x, y), THREAD if (x + y) % 2 == 0 else (214, 206, 188, 255))
# upper arms: a short sleeve of cloth over the shoulder, striped edge
fill(a_base, 44, 16, 47, 19)
for x0, x1 in ((40, 43), (44, 47), (48, 51), (52, 55)):
    fill(a_base, x0, 20, x1, 22)
    paint(a_over, x0, 22, x1, 22, STRIPE)
a_base.save(os.path.join(ARMOR_TEX, "cloth_layer_1.png"))
a_over.save(os.path.join(ARMOR_TEX, "cloth_layer_1_overlay.png"))
# layer 2 is only requested for leggings, written empty so a missing file never shows up in logs
Image.new("RGBA", (64, 32), CLEAR).save(os.path.join(ARMOR_TEX, "cloth_layer_2.png"))
Image.new("RGBA", (64, 32), CLEAR).save(os.path.join(ARMOR_TEX, "cloth_layer_2_overlay.png"))

def split(img):
    """Moves the dark outline into an overlay layer so dye never tints it."""
    base = img.copy(); over = canvas(); bp = base.load(); op = over.load()
    for y in range(16):
        for x in range(16):
            if bp[x, y] == OUT:
                op[x, y] = OUT; bp[x, y] = CLEAR
    return base, over

def kippah_icon():
    i = canvas(); blob(i, 8, 11, 6.6, 5.6, (238, 238, 242, 255))
    px = i.load()
    for y in range(12, 16):
        for x in range(16): px[x, y] = CLEAR
    base, over = split(i); bp = base.load(); op = over.load()
    for x in range(16):
        if bp[x, 11][3]:
            op[x, 11] = TRIM; bp[x, 11] = CLEAR
    for x in range(16):
        if op[x, 11][3]: op[x, 12] = OUT
    return base, over

def tallit_icon():
    i = canvas(); outline_rect(i, 2, 2, 13, 13, (238, 238, 242, 255))
    base, over = split(i); op = over.load()
    for x in range(3, 13):
        op[x, 8] = STRIPE; op[x, 10] = STRIPE
    for x in (3, 4, 11, 12):                    # tassels hanging from the corners
        op[x, 14] = KNOT; op[x, 15] = THREAD
    return base, over

for name, fn in (("kippah", kippah_icon), ("tallit", tallit_icon)):
    base, over = fn()
    base.save(os.path.join(TEX, name + ".png")); over.save(os.path.join(TEX, name + "_overlay.png"))
    with open(os.path.join(ASSETS, "models", "item", name + ".json"), "w") as f:
        json.dump({"parent": "minecraft:item/generated",
                   "textures": {"layer0": "shalomcraft:item/" + name,
                                "layer1": "shalomcraft:item/" + name + "_overlay"}}, f, indent=2)

# allow dyeing in a crafting grid with any dye, same as leather armor
with open(os.path.join(DYE_TAG, "dyeable.json"), "w") as f:
    json.dump({"replace": False, "values": ["shalomcraft:kippah", "shalomcraft:tallit"]}, f, indent=2)

with open(os.path.join(ASSETS, "lang", "en_us.json")) as f:
    lang = json.load(f)
lang["item.shalomcraft.kippah"] = "Kippah"
lang["item.shalomcraft.tallit"] = "Tallit"
with open(os.path.join(ASSETS, "lang", "en_us.json"), "w") as f:
    json.dump(lang, f, indent=2, ensure_ascii=False)

write("kippah", {"type": "minecraft:crafting_shaped", "category": "equipment",
                 "pattern": ["WW"], "key": {"W": it("minecraft:white_wool")},
                 "result": result("shalomcraft:kippah", 1)})
write("tallit", {"type": "minecraft:crafting_shaped", "category": "equipment",
                 "pattern": ["WWW", "WWW", "S S"],
                 "key": {"W": it("minecraft:white_wool"), "S": it("minecraft:string")},
                 "result": result("shalomcraft:tallit", 1)})

# ================= v0.3.0: more banner patterns, candle flames, candlesticks, mezuzah =================
def outline_pixels(img):
    """Adds a 1 pixel dark outline around the opaque pixels of a 16x16 sprite."""
    out = img.copy(); src = img.load(); dst = out.load()
    for y in range(16):
        for x in range(16):
            if src[x, y][3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 16 and 0 <= ny < 16 and src[nx, ny][3]:
                        dst[x, y] = OUT; break
    return out

def load_lang():
    with open(os.path.join(ASSETS, "lang", "en_us.json")) as f: return json.load(f)
def save_lang(d):
    with open(os.path.join(ASSETS, "lang", "en_us.json"), "w") as f: json.dump(d, f, indent=2, ensure_ascii=False)

COLORS = ("white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray",
          "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black")

# --- loom items for the two stripe patterns ---
lang = load_lang()
for name, label in (("israeli_stripes", "Israeli Stripes"), ("israeli_side_stripes", "Israeli Side Stripes")):
    with open(os.path.join(PATTERN_TAG, name + ".json"), "w") as f:
        json.dump({"values": ["shalomcraft:" + name]}, f, indent=2)
    icon = canvas(); outline_rect(icon, 2, 1, 13, 14, (246, 240, 222, 255), o=(120, 100, 70, 255))
    if name == "israeli_stripes":
        rect(icon, 3, 3, 12, 4, (46, 92, 190, 255)); rect(icon, 3, 11, 12, 12, (46, 92, 190, 255))
    else:
        rect(icon, 3, 2, 4, 13, (46, 92, 190, 255)); rect(icon, 11, 2, 12, 13, (46, 92, 190, 255))
    icon.save(os.path.join(TEX, name + "_banner_pattern.png"))
    with open(os.path.join(ASSETS, "models", "item", name + "_banner_pattern.json"), "w") as f:
        json.dump({"parent": "minecraft:item/generated",
                   "textures": {"layer0": "shalomcraft:item/" + name + "_banner_pattern"}}, f, indent=2)
    lang[f"item.shalomcraft.{name}_banner_pattern"] = "Banner Pattern"
    lang[f"item.shalomcraft.{name}_banner_pattern.desc"] = label
    for color in COLORS:
        lang[f"block.shalomcraft.banner.{name}.{color}"] = f"{color.replace('_', ' ').title()} {label}"
    shapeless(name + "_banner_pattern", ["minecraft:paper", "minecraft:blue_dye", "minecraft:blue_dye"],
              name + "_banner_pattern", 1, "misc")

# --- shared candle flame texture (a static flame, vertical gradient) ---
fl = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
for y in range(16):
    c = (255, 244, 170) if y < 4 else ((255, 178, 46) if y < 10 else (232, 96, 24))
    for x in range(16):
        fl.putpixel((x, y), c + (255,))
fl.save(os.path.join(ASSETS, "textures", "block", "candle_flame.png"))

SILVER = [(112, 120, 134), (166, 174, 188), (208, 214, 224), (240, 244, 250)]
def metal_texture(name, metal):
    t = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            pal = metal if x < 8 else candle
            t.putpixel((x, y), pal[(x + y * 2) % 4 if (x % 8) < 7 else 0] + (255,))
    for y in range(8, 12):                    # wick region
        for x in range(0, 4):
            t.putpixel((x, y), (46, 38, 34, 255) if (x + y) % 3 else (92, 78, 66, 255))
    t.save(os.path.join(ASSETS, "textures", "block", name + ".png"))
metal_texture("gold_candlesticks", gold)
metal_texture("silver_candlesticks", SILVER)

# --- menorah: one flame model per candle, blockstate becomes multipart with a lit_N property per candle ---
FLAME_UV = [0, 0, 16, 16]
FLAME_EXTRA = {"shade": False}
def flame_cube(x, top):
    face = {"uv": FLAME_UV, "texture": "#f"}
    return {"from": [x - 0.7, top + 1.0, 7.3], "to": [x + 0.7, top + 3.0, 8.7], "shade": False,
            "neoforge_data": {"block_light": 15, "sky_light": 15, "ambient_occlusion": False},
            "faces": {d: dict(face) for d in ("north", "east", "south", "west", "up", "down")}}

def write_model(path, data):
    with open(os.path.join(ASSETS, "models", "block", path + ".json"), "w") as f: json.dump(data, f, indent=2)

for i in range(9):
    x = 2 + i * 1.5; top = 11 if i == 4 else 8
    write_model(f"menorah_flame_{i}", {"textures": {"f": "shalomcraft:block/candle_flame", "particle": "shalomcraft:block/candle_flame"},
                                       "elements": [flame_cube(x, top)]})
YROT = {"north": 0, "east": 90, "south": 180, "west": 270}
def rot(model, facing):
    d = {"model": model}
    if YROT[facing]: d["y"] = YROT[facing]
    return d
parts = []
for fc in YROT:
    parts.append({"when": {"facing": fc}, "apply": rot("shalomcraft:block/menorah", fc)})
for i in range(9):
    for fc in YROT:
        parts.append({"when": {"AND": [{"facing": fc}, {f"lit_{i}": "true"}]},
                      "apply": rot(f"shalomcraft:block/menorah_flame_{i}", fc)})
with open(os.path.join(ASSETS, "blockstates", "menorah.json"), "w") as f: json.dump({"multipart": parts}, f, indent=2)

# --- Shabbat candlesticks: gold and silver pairs, two candles lit one at a time ---
def cube_faces(uv):
    return {d: {"uv": uv, "texture": "#0"} for d in ("north", "east", "south", "west", "up", "down")}

def candlestick_elements():
    els = []
    def add(frm, to, uv):
        els.append({"from": frm, "to": to, "faces": cube_faces(uv)})
    for cx in (4.5, 11.5):
        add([cx - 2.0, 0, 6.0], [cx + 2.0, 1, 10.0], GOLD_UV)       # round foot
        add([cx - 0.8, 1, 7.2], [cx + 0.8, 5, 8.8], GOLD_UV)         # stem
        add([cx - 1.6, 5, 6.4], [cx + 1.6, 6, 9.6], GOLD_UV)         # drip cup
        add([cx - 0.9, 6, 7.1], [cx + 0.9, 12, 8.9], CANDLE_UV)      # candle
        add([cx - 0.2, 12, 7.8], [cx + 0.2, 13.2, 8.2], WICK_UV)     # wick
    return els
for metal in ("gold", "silver"):
    write_model(f"{metal}_candlesticks", {"parent": "minecraft:block/block",
                "textures": {"0": f"shalomcraft:block/{metal}_candlesticks", "particle": f"shalomcraft:block/{metal}_candlesticks"},
                "elements": candlestick_elements()})
    with open(os.path.join(ASSETS, "models", "item", f"{metal}_candlesticks.json"), "w") as f:
        json.dump({"parent": f"shalomcraft:block/{metal}_candlesticks"}, f, indent=2)
    parts = []
    for fc in YROT:
        parts.append({"when": {"facing": fc}, "apply": rot(f"shalomcraft:block/{metal}_candlesticks", fc)})
    for i in range(2):
        for fc in YROT:
            parts.append({"when": {"AND": [{"facing": fc}, {f"lit_{i}": "true"}]},
                          "apply": rot(f"shalomcraft:block/candlestick_flame_{i}", fc)})
    with open(os.path.join(ASSETS, "blockstates", f"{metal}_candlesticks.json"), "w") as f:
        json.dump({"multipart": parts}, f, indent=2)
for i, cx in enumerate((4.5, 11.5)):
    el = flame_cube(cx, 12)
    write_model(f"candlestick_flame_{i}", {"textures": {"f": "shalomcraft:block/candle_flame", "particle": "shalomcraft:block/candle_flame"},
                                           "elements": [el]})

# --- mezuzah: wall mounted case on a slant, gold and silver ---
GLYPH = (40, 34, 30, 255)
def mezuzah_texture(name, metal):
    t = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y in range(8):                                  # plain region for the sides and back, uv 8,0 to 16,8
        for x in range(8, 16): t.putpixel((x, y), metal[(x + y) % 3 + 1] + (255,))
    for y in range(12):                                 # front face, 5 wide and 12 tall, uv 0,0 to 5,12
        for x in range(5):
            c = metal[0] if y in (0, 1, 10, 11) else (metal[3] if y in (2, 9) else metal[1])
            t.putpixel((x, y), c + (255,))
    for y in range(3, 8):                               # shin on the front
        for x in range(5):
            if (x % 2 == 0) or y == 7: t.putpixel((x, y), GLYPH)
    t.save(os.path.join(ASSETS, "textures", "block", name + ".png"))
    return t
mez = {"gold": mezuzah_texture("gold_mezuzah", gold), "silver": mezuzah_texture("silver_mezuzah", SILVER)}

def mezuzah_model(metal, angle):
    plain = [8, 0, 16, 8]
    f = {"south": {"uv": [0, 0, 5, 12], "texture": "#0"}}
    for d in ("north", "east", "west", "up", "down"): f[d] = {"uv": plain, "texture": "#0"}
    return {"textures": {"0": f"shalomcraft:block/{metal}_mezuzah", "particle": f"shalomcraft:block/{metal}_mezuzah"},
            "elements": [{"from": [5.5, 2, 0], "to": [10.5, 14, 1.4],
                          "rotation": {"origin": [8, 8, 0.7], "axis": "z", "angle": angle}, "faces": f}]}

# the model has its back on the north side of the block and its face towards south
MYROT = {"south": 0, "west": 90, "north": 180, "east": 270}
for metal in ("gold", "silver"):
    write_model(f"{metal}_mezuzah_a", mezuzah_model(metal, 22.5))
    write_model(f"{metal}_mezuzah_b", mezuzah_model(metal, -22.5))
    variants = {}
    for fc, y in MYROT.items():
        for flipped, suffix in (("false", "a"), ("true", "b")):
            v = {"model": f"shalomcraft:block/{metal}_mezuzah_{suffix}"}
            if y: v["y"] = y
            variants[f"facing={fc},flipped={flipped}"] = v
    with open(os.path.join(ASSETS, "blockstates", f"{metal}_mezuzah.json"), "w") as f:
        json.dump({"variants": variants}, f, indent=2)
    # inventory sprite: draw the case large, tilt it, shrink it, outline it
    SS = 8; big = Image.new("RGBA", (16 * SS, 16 * SS), (0, 0, 0, 0)); bd = ImageDraw.Draw(big)
    cw, ch = 5 * SS, 12 * SS; x0, y0 = (16 * SS - cw) // 2, (16 * SS - ch) // 2
    pal = gold if metal == "gold" else SILVER
    for ry in range(12):
        c = pal[0] if ry in (0, 1, 10, 11) else (pal[3] if ry in (2, 9) else pal[1])
        bd.rectangle([x0, y0 + ry * SS, x0 + cw - 1, y0 + (ry + 1) * SS - 1], fill=c + (255,))
    for ry in range(3, 8):
        for rx in range(5):
            if rx % 2 == 0 or ry == 7:
                bd.rectangle([x0 + rx * SS, y0 + ry * SS, x0 + (rx + 1) * SS - 1, y0 + (ry + 1) * SS - 1], fill=GLYPH)
    big = big.rotate(-22.5, resample=Image.BICUBIC)
    small = big.resize((16, 16), Image.BOX)
    sp = small.load()
    for yy in range(16):
        for xx in range(16):
            r, g, b2, a = sp[xx, yy]
            sp[xx, yy] = (r, g, b2, 255) if a >= 110 else (0, 0, 0, 0)
    outline_pixels(small).save(os.path.join(TEX, f"{metal}_mezuzah.png"))
    with open(os.path.join(ASSETS, "models", "item", f"{metal}_mezuzah.json"), "w") as f:
        json.dump({"parent": "minecraft:item/generated", "textures": {"layer0": f"shalomcraft:item/{metal}_mezuzah"}}, f, indent=2)

# --- loot tables, mining tag, lighters tag ---
for block in ("gold_candlesticks", "silver_candlesticks", "gold_mezuzah", "silver_mezuzah"):
    with open(os.path.join(LOOT, block + ".json"), "w") as f:
        json.dump({"type": "minecraft:block", "random_sequence": "shalomcraft:blocks/" + block,
                   "pools": [{"rolls": 1.0, "bonus_rolls": 0.0,
                              "conditions": [{"condition": "minecraft:survives_explosion"}],
                              "entries": [{"type": "minecraft:item", "name": "shalomcraft:" + block}]}]}, f, indent=2)
with open(os.path.join(TAGS, "pickaxe.json"), "w") as f:
    json.dump({"replace": False, "values": ["shalomcraft:menorah", "shalomcraft:gold_candlesticks",
              "shalomcraft:silver_candlesticks", "shalomcraft:gold_mezuzah", "shalomcraft:silver_mezuzah"]}, f, indent=2)
ITEM_TAGS = os.path.join(ROOT, "data", "shalomcraft", "tags", "item"); os.makedirs(ITEM_TAGS, exist_ok=True)
with open(os.path.join(ITEM_TAGS, "candle_lighters.json"), "w") as f:
    json.dump({"replace": False, "values": ["minecraft:flint_and_steel", "minecraft:fire_charge"]}, f, indent=2)

# --- lang and recipes ---
for k, v in (("gold_candlesticks", "Gold Shabbat Candlesticks"), ("silver_candlesticks", "Silver Shabbat Candlesticks"),
             ("gold_mezuzah", "Gold Mezuzah"), ("silver_mezuzah", "Silver Mezuzah")):
    lang["block.shalomcraft." + k] = v
save_lang(lang)

SILVER_INGOT = [{"tag": "c:ingots/silver"}, {"item": "minecraft:iron_ingot"}]
SILVER_NUGGET = [{"tag": "c:nuggets/silver"}, {"item": "minecraft:iron_nugget"}]
write("gold_candlesticks", {"type": "minecraft:crafting_shaped", "category": "misc",
      "pattern": ["C C", "I I", "III"], "key": {"C": {"tag": "minecraft:candles"}, "I": it("minecraft:gold_ingot")},
      "result": result("shalomcraft:gold_candlesticks", 1)})
write("silver_candlesticks", {"type": "minecraft:crafting_shaped", "category": "misc",
      "pattern": ["C C", "I I", "III"], "key": {"C": {"tag": "minecraft:candles"}, "I": SILVER_INGOT},
      "result": result("shalomcraft:silver_candlesticks", 1)})
write("gold_mezuzah", {"type": "minecraft:crafting_shapeless", "category": "misc",
      "ingredients": [it("minecraft:gold_nugget")] * 3 + [it("minecraft:paper"), it("minecraft:ink_sac")],
      "result": result("shalomcraft:gold_mezuzah", 1)})
write("silver_mezuzah", {"type": "minecraft:crafting_shapeless", "category": "misc",
      "ingredients": [SILVER_NUGGET] * 3 + [it("minecraft:paper"), it("minecraft:ink_sac")],
      "result": result("shalomcraft:silver_mezuzah", 1)})
