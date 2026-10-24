#!/usr/bin/env python3
"""讀 GitHub not-important issues -> not_interested.json（冪等，以 type+city+name 去重）"""
import json, re, subprocess, os
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, "not_interested.json")
js = json.loads(subprocess.check_output(["gh","issue","list","-R","1234yyyyyy/taiwan-food-guide","--label","not-important","--state","all","--limit","500","--json","number,createdAt,state,body"]))
HINTS = ["夜市","老街","市場","漁港","海鮮","溫泉","步道","廟","宮","寺","博物館","公園","濕地","牛肉麵","滷肉飯","魯肉飯","小吃","火鍋","咖啡","甜點","冰","麵","飯","湯","羹","粿","餅","茶","燒烤","拉麵","便當","早餐","素"]
items = {}
if os.path.exists(OUT):
    for it in json.load(open(OUT, encoding="utf-8")): items[(it["type"], it["city"], it.get("attraction",""), it["name"])] = it
for iss in js:
    for line in (iss.get("body") or "").splitlines():
        m = re.match(r"\s*-\s*\[(景點|餐廳)\]\s*(.*?)\s*\|\s*#(\S+)", line)
        if not m: continue
        kind, rest, aid = m.groups(); hint = ""
        hm = re.search(r"\s*（(.*)）\s*$", rest)
        if hm: hint, rest = hm.group(1), rest[:hm.start()]
        parts = [p.strip() for p in rest.split(" / ")]
        typ = "attraction" if kind == "景點" else "restaurant"
        city, name = parts[0], parts[-1]; att = parts[1] if typ == "restaurant" and len(parts) > 2 else ""
        cats = [k for k in HINTS if k in name + hint + att] if True else []
        items.setdefault((typ, city, att, name), {"type": typ, "city": city, "attraction": att, "name": name, "anchor": aid,
            "desc": hint, "category_hints": cats, "issue": iss["number"], "date": iss["createdAt"][:10]})
json.dump(sorted(items.values(), key=lambda r: (r["date"], r["city"])), open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(items)} not-interested items; open issues: {[i['number'] for i in js if i['state']=='OPEN']}")
