#!/usr/bin/env bash
set -euo pipefail

# —— EDIT THESE TWO PATHS ——
REPO_DIR="$HOME/code/passradials-repo"	# your local clone of the GitHub repo
LOCAL_IMGS_DIR="$HOME/pass_radials/imgs"				# where your new PNGs get written (change me)
# ————————————————

PYTHON_BIN="${PYTHON_BIN:-$(command -v python3 || command -v python)}"

cd "$REPO_DIR"

# Make sure folders exist
mkdir -p img data

# Copy only PNGs from your source folder into the repo's img/
rsync -av --include='*/' --include='*.png' --exclude='*' "$LOCAL_IMGS_DIR"/ img/

# Rebuild the website manifest (required by index.html)
# If your generator lives elsewhere, adjust the path.
"$PYTHON_BIN" scripts/generate_index.py

# Commit & push only if there are real changes
git add img/ data/index.json || true
if ! git diff --cached --quiet; then
	git commit -m "Auto-sync images & index.json: $(date -u +'%Y-%m-%d %H:%M:%SZ')"
	git push origin main
else
	echo "No changes to commit."
fi
