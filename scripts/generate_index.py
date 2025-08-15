#!/usr/bin/env python3
import json, re
from pathlib import Path

# Prefer 'img', fall back to 'imgs'
IMG_DIR = Path("img") if Path("img").exists() else Path("imgs")
OUT = Path("data/index.json")

PATTERN = re.compile(
	r'^(?P<country>[a-z]+)-(?P<comp>[a-z-]+)-(?P<y1>\d{4})-(?P<y2>\d{4})-(?P<h>[a-z0-9-]+)-(?P<a>[a-z0-9-]+)$',
	re.IGNORECASE
)

def title_case(slug: str) -> str:
	return " ".join(w.capitalize() for w in slug.split("-"))

def record_from_path(p: Path):
	stem = p.stem  # name without extension
	m = PATTERN.match(stem)
	if m:
		g = {k: v.lower() for k, v in m.groupdict().items()}
		season = f"{g['y1']}\u2013{g['y2']}"  # en dash
		label = f"{season} • {title_case(g['country'])} {title_case(g['comp'])} — {title_case(g['h'])} vs {title_case(g['a'])}"
		id_ = stem  # slug without extension
		sort_key = (int(g['y2']), int(g['y1']), g['country'], g['comp'], g['h'], g['a'])
	else:
		# Not matching? Still include it so it shows up.
		id_ = stem
		label = stem
		sort_key = (0, 0, "", "", "", "")
	return {"id": id_, "label": label, "img": f"{IMG_DIR}/{p.name}", "_sort": sort_key}

def main():
	OUT.parent.mkdir(parents=True, exist_ok=True)
	if not IMG_DIR.exists():
		print(f"WARNING: {IMG_DIR} does not exist; index will be empty.")
		OUT.write_text("[]", encoding="utf-8")
		return

	# Collect .png or .PNG
	files = [p for p in IMG_DIR.iterdir() if p.is_file() and p.suffix.lower() == ".png"]
	records = [record_from_path(p) for p in files]
	records.sort(key=lambda r: r["_sort"], reverse=True)
	for r in records:
		r.pop("_sort", None)

	OUT.write_text(json.dumps(records, indent=1), encoding="utf-8")
	print(f"Wrote {OUT} with {len(records)} items using '{IMG_DIR}/'")

if __name__ == "__main__":
	main()
	
