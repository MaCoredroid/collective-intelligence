"""Knowing Simulated Annealing Isn't Running It: narrated summary of part 3.

    manim -qh --frame_rate 30 --disable_caching film3.py Film3
"""
import subprocess
from pathlib import Path

from manim import *

NARR = Path(__file__).parent / "narration"
config.background_color = "#F4F1EA"

INK = "#1F2328"
INK2 = "#5B6168"
RULE = "#D9D4C7"
CLAY = "#C8643B"
SLATE = "#3B6E9E"
GREY = "#8E959C"
CARD = "#FBF9F4"
SERIF = "Charter"
MONO = "Menlo"


def clip_len(key):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(NARR / f"{key}.mp3")],
                         capture_output=True, text=True).stdout.strip()
    return float(out)


def serif(t, size=40, color=INK, slant=NORMAL):
    return Text(t, font=SERIF, font_size=size, color=color, slant=slant)


def mono(t, size=20, color=INK2):
    return Text(t, font=MONO, font_size=size, color=color)


def card(w, h):
    return RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=RULE, stroke_width=1.6, fill_color=CARD, fill_opacity=1)


class Film3(Scene):
    def begin(self, key):
        self._t0 = self.renderer.time
        self._need = clip_len(key) + 0.7
        self.add_sound(str(NARR / f"{key}.mp3"))

    def pad(self):
        left = self._need - (self.renderer.time - self._t0)
        if left > 0:
            self.wait(left)

    def clear_all(self, rt=0.8):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=rt)

    def construct(self):
        self.wait(0.3)
        self.hook()
        self.ruler()
        self.skill()
        self.levers()
        self.oracle()
        self.sibling()
        self.next_steps()
        self.close()

    # 1 ---------------------------------------------------------------
    def hook(self):
        self.begin("s1")
        eyebrow = mono("collective intelligence · part 3", 18).to_edge(UP, buff=0.5)
        title = serif("Knowing isn't running", 46).next_to(eyebrow, DOWN, buff=0.25)
        self.play(FadeIn(eyebrow), FadeIn(title, shift=DOWN * 0.1), run_time=1.0)
        left = card(5.6, 2.6).move_to(LEFT * 3.2 + DOWN * 0.6)
        right = card(5.6, 2.6).move_to(RIGHT * 3.2 + DOWN * 0.6)
        lt = mono("what it plans", 16, GREY).next_to(left, UP, buff=0.15)
        rt = mono("what it ships", 16, GREY).next_to(right, UP, buff=0.15)
        plan = VGroup(
            serif("“use simulated annealing,", 24, INK2, slant=ITALIC),
            serif("bounded by a timer, keep", 24, INK2, slant=ITALIC),
            serif("the best layout so far”", 24, INK2, slant=ITALIC),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(left)
        code = VGroup(
            mono("sort(items, by_value);", 18, INK),
            mono("for (item : items)", 18, INK),
            mono("    place_greedily(item);", 18, INK),
            mono("print(layout);", 18, INK),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(right)
        self.play(FadeIn(left), FadeIn(lt), FadeIn(plan, shift=UP * 0.1), run_time=1.0)
        arrow = Arrow(left.get_right(), right.get_left(), buff=0.12, color=CLAY, stroke_width=3, tip_length=0.2)
        self.play(GrowArrow(arrow), run_time=0.6)
        self.play(FadeIn(right), FadeIn(rt), FadeIn(code, shift=UP * 0.1), run_time=1.0)
        self.wait(0.8)
        self.pad()
        self.clear_all()

    # 2 ---------------------------------------------------------------
    def ruler(self):
        self.begin("s2")
        top = serif("A better ruler", 42).to_edge(UP, buff=0.8)
        sub = mono("credit only the points above the best trivial program", 17, INK2).next_to(top, DOWN, buff=0.25)
        self.play(FadeIn(top, shift=DOWN * 0.1), FadeIn(sub), run_time=0.9)
        W = 11.0
        g = Rectangle(width=W * 0.98, height=0.9, stroke_width=0, fill_color=GREY, fill_opacity=1)
        a = Rectangle(width=W * 0.02, height=0.9, stroke_width=0, fill_color=CLAY, fill_opacity=1)
        bar = VGroup(g, a).arrange(RIGHT, buff=0.03).move_to(DOWN * 0.2)
        gl = mono("points at or below the trivial bar · ~98%", 18, INK).next_to(g, DOWN, buff=0.25).align_to(g, LEFT)
        al = mono("above it · ~2%", 18, CLAY).next_to(a, UP, buff=0.25).align_to(a, RIGHT)
        self.play(GrowFromEdge(g, LEFT), run_time=1.4)
        self.play(FadeIn(gl), run_time=0.5)
        self.play(GrowFromEdge(a, LEFT), FadeIn(al), run_time=0.7)
        cap = serif("Every gain since step 40 sat in the grey part.", 30).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.7)
        self.wait(0.6)
        self.pad()
        self.clear_all()

    # 3 ---------------------------------------------------------------
    def skill(self):
        self.begin("s3")
        top = serif("The missing skill", 42).to_edge(UP, buff=0.8)
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.7)
        items = [("a clock", "stop before the time limit"), ("a cheap delta", "score a small change fast"), ("a memory", "keep the best answer so far")]
        cards = VGroup()
        for name, desc in items:
            c = card(3.7, 1.7)
            t1 = serif(name, 30, INK).move_to(c.get_center() + UP * 0.25)
            t2 = mono(desc, 14, INK2).move_to(c.get_center() + DOWN * 0.35)
            cards.add(VGroup(c, t1, t2))
        cards.arrange(RIGHT, buff=0.35).move_to(UP * 0.4)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.35), run_time=1.6)
        lab = mono("working searches, started from its own archived programs", 17, INK2).move_to(DOWN * 1.45)
        n = serif("0 / 127", 64, CLAY).move_to(DOWN * 2.3)
        n2 = mono("from scratch: 0 / 128", 16, GREY).next_to(n, DOWN, buff=0.15)
        self.play(FadeIn(lab), run_time=0.6)
        self.play(FadeIn(n, scale=0.8), run_time=0.9)
        self.play(FadeIn(n2), run_time=0.5)
        self.wait(0.6)
        self.pad()
        self.clear_all()

    # 4 ---------------------------------------------------------------
    def levers(self):
        self.begin("s4")
        top = serif("Eight teacher-free levers", 40).to_edge(UP, buff=0.6)
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.7)
        names = ["rank reward per test", "fixed quality bars", "scarce oracle", "plan first",
                 "search kit", "kit bonus", "self-distillation", "expert iteration"]
        hdr = VGroup(mono("habit changed", 16, SLATE), mono("algorithm changed", 16, CLAY)).arrange(RIGHT, buff=0.9)
        rows = VGroup()
        for nm in names:
            rows.add(mono(nm, 19, INK))
        rows.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(LEFT * 2.6 + DOWN * 0.45)
        hdr.next_to(rows, RIGHT, buff=1.6).align_to(rows, UP).shift(UP * 0.55)
        self.play(FadeIn(hdr), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.12), run_time=1.8)
        habit = [False, False, True, True, True, False, True, False]
        marks = VGroup()
        for r, h in zip(rows, habit):
            hm = mono("yes" if h else "·", 19, SLATE if h else GREY).move_to([hdr[0].get_center()[0], r.get_center()[1], 0])
            am = mono("no", 19, CLAY).move_to([hdr[1].get_center()[0], r.get_center()[1], 0])
            marks.add(hm, am)
        self.play(LaggedStart(*[FadeIn(m) for m in marks[0::2]], lag_ratio=0.1), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(m) for m in marks[1::2]], lag_ratio=0.1), run_time=1.4)
        self.wait(0.6)
        self.pad()
        self.clear_all()

    # 5 ---------------------------------------------------------------
    def oracle(self):
        self.begin("s5")
        top = serif("Scarce oracle: habits moved", 40).to_edge(UP, buff=0.8)
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.7)
        u = 0.1
        x0 = -3.6
        rows = [("run locally before submitting · unlimited judge", 16.5, GREY, "~15%"),
                ("run locally before submitting · 10 submissions, untrained", 56, SLATE, "56%"),
                ("run locally before submitting · 10 submissions, trained", 70, SLATE, "65–72%"),
                ("search-style code · steps 1–18", 11, CLAY, "3–19%, no trend")]
        grp = VGroup()
        for i, (lab, v, col, txt) in enumerate(rows):
            y = 1.25 - i * 1.05
            l = mono(lab, 16, INK2).move_to([x0, y + 0.38, 0], aligned_edge=LEFT)
            b = Rectangle(width=v * u, height=0.36, stroke_width=0, fill_color=col, fill_opacity=1).move_to([x0, y - 0.05, 0], aligned_edge=LEFT)
            t = mono(txt, 17, INK).next_to(b, RIGHT, buff=0.2)
            grp.add(VGroup(l, b, t))
        for g in grp:
            self.play(FadeIn(g[0]), GrowFromEdge(g[1], LEFT), FadeIn(g[2]), run_time=0.8)
        cap = serif("The code it tested stayed greedy.", 30).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.7)
        self.wait(0.6)
        self.pad()
        self.clear_all()

    # 6 ---------------------------------------------------------------
    def sibling(self):
        self.begin("s6")
        top = serif("The skill is one size up", 42).to_edge(UP, buff=0.8)
        sub = mono("attempts with a working search · held-out problems", 17, INK2).next_to(top, DOWN, buff=0.25)
        self.play(FadeIn(top, shift=DOWN * 0.1), FadeIn(sub), run_time=0.8)
        u = 0.07
        x0 = -2.4
        data = [("9B", 3.7, 3.1, SLATE), ("27B", 75.5, 89.8, CLAY)]
        grp = VGroup()
        for i, (nm, a, b, col) in enumerate(data):
            y = 0.35 - i * 1.6
            lab = serif(nm, 34, INK).move_to([x0 - 1.3, y - 0.25, 0])
            b1 = Rectangle(width=max(a * u, 0.06), height=0.34, stroke_width=0, fill_color=col, fill_opacity=1).move_to([x0, y, 0], aligned_edge=LEFT)
            b2 = Rectangle(width=max(b * u, 0.06), height=0.34, stroke_width=0, fill_color=col, fill_opacity=0.75).move_to([x0, y - 0.5, 0], aligned_edge=LEFT)
            t1 = mono(f"{a:g}% · set A", 16, INK).next_to(b1, RIGHT, buff=0.2)
            t2 = mono(f"{b:g}% · set B", 16, INK).next_to(b2, RIGHT, buff=0.2)
            grp.add(VGroup(lab, b1, b2, t1, t2))
        for g in grp:
            self.play(FadeIn(g[0]), GrowFromEdge(g[1], LEFT), GrowFromEdge(g[2], LEFT), FadeIn(g[3]), FadeIn(g[4]), run_time=1.0)
        note = mono("both untrained · same model family", 16, GREY).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(0.6)
        self.pad()
        self.clear_all()

    # 7 ---------------------------------------------------------------
    def next_steps(self):
        self.begin("s7")
        top = serif("Next", 42).to_edge(UP, buff=0.8)
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.6)
        steps = [("1", "learn from a teacher", "on-policy distillation from the 27B · running"),
                 ("2", "learn from human code", "permissively licensed search programs"),
                 ("3", "then teams", "a skill worth dividing up")]
        rows = VGroup()
        for num, a, b in steps:
            dot = Circle(radius=0.28, stroke_color=CLAY, stroke_width=2.5)
            n = mono(num, 20, CLAY).move_to(dot)
            t = VGroup(serif(a, 30, INK), mono(b, 15, INK2)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            rows.add(VGroup(VGroup(dot, n), t).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.4), run_time=2.2)
        self.wait(0.6)
        self.pad()
        self.clear_all()

    # 8 ---------------------------------------------------------------
    def close(self):
        self.begin("s8")
        title = serif("Knowing the algorithm isn't running it.", 50)
        dot = Dot(radius=0.11, color=CLAY).next_to(title, UP, buff=0.6)
        sub = mono("collective intelligence · part 3", 17, INK2).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(dot, scale=0.4), run_time=0.6)
        self.play(Write(title), run_time=1.8)
        self.play(FadeIn(sub), run_time=0.7)
        self.wait(1.5)
        self.pad()
        self.play(FadeOut(VGroup(title, sub)), dot.animate.scale(0.6), run_time=1.0)
        self.play(FadeOut(dot), run_time=0.6)
