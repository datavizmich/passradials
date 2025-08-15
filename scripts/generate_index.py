#!/usr/bin/env python3
import json, re
from pathlib import Path

IMG_DIR = Path("img")
OUT = Path("data/index.json")

# england-premier-league-2024-2025-chelsea-manchester-united.png
PATTERN = re.compile(
	r'^(?P<country>[a-z]+)-(?P<comp>[a-z-]+)-(?P<y1>\d{4})-(?P<y2>\d{4})-(?P<h>[a-z-]+)-(?P<a>[a-z-]+)\.png$'
)

def title_case(slug: str) -> str:
	return " ".join(w.capitalize() for w in slug.split("-"))

def record_from_path(p: Path):
	m = PATTERN.match(p.name)
	if m:
		g = m.groupdict()
		season = f"{g['y1']}\u2013{g['y2']}"  # en dash
		label = f"{season} • {title_case(g['country'])} {title_case(g['comp'])} — {title_case(g['h'])} vs {title_case(g['a'])}"
		id_ = p.stem  # full slug without .png
		sort_key = (int(g['y2']), int(g['y1']), g['country'], g['comp'], g['h'], g['a'])
	else:
		label = p.stem
		id_ = p.stem
		sort_key = (0,0,"","","","")
	return {"id": id_, "label": label, "img": f"img/{p.name}", "_sort": sort_key}

def main():
	OUT.parent.mkdir(parents=True, exist_ok=True)
	records = [record_from_path(p) for p in IMG_DIR.glob("*.png")]
	records.sort(key=lambda r: r["_sort"], reverse=True)
	for r in records: r.pop("_sort", None)
	OUT.write_text(json.dumps(records, indent=1), encoding="utf-8")
	print(f"Wrote {OUT} with {len(records)} items.")

if __name__ == "__main__":
	main()

