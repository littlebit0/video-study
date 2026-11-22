"""Segment timing for narration-synced Manim scenes.

Usage in video_<name>.py:
    Seg = make_seg(DURATIONS_FILE)
    s = Seg(self, "s1_seg1")
    s.play(Write(title), rt=1.0)   # tracks elapsed time
    s.at("CUE")                    # wait until the narrator reaches {CUE}
    s.end()                        # pad to the audio length, then a 0.5 s fade

The 0.5 s fade in end() matches the 0.5 s silence edge-tts puts between segments.
Skip it and every later segment drifts out of sync.
"""
from manim import FadeOut, Group
from video_utils.manim_helpers import make_sync_helpers

CAPTION_TOP = -2.85  # burned-in captions occupy the frame below this y


def make_seg(durations_file):
    seg_dur, cue_t, until, sync, fill = make_sync_helpers(durations_file)

    class Seg:
        def __init__(self, scene, key):
            self.s, self.k, self.e, self.d = scene, key, 0.0, seg_dur(key)

        def play(self, *anims, rt=1.0):
            self.s.play(*anims, run_time=rt)
            self.e += rt

        def at(self, cue):
            self.e = sync(self.s, self.k, cue, self.e)

        def until(self, cue):
            """Seconds left before a cue; use as run_time for a slow filler animation."""
            return until(self.k, cue, self.e)

        def end(self):
            if self.e > self.d + 0.05:
                print(f"WARNING {self.k}: animations {self.e:.2f}s exceed audio {self.d:.2f}s")
            for m in self.s.mobjects:
                if m.get_bottom()[1] < CAPTION_TOP - 0.01 and m.get_height() < 6:
                    print(f"WARNING {self.k}: {type(m).__name__} reaches y={m.get_bottom()[1]:.2f} (caption zone)")
            fill(self.s, self.d, self.e)
            self.s.play(FadeOut(Group(*self.s.mobjects)), run_time=0.5)

    return Seg
