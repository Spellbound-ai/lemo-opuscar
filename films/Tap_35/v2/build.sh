#!/bin/sh
# Rebuild Tap_35 (v2): B-roll from my-assets/ + code graphics + original narration.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
LIB=${LIB:-$(cd "$HERE/../../.." && pwd)}
export LIB
python3 "$HERE/bgtrack.py"                                   # cut my-assets/ per edl.py -> bg/ frames
cd "$LIB"
node core/render/video.mjs "$HERE" --fps 24 --workers 4 --out "$HERE/out/video.mp4"
"$LIB/.venv/bin/python" "$HERE/mix.py"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/../Tap_35_v2.mp4" 24
