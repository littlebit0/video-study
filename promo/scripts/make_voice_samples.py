"""Same sentence in several Korean voices -> mp3 files to send to the user.
Usage: python make_voice_samples.py <outdir> ["sentence"] [--say-yuna]"""
import asyncio, subprocess, sys, pathlib, edge_tts
VOICES = ["ko-KR-InJoonNeural", "ko-KR-SunHiNeural", "ko-KR-HyunsuMultilingualNeural"]
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
args = [a for a in sys.argv[2:] if not a.startswith("--")]
text = args[0] if args else "강의 녹음, 아직도 듣고 있어요? 스킬 하나면 영상이 알아서 나와요. 좋아요와 팔로우 부탁드려요!"
async def main():
    for i, v in enumerate(VOICES, 1):
        await edge_tts.Communicate(text, v, rate="+0%").save(str(out / f"{i}_{v}.mp3"))
        print(out / f"{i}_{v}.mp3")
asyncio.run(main())
if "--say-yuna" in sys.argv:  # offline macOS voice
    aiff = out / "yuna.aiff"
    subprocess.check_call(["say", "-v", "Yuna", "-o", str(aiff), text])
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", str(aiff), str(out / "4_macOS_Yuna.mp3")]); aiff.unlink()
