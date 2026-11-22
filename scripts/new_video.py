"""Scaffold a video-study project and/or one video inside it.

Usage: python3 new_video.py <project_dir> <slug>
  slug = vN_<name>, e.g. v1_basics, v5_midterm  (name = part after "vN_")
Creates (only what is missing, never overwrites):
  <project>/PRODUCTION_GUIDE.md          from references/production_guide.md
  <project>/intermediate/common/          ko_setup.py, ui.py, seg.py, build.py
  <project>/intermediate/<slug>/src/      video_<name>.py, part_<name>_narration.py, generate_tts_<name>.py
  <project>/final/, <project>/sources/
"""
import re, shutil, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
proj, slug = Path(sys.argv[1]).expanduser(), sys.argv[2]
if not re.fullmatch(r"v\d+_[a-z0-9]+", slug):
    sys.exit("slug must look like v1_basics (lowercase, digits)")
name = slug.split("_", 1)[1]

for d in ("final", "sources", "intermediate/common", f"intermediate/{slug}/src"):
    (proj / d).mkdir(parents=True, exist_ok=True)


def put(src, dst, sub=None):
    if dst.exists():
        print(f"keep    {dst}")
        return
    text = src.read_text()
    dst.write_text(text.replace("NAME", sub) if sub else text)
    print(f"create  {dst}")


put(SKILL / "references" / "production_guide.md", proj / "PRODUCTION_GUIDE.md")
for f in (SKILL / "assets" / "common").glob("*.py"):
    put(f, proj / "intermediate" / "common" / f.name)
for f in (SKILL / "assets" / "template").glob("*.py"):
    put(f, proj / "intermediate" / slug / "src" / f.name.replace("NAME", name), sub=name)
gi = proj / ".gitignore"
if not gi.exists():
    gi.write_text("intermediate/*/media/\nintermediate/*/audio/\nintermediate/*/output/\n")
print(f"\nnext: write intermediate/{slug}/brief.md, then edit src/part_{name}_narration.py")
