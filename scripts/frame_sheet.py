"""Tile images into contact sheets so a whole video can be reviewed in a few Reads.

Usage:
  frame_sheet.py dir <png_dir> <out_prefix> [per_sheet=6]
      tiles every PNG in png_dir (e.g. validator review screenshots), 2 columns, filename labels
  frame_sheet.py video <file.mp4> <out.png> [n=6]
      grabs n evenly spaced frames (skipping the first/last 5%) and tiles them
Run with ~/tools/.venv/bin/python (needs Pillow; ffmpeg on PATH for video mode).
"""
import glob, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw


def tile(paths, out, labels=None, width=800):
    ims = [Image.open(p).convert("RGB") for p in paths]
    h = int(ims[0].height * width / ims[0].width)
    rows = (len(ims) + 1) // 2
    sheet = Image.new("RGB", (width * 2, h * rows), "black")
    d = ImageDraw.Draw(sheet)
    for i, im in enumerate(ims):
        x, y = (i % 2) * width, (i // 2) * h
        sheet.paste(im.resize((width, h)), (x, y))
        if labels:
            d.text((x + 6, y + 6), labels[i], fill="yellow")
    sheet.save(out)
    print(out)


mode = sys.argv[1]
if mode == "dir":
    fs = sorted(glob.glob(str(Path(sys.argv[2]) / "*.png")))
    per = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    for k in range(0, len(fs), per):
        tile(fs[k:k + per], f"{sys.argv[3]}_{k // per}.png", [Path(f).name for f in fs[k:k + per]], width=640)
elif mode == "video":
    vid, out = sys.argv[2], sys.argv[3]
    n = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    dur = float(subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", vid],
                               capture_output=True, text=True).stdout)
    ts = [dur * (0.05 + 0.9 * i / max(n - 1, 1)) for i in range(n)]
    tmp = Path(tempfile.mkdtemp())
    paths = []
    for i, t in enumerate(ts):
        p = tmp / f"f{i}.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.1f}", "-i", vid, "-frames:v", "1", str(p)], check=True)
        paths.append(p)
    tile(paths, out, [f"{int(t // 60)}:{int(t % 60):02d}" for t in ts])
else:
    sys.exit(__doc__)
