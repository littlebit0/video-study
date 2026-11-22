"""Generate narration audio + durations.json for video NAME.
Run: ~/tools/.venv/bin/python src/generate_tts_NAME.py
Re-running reuses existing sentence mp3s; delete audio/video_NAME/ after editing narration text.
Note: edge-tts sends the narration text to Microsoft's TTS service.
"""
import sys, os
sys.path.insert(0, os.path.expanduser("~/tools"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "common"))
from pathlib import Path
from video_utils.tts_edge import generate_and_save
from ko_setup import VOICE
from part_NAME_narration import VIDEO

timing = generate_and_save(VIDEO, Path(__file__).resolve().parents[1] / "audio" / "video_NAME", voice=VOICE)
total = sum(v["scene_duration"] for k, v in timing.items() if k != "segments")
print(f"\nTOTAL {total / 60:.1f} min")
for k, v in timing.items():
    if k != "segments":
        print(f"  {k}: {v['scene_duration']:.1f}s  " + ", ".join(f"{s}={x['duration']:.1f}" for s, x in v["segments"].items()))
