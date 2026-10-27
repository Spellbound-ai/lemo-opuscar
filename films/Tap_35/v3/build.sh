#!/bin/sh
# Rebuild Tap_35 v3: stable-shot B-roll (shots.py + ocr.py -> clean.json -> edl.py) + graphics + original narration.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
LIB=${LIB:-$(cd "$HERE/../../.." && pwd)}
export LIB
cd "$HERE"
python3 shots.py && python3 ocr.py && python3 edl.py   # needs tesseract; clean.json is rebuilt by hand-review step (see README in commit)
python3 -c "import json; from edl import EDL; json.dump([[a,b,c] for a,b,c,d in EDL], open('edl.json','w'))"
python3 bgtrack.py
cd "$LIB"
node core/render/video.mjs "$HERE" --fps 24 --workers 4 --out "$HERE/out/video.mp4"
"$LIB/.venv/bin/python" "$HERE/mix.py"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/out/full.mp4" 24
