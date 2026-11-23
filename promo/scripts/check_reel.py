"""Check a rendered reel and write a contact sheet. Usage: python check_reel.py <mp4> <sheet.png> [N=16]
Checks: 1080x1920, 26-38 s, <50 MB, audio stream. Sheet = N evenly spaced frames (ffmpeg only)."""
import json, os, subprocess, sys
mp4, sheet = sys.argv[1], sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 16
p = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height:format=duration,size", "-of", "json", mp4]))
v = next(s for s in p["streams"] if s["codec_type"] == "video"); a = [s for s in p["streams"] if s["codec_type"] == "audio"]
dur = float(p["format"]["duration"]); mb = int(p["format"]["size"]) / 1e6
res = {"1080x1920": (v["width"], v["height"]) == (1080, 1920), "duration 26-38s": 26 <= dur <= 38, "size <50MB": mb < 50, "audio": bool(a)}
print(f"{v['width']}x{v['height']} {v['codec_name']} {dur:.1f}s {mb:.1f}MB audio={bool(a)}")
for k, ok in res.items(): print(("OK  " if ok else "FAIL"), k)
cols = 8
subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-vf", f"fps={n / dur:.4f},scale=270:-1,tile={cols}x{-(-n // cols)}", "-frames:v", "1", sheet])
print("sheet:", sheet, "(Read it: safe zone y 10-75%, caption ~70%, no overlap)")
sys.exit(0 if all(res.values()) else 1)
