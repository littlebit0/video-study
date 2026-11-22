"""Split a long transcript into parts at lines that mark a new week/session (e.g. '2주차', '10주차').

Usage: python3 split_by_marker.py <transcript.txt> <out_dir> [regex]
Default regex: ^\\s*\\d+\\s*주차   -> files rec_w02.txt, rec_w10.txt, ...
Prints each part's line range so you can check the cut points.
"""
import re, sys
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
pat = re.compile(sys.argv[3] if len(sys.argv) > 3 else r"^\s*(\d+)\s*주차")
out.mkdir(parents=True, exist_ok=True)
lines = src.read_text(errors="ignore").splitlines(keepends=True)
cuts = [(i, m.group(1)) for i, l in enumerate(lines) if (m := pat.match(l)) and len(l) < 40]
if not cuts:
    sys.exit("no marker lines found; pass a regex as the 3rd argument")
for n, (start, wk) in enumerate(cuts):
    end = cuts[n + 1][0] if n + 1 < len(cuts) else len(lines)
    name = f"rec_w{int(wk):02d}.txt"
    (out / name).write_text("".join(lines[start:end]))
    print(f"{name}: lines {start + 1}-{end} ({end - start} lines)")
if cuts[0][0] > 0:
    print(f"note: lines 1-{cuts[0][0]} come before the first marker and were not written")
