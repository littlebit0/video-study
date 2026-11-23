#!/bin/bash
# Usage: new_reel.sh <dest> [--link-modules <existing project>] [--install]
#   --install        run npm install (downloads ~400 MB: ask the user first!)
#   --link-modules   symlink node_modules from an existing Remotion project (no download)
set -e
DEST="$1"; shift || true
[ -z "$DEST" ] && { echo "usage: new_reel.sh <dest> [--link-modules <dir>] [--install]"; exit 1; }
[ -e "$DEST" ] && { echo "$DEST already exists"; exit 1; }
HERE="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$DEST" && cp -R "$HERE/template/." "$DEST/"
mkdir -p "$DEST/out" "$DEST/public/tts"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$CHROME" ] || echo "WARN: Chrome not found; edit remotion.config.ts (setBrowserExecutable). Do not download a browser without asking."
while [ $# -gt 0 ]; do
  case "$1" in
    --link-modules) ln -s "$(cd "$2" && pwd)/node_modules" "$DEST/node_modules"
      [ -d "$2/node_modules/@remotion/media" ] || echo "WARN: $2 has no @remotion/media (needed for <Audio>/<Video>). Run: npx remotion add @remotion/media there, or use --install."
      shift 2;;
    --install) export PATH="$HOME/.local/node/bin:$PATH"; (cd "$DEST" && npm install); shift;;
    *) echo "unknown arg $1"; exit 1;;
  esac
done
echo "ready: $DEST  -> edit src/reel.json, then: cd $DEST && npm run build:voice -- [voice]"
