"""Narration for video NAME (Korean). Edit freely.

Rules:
- {CUE} goes right before the word the animation should land on.
- One segment = 60-150 syllables (about 15-40 s). 2-5 segments per scene.
- Write what the TTS should *say*: "에이 엑스는 비", "3 곱하기 3", "람다", "행렬식".
  Symbols stay on screen only.
- Sentences end with . ? ! (the TTS splits on them).
"""

VIDEO = {
    "S0_Intro": {"segments": {
        "s0_seg1": (
            "오늘은 무엇을 배울까요? "
            "{TITLE} 이번 영상의 주제는 바로 이거예요. "
            "{QUESTION} 오늘의 질문 하나, 끝까지 보면 답이 나와요."
        ),
        "s0_seg2": (
            "{POINT} 핵심은 한 줄로 정리할 수 있어요. "
            "{EXAM} 그리고 이 부분은 시험에 자주 나온다고 교수님이 강조하셨어요."
        ),
    }},
}

SCENE_ORDER = list(VIDEO.keys())
