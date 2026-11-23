"""Voice-over + timeline builder. Usage: python scripts/tts.py [EdgeTTSVoiceName]"""
import asyncio, json, subprocess, sys, edge_tts

VOICE = sys.argv[1] if len(sys.argv) > 1 else "ko-KR-InJoonNeural"  # <- the single voice setting
RATE = "+0%"  # never faster than +8%
assert int(RATE.strip("+%")) <= 8

R = json.load(open("src/reel.json"))
L = [(l["id"], l["scene"], l["rows"]) for l in R["lines"]]
SAY = R["say"]
PRE_GAP = R["preGap"]
GAP = 0.08
LEAD = 0.1

def spoken(rows):
    t = " ".join(rows).replace("|", "")
    for k, v in SAY.items(): t = t.replace(k, v)
    return t

async def one(i, t, retry=2):
    for n in range(retry):
        try:
            await edge_tts.Communicate(t, VOICE, rate=RATE).save(f"public/tts/{i}.raw.mp3")
            subprocess.check_call(["ffmpeg","-v","error","-y","-i",f"public/tts/{i}.raw.mp3","-af","silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse","-b:a","128k",f"public/tts/{i}.mp3"]); return
        except Exception:
            if n == retry - 1: raise
async def main():
    await asyncio.gather(*[one(i, spoken(r)) for i, _, r in L])
asyncio.run(main())

t = 0.3; out = []
for i, s, rows in L:
    for r in rows: assert len(r.replace("|", "")) <= 16, r
    t += PRE_GAP.get(i, 0)
    d = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"public/tts/{i}.mp3"]))
    ph = [(ri, p) for ri, r in enumerate(rows) for p in r.split("|") if p.strip()]
    w = [max(1, len(p.replace(" ", ""))) for _, p in ph]; tot = sum(w); c = 0; phs = []
    for (ri, p), wi in zip(ph, w):
        phs.append(dict(row=ri, text=p, start=round(t + d * c / tot, 3), end=round(t + d * (c + wi) / tot, 3))); c += wi
    out.append(dict(id=i, scene=s, rows=[r.split("|") for r in rows], phrases=phs, start=round(t, 3), dur=round(d, 3), say=spoken(rows)))
    t += d + GAP
total = round(t + 0.4, 3)
names = []
for o in out:
    if o["scene"] not in names: names.append(o["scene"])
def sstart(n):
    f = next(o["start"] for o in out if o["scene"] == n)
    return 0 if n == names[0] else f - (0.8 if n == "demo" else LEAD)
scenes = {n: dict(from_=round(sstart(n), 3), to=round(sstart(names[i + 1]) if i + 1 < len(names) else total, 3)) for i, n in enumerate(names)}
json.dump(dict(voice=VOICE, rate=RATE, lines=out, scenes=scenes, total=total), open("src/timeline.json", "w"), ensure_ascii=False, indent=1)
print(VOICE, "total", total)
for o in out: print(o["id"], o["start"], o["dur"], o["say"])
