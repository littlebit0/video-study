"""Convert a YouTube .vtt subtitle file (from the watch skill's prepare_video.sh) into
de-duplicated "[HH:MM:SS] text" lines.

Usage: python3 vtt_to_txt.py <subtitles.ko.vtt> <out.txt>
The watch skill may report "transcript=unavailable" even when subtitles.<lang>.vtt exists;
run this on the .vtt in that case.
"""
import re, sys

out, last, t = [], "", "00:00:00"
for line in open(sys.argv[1], encoding="utf-8"):
    line = line.strip()
    m = re.match(r"(\d\d:\d\d:\d\d)\.\d+ -->", line)
    if m:
        t = m.group(1); continue
    if not line or line.startswith(("WEBVTT", "Kind:", "Language:")) or line.isdigit():
        continue
    line = re.sub(r"<[^>]+>", "", line).strip()
    if line and line != last:
        out.append(f"[{t}] {line}"); last = line
open(sys.argv[2], "w").write("\n".join(out))
print(f"{len(out)} lines -> {sys.argv[2]}")
