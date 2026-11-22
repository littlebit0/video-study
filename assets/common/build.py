"""Render + mux + concat + captions for one project.

Usage: ~/tools/.venv/bin/python intermediate/common/build.py <slug> [--quality h|l] [--only Scene1,Scene2]
Expects intermediate/<slug>/src/video_<slug>.py, part_<slug>_narration.py (SCENE_ORDER),
and audio/video_<slug>/<Scene>.mp3 + durations.json from the TTS step.
"""
import argparse, os, subprocess, sys, json, shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # linear-algebra-videos/
PY = os.path.expanduser("~/tools/.venv/bin/python")
FONT = "Apple SD Gothic Neo"


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{cmd[:4]}... failed:\n{r.stderr[-1500:]}")
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--quality", default="h", choices=["h", "l"])
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--captions-only", action="store_true", help="skip rendering; re-join output/*.mp4 and redo captions")
    a = ap.parse_args()

    proj = ROOT / "intermediate" / a.slug
    name = a.slug.split("_", 1)[1] if a.slug[:1] == "v" and a.slug[1:2].isdigit() else a.slug  # v5_midterm -> midterm
    src = proj / "src"
    sys.path.insert(0, str(src))
    narr = __import__(f"part_{name}_narration")
    scenes = a.only.split(",") if a.only else narr.SCENE_ORDER
    audio = proj / "audio" / f"video_{name}"
    out = proj / "output"; out.mkdir(exist_ok=True)
    final = ROOT / "final" / a.slug; final.mkdir(parents=True, exist_ok=True)
    qflag, fps, qdir = ("-qh", "24", "1080p24") if a.quality == "h" else ("-ql", "15", "480p15")

    def render(sc):
        r = run([PY, "-m", "manim", "render", qflag, "--fps", fps, "--disable_caching",
                 f"src/video_{name}.py", sc], cwd=proj)
        for line in (r.stdout + r.stderr).splitlines():
            if line.startswith("WARNING "):   # Seg timing / caption-zone warnings
                print(f"  [{sc}] {line}", flush=True)
        vid = proj / "media" / "videos" / f"video_{name}" / qdir / f"{sc}.mp4"
        muxed = out / f"{sc}.mp4"
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(vid), "-i", str(audio / f"{sc}.mp3"),
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(muxed)])
        print(f"  done {sc}", flush=True)
        return muxed

    print(f"Rendering {len(scenes)} scenes ({qdir}, {a.jobs} jobs)...", flush=True)
    if not a.captions_only:
        with ThreadPoolExecutor(a.jobs) as ex:
            list(ex.map(render, scenes))
    if a.only:
        return

    lst = out / "concat.txt"
    lst.write_text("".join(f"file '{out / f'{sc}.mp4'}'\n" for sc in narr.SCENE_ORDER))
    mp4 = final / f"{a.slug}.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(mp4)])

    sys.path.insert(0, os.path.expanduser("~/tools"))
    from video_utils.captions import generate_srt
    srt = final / f"{a.slug}.srt"
    # Scenes are joined at their muxed length (video ends a few frames before the audio),
    # so time captions from those lengths, not from the TTS scene durations, to avoid drift.
    timing = json.loads((audio / "durations.json").read_text())
    for sc in narr.SCENE_ORDER:
        timing[sc]["scene_duration"] = float(run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                                                  "-of", "csv=p=0", str(out / f"{sc}.mp4")]).stdout.strip())
    actual = out / "durations_actual.json"; actual.write_text(json.dumps(timing))
    generate_srt(str(actual), str(srt))

    style = (f"FontName={FONT},FontSize=13,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,"
             "Outline=1,BorderStyle=4,BackColour=&H99000000,MarginV=6,MarginL=40,MarginR=40")
    tmp_srt = out / "captions.srt"; shutil.copy(srt, tmp_srt)   # filter path must avoid spaces/quotes
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4),
         "-vf", f"subtitles=captions.srt:force_style='{style}'",
         "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "copy",
         str(final / f"{a.slug}_captioned.mp4")], cwd=out)
    dur = run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)]).stdout.strip()
    print(f"Final: {mp4} ({float(dur)/60:.1f} min) + {srt.name} + {a.slug}_captioned.mp4")


if __name__ == "__main__":
    main()
