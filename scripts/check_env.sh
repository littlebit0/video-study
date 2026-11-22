#!/usr/bin/env bash
# Check everything video-study needs. Prints "ok"/"missing" per item; exit 1 if a required item is missing.
# Install steps for anything missing: references/setup.md
PY=~/tools/.venv/bin/python
miss=0
chk() { if eval "$2" >/dev/null 2>&1; then printf 'ok       %s\n' "$1"; else printf 'missing  %s%s\n' "$1" "${3:+  ($3)}"; [ -z "$4" ] && miss=1; fi; }

chk "python env ~/tools/.venv (3.10+)"  "$PY -c 'import sys; assert sys.version_info >= (3,10)'"
chk "manim"                             "$PY -c 'import manim'"
chk "edge-tts"                          "$PY -c 'import edge_tts'"
chk "pydub"                             "$PY -c 'import pydub'"
chk "pymupdf"                           "$PY -c 'import pymupdf'"
chk "Pillow"                            "$PY -c 'import PIL'"
chk "ffmpeg on PATH"                    "command -v ffmpeg"
chk "ffprobe on PATH"                   "command -v ffprobe"
chk "ffmpeg libass (burned captions)"   "ffmpeg -hide_banner -filters | grep -q ' subtitles '"
chk "latex + dvisvgm (MathTex)"         "command -v latex && command -v dvisvgm"
chk "notes-to-video skill"              "test -f ~/.claude/skills/notes-to-video/SKILL.md"
chk "video_utils (~/tools/video_utils)" "test -f ~/tools/video_utils/tts_edge.py"
chk "Korean font Apple SD Gothic Neo"   "test -f /System/Library/Fonts/AppleSDGothicNeo.ttc"
chk "watch skill (YouTube lectures)"    "test -f ~/.claude/skills/watch/SKILL.md" "optional" opt
chk "yt-dlp (YouTube lectures)"         "command -v yt-dlp" "optional" opt
chk "textutil (rtf/docx -> txt)"        "command -v textutil" "macOS only" opt
exit $miss
