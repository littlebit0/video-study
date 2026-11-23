"""Patch ~/tools/video_utils/validate_scenes.py so straight lines are checked exactly.

Problem: the stock validator compares the *axis-aligned bounding box* of every Line/Arrow with each text's box.
A diagonal arrow's box is a big rectangle, so any weight label next to a diagonal edge is reported as
"[LINE-CROSS 100%] Arrow crosses through MathTex(..)" even when it is far from the line. Dense graphs
(shortest-path, multistage, trees with diagonal edges) can then never pass.

Fix: for Line/Arrow/DashedLine test the real segment against the text box (Liang-Barsky). Curves and other
line types keep the old bounding-box test. Idempotent; keeps validate_scenes.py.orig once.

Usage: python3 patch_validator.py [path/to/validate_scenes.py]
"""
import shutil, sys
from pathlib import Path

path = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path("~/tools/video_utils/validate_scenes.py").expanduser()
src = path.read_text()
if "_seg_hits_box" in src:
    print("already patched:", path)
    sys.exit(0)

HELPER = '''def _seg_hits_box(a, b, bb, pad=0.02):
    """True if segment a-b intersects the box bb=(x_min, y_min, x_max, y_max) (Liang-Barsky)."""
    x0, y0, x1, y1 = bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad
    px, py = float(a[0]), float(a[1])
    dx, dy = float(b[0]) - px, float(b[1]) - py
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, px - x0), (dx, x1 - px), (-dy, py - y0), (dy, y1 - py)):
        if abs(p) < 1e-12:
            if q < 0:
                return False
        else:
            r = q / p
            if p < 0:
                if r > t1:
                    return False
                t0 = max(t0, r)
            else:
                if r < t0:
                    return False
                t1 = min(t1, r)
    return True


def get_all_lines(scene):'''

OLD = '''                oa = overlap_area(lbb, tbb)
                if oa <= 0:
                    continue
                txt_area = box_area(tbb)
                if txt_area <= 0:
                    continue
                pct = oa / txt_area
                if pct >= 0.15:  # line covers >15% of the text area'''
NEW = '''                txt_area = box_area(tbb)
                if txt_area <= 0:
                    continue
                if isinstance(line_mob, Line):
                    if not _seg_hits_box(line_mob.get_start(), line_mob.get_end(), tbb):
                        continue
                    pct = 1.0
                else:
                    oa = overlap_area(lbb, tbb)
                    if oa <= 0:
                        continue
                    pct = oa / txt_area
                if pct >= 0.15:  # line covers >15% of the text area'''

assert src.count("def get_all_lines(scene):") == 1 and src.count(OLD) == 1, "validate_scenes.py differs from the expected version"
new = src.replace("def get_all_lines(scene):", HELPER, 1).replace(OLD, NEW, 1)
compile(new, str(path), "exec")                       # syntax check before touching the real file
if not path.with_suffix(".py.orig").exists():
    shutil.copy(path, path.with_suffix(".py.orig"))
tmp = path.with_suffix(".py.tmp")
tmp.write_text(new)
tmp.replace(path)                                      # atomic swap: running validators never see a half-written file
print("patched:", path)
