#!/usr/bin/env python3
"""Cross checks the Java registrations against assets and data. Run from the project root: python3 tools/validate.py"""
import glob, json, os, re, sys

A = "src/main/resources/assets/shalomcraft"
D = "src/main/resources/data/shalomcraft"
java = "".join(open(f).read() for f in ("src/main/java/com/shalomcraft/ModItems.java", "src/main/java/com/shalomcraft/ModBlocks.java"))
items = set(re.findall(r'(?:edible|plain|gem|registerSimpleItem|registerItem|registerSimpleBlockItem|ITEMS\.register)\("([a-z_]+)"', java))
blocks = set(re.findall(r'BLOCKS\.register\("([a-z_]+)"', java))
lang = json.load(open(A + "/lang/en_us.json"))
bad = []

for f in glob.glob("src/main/resources/**/*.json", recursive=True):
    try: json.load(open(f))
    except Exception as e: bad.append(("bad json", f, str(e)))

for n in sorted(items):
    if n in blocks:
        if f"block.shalomcraft.{n}" not in lang: bad.append(("lang block", n))
        if not os.path.exists(f"{A}/blockstates/{n}.json"): bad.append(("blockstate", n))
        if not os.path.exists(f"{D}/loot_table/blocks/{n}.json"): bad.append(("loot table", n))
    else:
        if f"item.shalomcraft.{n}" not in lang: bad.append(("lang item", n))
        if not os.path.exists(f"{A}/textures/item/{n}.png"): bad.append(("item texture", n))
    if not os.path.exists(f"{A}/models/item/{n}.json"): bad.append(("item model", n))

def model_file(ref): return f"{A}/models/{ref.split(':')[1]}.json"
for bs in glob.glob(A + "/blockstates/*.json"):
    j = json.load(open(bs))
    refs = [v["model"] for v in j["variants"].values()] if "variants" in j else [p["apply"]["model"] for p in j["multipart"]]
    for r in set(refs):
        if not os.path.exists(model_file(r)): bad.append(("missing block model", bs, r))
for mf in glob.glob(A + "/models/**/*.json", recursive=True):
    j = json.load(open(mf))
    for t in (j.get("textures") or {}).values():
        if not t.startswith("#") and not os.path.exists(f"{A}/textures/{t.split(':')[1]}.png"):
            bad.append(("missing texture", mf, t))
    for o in j.get("overrides", []):
        if not os.path.exists(model_file(o["model"])): bad.append(("missing override model", mf, o["model"]))
    if "parent" in j and j["parent"].startswith("shalomcraft:") and not os.path.exists(model_file(j["parent"])):
        bad.append(("missing parent", mf, j["parent"]))

if os.path.exists(A + "/sounds.json"):
    for ev, d in json.load(open(A + "/sounds.json")).items():
        for s in d["sounds"]:
            nm = s["name"] if isinstance(s, dict) else s
            if not os.path.exists(f"{A}/sounds/{nm.split(':')[1]}.ogg"): bad.append(("missing sound", ev, nm))
        if d.get("subtitle") and d["subtitle"] not in lang: bad.append(("missing subtitle lang", d["subtitle"]))

known_extra = {"israeli_stripes", "star_of_david", "israeli_side_stripes"}
for f in glob.glob(D + "/recipe/*.json"):
    for m in re.findall(r'shalomcraft:([a-z_]+)', open(f).read()):
        if m not in items and m not in known_extra and m not in ("candle_lighters", "shofar_horns"):
            bad.append(("recipe refs unknown", os.path.basename(f), m))

print(f"items {len(items)}, blocks {len(blocks)}, recipes {len(glob.glob(D + '/recipe/*.json'))}, problems: {bad if bad else 'none'}")
sys.exit(1 if bad else 0)
