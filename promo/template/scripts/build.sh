#!/bin/bash
# Usage: npm run build:voice -- [EdgeTTSVoiceName]   (default ko-KR-InJoonNeural)
set -e
cd "$(dirname "$0")/.."
export PATH="$HOME/.local/node/bin:$PATH"
PY="$HOME/tools/.venv/bin/python"
VOICE="${1:-ko-KR-InJoonNeural}"
$PY scripts/tts.py "$VOICE"
# Companies: export REMOTION_LICENSE_KEY=<key>. Individuals who qualify may use "free-license". Unset = no flag.
LK=(); [ -n "$REMOTION_LICENSE_KEY" ] && LK=(--license-key="$REMOTION_LICENSE_KEY")
npx remotion render Reel out/video-study-reel.mp4 --codec=h264 --concurrency=2 "${LK[@]}"
npx remotion still Cover out/cover.png "${LK[@]}"
