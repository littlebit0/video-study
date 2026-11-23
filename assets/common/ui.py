"""Shared Manim building blocks for this project's Korean explainer videos."""
from manim import *
from video_utils.manim_helpers import CText, ACCENT, GOLD, TEAL, SOFT_WHITE, DIMMED

WARN = "#FC6255"
OK = "#83C167"
BLUE_3B = "#58C4DD"
DIMMED = "#9AA0A6"  # skill default #555555 is too faint on the dark background


def chapter_card(num, title, sub=None):
    """Big chapter title, e.g. ('1', '용어 빠른 정리')."""
    n = CText(f"Part {num}", font_size=30, color=GOLD)
    t = CText(title, font_size=52, color=SOFT_WHITE)
    g = VGroup(n, t).arrange(DOWN, buff=0.35)
    if sub:
        g.add(CText(sub, font_size=28, color=DIMMED))
        g.arrange(DOWN, buff=0.35)
    return g


def tag(text, color=BLUE_3B, size=26):
    """Rounded label like '서술 11 · 3점'. Placed top-left by caller."""
    t = CText(text, font_size=size, color=color)
    box = SurroundingRectangle(t, buff=0.15, corner_radius=0.12, color=color, stroke_width=2)
    return VGroup(box, t)


def banner(text, color=WARN, size=28):
    """Filled warning/answer banner for '많이 틀린 점' or '정답'."""
    t = CText(text, font_size=size, color=WHITE)
    box = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.4, corner_radius=0.15,
                           fill_color=color, fill_opacity=0.85, stroke_width=0)
    t.move_to(box)
    return VGroup(box, t)


def bullet_list(items, size=30, color=SOFT_WHITE, buff=0.32):
    rows = VGroup(*[CText("• " + s, font_size=size, color=color) for s in items])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return rows


def fit(m, w=12.0, h=6.2):
    """Shrink a mobject into the safe area if needed."""
    if m.width > w:
        m.set_width(w)
    if m.height > h:
        m.set_height(h)
    return m


def corner_tag(text, color=BLUE_3B):
    """Section label in the top-left corner. buff 0.7 keeps it inside the validator's safe area."""
    return tag(text, color=color).to_corner(UL, buff=0.7)


def bottom(m):
    """Place a banner at the bottom, still above the burned-in caption zone (y > -2.85)."""
    return m.to_edge(DOWN, buff=1.15)
