"""Korean defaults for every video in this project.
Import after `from video_utils.manim_helpers import *`.
"""
from manim import Text, MarkupText
KO_FONT = "Apple SD Gothic Neo"  # CMU Serif (skill default) has no Hangul
Text.set_default(font=KO_FONT)
MarkupText.set_default(font=KO_FONT)
VOICE = "ko-KR-SunHiNeural"
# Edge-TTS Korean pace measured 2026-11-22: ~230 syllables/min (spaces excluded).
SYLLABLES_PER_MIN = 230
