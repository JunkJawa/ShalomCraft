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
    """Upright hexagram drawn with integer vertices so every edge is a clean 1 pixel line.
    W and H are the largest x and y index. The up triangle has its base on row rb_up and its apex on
    row 0, the down triangle has its base on row rb_down and its apex on row H. With an even width
    the apexes are two pixels wide."""
    d = ImageDraw.Draw(img); ax = W // 2
    def L(x0, y0, x1, y1):
        d.line([(ox + x0, oy + y0), (ox + x1, oy + y1)], fill=WHITE, width=1)
    L(ax, 0, 0, rb_up); L(ax + 1, 0, W, rb_up); L(ax, 0, ax + 1, 0); L(0, rb_up, W, rb_up)
    L(ax, H, 0, rb_down); L(ax + 1, H, W, rb_down); L(ax, H, ax + 1, H); L(0, rb_down, W, rb_down)

def hstripes(img, ys, w, ox, oy):
    d = ImageDraw.Draw(img)
    for y0, y1 in ys:
        d.rectangle([ox, oy + y0, ox + w - 1, oy + y1], fill=WHITE)

def banner_mask(kind):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    for ox in (1, 22):                      # front and back faces of the 20x40 banner
        if kind == "star": hexagram(img, ox + 4, 1 + 14, 11, 12, 3, 9)
        else: hstripes(img, [(4, 9), (30, 35)], 20, ox, 1)
    return img

def shield_mask(kind):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    if kind == "star": hexagram(img, 1 + 2, 1 + 7, 7, 8, 2, 6)
    else: hstripes(img, [(2, 4), (17, 19)], 12, 1, 1)
    return img

for kind, name in (("star", "star_of_david"), ("stripes", "israeli_stripes")):
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
