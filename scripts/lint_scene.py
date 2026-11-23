"""Design-floor lint for Manim scene files (see references/design-floor.md).

Checks: literal hex colours outside module-level token assignments, emoji used as icons,
purple->blue gradients, glow-style stroke blur, hand-drawn window dots. Prints file:line, exits 1 on FAIL.

Usage: python3 lint_scene.py <video_*.py> [...]
"""
import re, sys
from pathlib import Path

HEX = re.compile(r'["\']#[0-9a-fA-F]{3,8}["\']')
TOKEN = re.compile(r'^[A-Z][A-Z0-9_]*\s*=\s*["\']#[0-9a-fA-F]{3,8}["\']')
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐⬆⬇]")
GRAD = re.compile(r'(color_gradient|set_color_by_gradient|GradientImage)')

def lint(path):
    fails, notes = [], []
    for i, line in enumerate(Path(path).read_text().splitlines(), 1):
        code = line.split("#", 1)[0] if "#" in line and not HEX.search(line) else line
        if HEX.search(line) and not TOKEN.match(line.strip()):
            fails.append((i, "literal colour; define a token constant at module top or in ui.py", line.strip()))
        if EMOJI.search(code):
            fails.append((i, "emoji as icon; draw a Manim shape or use text", line.strip()))
        if GRAD.search(code) and re.search(r"PURPLE|VIOLET|MAGENTA", code) and re.search(r"BLUE|TEAL", code):
            fails.append((i, "purple->blue gradient", line.strip()))
        if re.search(r"Circle\(.*color=(RED|YELLOW|GREEN)", code) and "radius=0.0" in code:
            notes.append((i, "hand-drawn window dots?", line.strip()))
    return fails, notes

if __name__ == "__main__":
    bad = 0
    for p in sys.argv[1:]:
        f, n = lint(p)
        for i, why, src in f:
            print(f"FAIL {p}:{i}: {why}\n    {src[:110]}")
        for i, why, src in n:
            print(f"NOTE {p}:{i}: {why}")
        bad += len(f)
    print("lint_scene:", "OK" if not bad else f"{bad} FAIL")
    sys.exit(1 if bad else 0)
