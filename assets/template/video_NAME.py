"""Manim scenes for video NAME. One Scene class per key in part_NAME_narration.SCENE_ORDER.

Pattern per segment:
    s = Seg(self, "sX_segY")        # new segment
    corner tag: self.add(t) (re-add after the previous segment's fade)
    s.play(..., rt=0.6)              # keep rt short (0.5-1.2) so animations never outrun the audio
    s.at("CUE")                      # jump to the cue time
    s.end()                          # pad + 0.5 s fade (required)

Layout rules: safe area x in [-6.5, 6.5], y in [-2.85, 3.5] (captions below -2.85).
Use CText (never Text), font_size >= 24. No Hangul inside MathTex.
"""
import sys, os
sys.path.insert(0, os.path.expanduser("~/tools"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "common"))
from pathlib import Path
from video_utils.manim_helpers import *
from ko_setup import *
from ui import *
from seg import make_seg

DURATIONS_FILE = Path(__file__).resolve().parents[1] / "audio" / "video_NAME" / "durations.json"
Seg = make_seg(DURATIONS_FILE)


class S0_Intro(Scene):
    def construct(self):
        s = Seg(self, "s0_seg1")
        t = corner_tag("1 · 들어가며")
        s.play(FadeIn(t), rt=0.5)
        s.at("TITLE")
        title = CText("오늘의 주제", font_size=56, color=SOFT_WHITE).shift(UP * 1.0)
        s.play(Write(title), rt=1.0)
        s.at("QUESTION")
        q = CText("오늘의 질문: ...?", font_size=32, color=GOLD).next_to(title, DOWN, buff=0.6)
        s.play(FadeIn(q, shift=UP * 0.2), rt=0.6)
        s.end()

        s = Seg(self, "s0_seg2")
        self.add(t)
        s.at("POINT")
        eq = MathTex(r"A\mathbf{x} = \mathbf{b}", font_size=60).shift(UP * 0.5)
        s.play(Write(eq), rt=1.0)
        s.at("EXAM")
        b = bottom(banner("시험 단골 · 교수님 강조", size=28))
        s.play(FadeIn(b, shift=UP * 0.2), rt=0.6)
        s.end()
