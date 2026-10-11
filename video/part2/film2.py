"""The Wall, the Compile Tax, and the Oracle: narrated summary of part 2.

    manim -qh --frame_rate 30 film2.py Film2
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


class Film2(Scene):
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
        self.wall()
        self.gain()
        self.tax()
        self.knows()
        self.best()
        self.agent()
        self.oracle()
        self.close()

    # 1 ---------------------------------------------------------------
    def wall(self):
        self.begin("s1")
        eyebrow = mono("collective intelligence · part 2", 18).to_edge(UP, buff=0.5)
        title = serif("The wall", 46).next_to(eyebrow, DOWN, buff=0.25)
        ax = Axes(x_range=[0, 105, 20], y_range=[0, 16, 4], x_length=9.6, y_length=4.0,
                  axis_config={"color": RULE, "stroke_width": 1.4, "include_tip": False}).shift(DOWN * 0.75)
        yl = VGroup(*[mono(str(v), 15, GREY).next_to(ax.c2p(0, v), LEFT, buff=0.15) for v in range(0, 17, 4)])
        xl = VGroup(*[mono("base" if s == 0 else str(s), 15, GREY).next_to(ax.c2p(s, 0), DOWN, buff=0.15) for s in range(0, 101, 20)])
        unit = mono("FrontierCS Avg@5 · training step", 15, GREY).next_to(ax, DOWN, buff=0.55)
        self.play(FadeIn(eyebrow), FadeIn(title, shift=DOWN * 0.1), Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(unit), run_time=1.3)
        plain = [(0, 6.22), (10, 7.42), (20, 8.82), (40, 11.48), (50, 11.85), (70, 12.22)]
        clip = [(40, 11.48), (50, 11.56), (60, 12.62), (70, 12.43)]
        best = [(40, 11.48), (50, 12.73), (70, 12.50), (100, 11.84)]
        mk = lambda pts, col: VMobject(color=col, stroke_width=4).set_points_as_corners([ax.c2p(*p) for p in pts])
        l1, l2, l3 = mk(plain, SLATE), mk(clip, CLAY), mk(best, GREY)
        self.play(Create(l1), run_time=2.2)
        self.play(Create(l2), Create(l3), run_time=1.6)
        band = Rectangle(width=ax.c2p(100, 0)[0] - ax.c2p(50, 0)[0], height=ax.c2p(0, 12.7)[1] - ax.c2p(0, 11.6)[1],
                         stroke_width=0, fill_color=CLAY, fill_opacity=0.14).move_to(ax.c2p(75, 12.15))
        bl = mono("every checkpoint after step 50: 11.6–12.7", 16, INK).next_to(band, UP, buff=0.25)
        self.play(FadeIn(band), FadeIn(bl), run_time=0.9)
        keys = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.4, color=SLATE, stroke_width=4), mono("plain GRPO", 14)).arrange(RIGHT, buff=0.12),
            VGroup(Line(ORIGIN, RIGHT * 0.4, color=CLAY, stroke_width=4), mono("Clip-Cov", 14)).arrange(RIGHT, buff=0.12),
            VGroup(Line(ORIGIN, RIGHT * 0.4, color=GREY, stroke_width=4), mono("reward the best", 14)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.5).next_to(ax, UP, buff=0.15).align_to(ax, LEFT).shift(RIGHT * 0.4)
        self.play(FadeIn(keys), run_time=0.6)
        self.wait(1.0)
        self.pad()
        self.clear_all()

    # 2 ---------------------------------------------------------------
    def gain(self):
        self.begin("s2")
        top = serif("Where the gain came from", 40).to_edge(UP, buff=0.8)
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.7)
        u = 0.9
        base = Rectangle(width=6.22 * u, height=0.8, stroke_width=0, fill_color=GREY, fill_opacity=1)
        val = Rectangle(width=4.9 * u, height=0.8, stroke_width=0, fill_color=SLATE, fill_opacity=1)
        qual = Rectangle(width=1.4 * u, height=0.8, stroke_width=0, fill_color=CLAY, fill_opacity=1)
        row = VGroup(base, val, qual).arrange(RIGHT, buff=0.04).move_to(ORIGIN)
        t0 = mono("base 6.2", 16, INK).next_to(base, DOWN, buff=0.2)
        t1 = mono("+4.9 valid code", 16, SLATE).next_to(val, DOWN, buff=0.2)
        t2 = mono("+1.4 better", 16, CLAY).next_to(qual, DOWN, buff=0.2).shift(RIGHT * 0.35)
        self.play(GrowFromEdge(base, LEFT), FadeIn(t0), run_time=0.8)
        self.play(GrowFromEdge(val, LEFT), FadeIn(t1), run_time=0.9)
        self.play(GrowFromEdge(qual, LEFT), FadeIn(t2), run_time=0.7)
        cap = serif("About 80% of the gain: answers that compile and run.", 30, INK).to_edge(DOWN, buff=1.0)
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.7)
        self.wait(0.6)
        self.pad()
        self.clear_all()

    # 3 ---------------------------------------------------------------
    def tax(self):
        self.begin("s3")
        top = serif("The compile tax", 42).to_edge(UP, buff=0.7)
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.7)
        left = RoundedRectangle(corner_radius=0.14, width=5.6, height=2.4, stroke_color=RULE, stroke_width=1.6, fill_color="#FBF9F4", fill_opacity=1).move_to(LEFT * 3.2 + UP * 0.6)
        right = left.copy().move_to(RIGHT * 3.2 + UP * 0.6)
        lt = serif("safe greedy code", 28).move_to(left.get_top() + DOWN * 0.45)
        rt = serif("search / annealing", 28, CLAY).move_to(right.get_top() + DOWN * 0.45)
        r1 = mono("compile failures: +16 points", 17, INK).move_to(right.get_center() + DOWN * 0.05)
        r2 = mono("when it scores: +4.3 higher", 17, CLAY).move_to(right.get_center() + DOWN * 0.6)
        l1 = mono("compiles more reliably", 17, INK).move_to(left.get_center() + DOWN * 0.05)
        l2 = mono("modest, steady score", 17, INK2).move_to(left.get_center() + DOWN * 0.6)
        self.play(FadeIn(left), FadeIn(lt), FadeIn(right), FadeIn(rt), run_time=0.9)
        self.play(FadeIn(l1), FadeIn(r1), run_time=0.7)
        self.play(FadeIn(l2), FadeIn(r2), run_time=0.7)
        # share of search code shrinking
        lab = mono("share of search-style programs in training", 16, INK2).move_to(DOWN * 1.65)
        full = 8.0
        b0 = Rectangle(width=full * 0.19, height=0.32, stroke_width=0, fill_color=CLAY, fill_opacity=1).move_to([-4.0, -2.3, 0], aligned_edge=LEFT)
        v0 = mono("19% → 4–9%", 18, INK).next_to(b0, RIGHT, buff=0.25)
        self.play(FadeIn(lab), GrowFromEdge(b0, LEFT), FadeIn(v0), run_time=0.8)
        self.play(b0.animate.stretch_to_fit_width(full * 0.065, about_edge=LEFT), v0.animate.next_to(b0.copy().stretch_to_fit_width(full * 0.065, about_edge=LEFT), RIGHT, buff=0.25), run_time=1.4)
        self.wait(0.6)
        self.pad()
        self.clear_all()

    # 4 ---------------------------------------------------------------
    def knows(self):
        self.begin("s4")
        top = serif("It knows better than it ships", 40).to_edge(UP, buff=0.7)
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.7)
        q1 = serif("“simple is better”", 32, INK2, slant=ITALIC).move_to(LEFT * 3.0 + UP * 1.2)
        q2 = serif("“It's safer for TLE.”", 32, INK2, slant=ITALIC).move_to(RIGHT * 3.0 + UP * 1.2)
        self.play(FadeIn(q1, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(q2, shift=UP * 0.1), run_time=0.6)
        rows = [("one sample (Avg@5)", 12, SLATE), ("best of 5", 20, SLATE), ("best of 55, pooled checkpoints", 29, CLAY)]
        u = 0.25
        bars = VGroup()
        for i, (name, v, col) in enumerate(rows):
            y = -0.4 - i * 0.75
            lab = mono(name, 17, INK2).move_to([-2.2, y, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=v * u, height=0.38, stroke_width=0, fill_color=col, fill_opacity=1).move_to([-1.9, y, 0], aligned_edge=LEFT)
            val = mono(str(v), 18, INK).next_to(bar, RIGHT, buff=0.18)
            bars.add(VGroup(lab, bar, val))
        for g in bars:
            self.play(FadeIn(g[0]), GrowFromEdge(g[1], LEFT), FadeIn(g[2]), run_time=0.6)
        self.wait(0.5)
        self.pad()
        self.clear_all()

    # 5 ---------------------------------------------------------------
    def best(self):
        self.begin("s5")
        top = serif("Rewarding the best answer", 40).to_edge(UP, buff=0.7)
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.7)
        ax = Axes(x_range=[40, 105, 20], y_range=[0, 24, 8], x_length=7.6, y_length=3.6,
                  axis_config={"color": RULE, "stroke_width": 1.4, "include_tip": False}).shift(DOWN * 0.5 + LEFT * 1.6)
        xl = VGroup(*[mono(str(s), 15, GREY).next_to(ax.c2p(s, 0), DOWN, buff=0.15) for s in (40, 60, 80, 100)])
        yl = VGroup(*[mono(str(v), 15, GREY).next_to(ax.c2p(40, v), LEFT, buff=0.15) for v in (0, 8, 16, 24)])
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.8)
        b5 = VMobject(color=CLAY, stroke_width=4).set_points_as_corners([ax.c2p(*p) for p in [(40, 20.88), (50, 20.82), (70, 20.01), (100, 19.80)]])
        av = VMobject(color=SLATE, stroke_width=4).set_points_as_corners([ax.c2p(*p) for p in [(40, 11.48), (50, 12.73), (70, 12.50), (100, 11.84)]])
        t1 = mono("best of 5", 16, CLAY).next_to(ax.c2p(100, 19.8), RIGHT, buff=0.15)
        t2 = mono("average · no gain", 16, SLATE).next_to(ax.c2p(100, 11.84), RIGHT, buff=0.15)
        self.play(Create(b5), Create(av), run_time=1.6)
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.6)
        cap = serif("In theory, with deterministic scores, collapse is the optimum.", 28).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.7)
        self.wait(0.6)
        self.pad()
        self.clear_all()

    # 6 ---------------------------------------------------------------
    def agent(self):
        self.begin("s6")
        top = serif("In agent mode, RL added submissions, not testing", 36).to_edge(UP, buff=0.7)
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.7)
        lab1 = mono("judged submissions per trial (median), base → step 20", 17, INK2).move_to(UP * 1.1)
        n = DecimalNumber(38, num_decimal_places=0, font_size=72, color=CLAY).move_to(UP * 0.1)
        self.play(FadeIn(lab1), FadeIn(n), run_time=0.6)
        self.play(ChangeDecimalToValue(n, 50), run_time=1.2)
        n.set_value(50)
        note = mono("all of the extra ones after the last improvement", 17, INK).next_to(n, DOWN, buff=0.3)
        lab2 = mono("submissions run locally first: 14.6% → 14.8%", 18, INK2).next_to(note, DOWN, buff=0.6)
        self.play(FadeIn(note), run_time=0.6)
        self.play(FadeIn(lab2), run_time=0.6)
        self.wait(0.6)
        self.pad()
        self.clear_all()

    # 7 ---------------------------------------------------------------
    def oracle(self):
        self.begin("s7")
        top = serif("Now running: a scarce oracle", 40).to_edge(UP, buff=0.7)
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.7)
        dots = VGroup(*[Circle(radius=0.18, stroke_color=CLAY, stroke_width=2.5) for _ in range(10)]).arrange(RIGHT, buff=0.22).move_to(UP * 0.7)
        dl = mono("10 judged submissions per trial", 17, INK2).next_to(dots, UP, buff=0.3)
        self.play(FadeIn(dl), LaggedStart(*[Create(d) for d in dots], lag_ratio=0.08), run_time=1.2)
        self.play(LaggedStart(*[d.animate.set_fill(CLAY, opacity=1) for d in dots[:3]], lag_ratio=0.3), run_time=0.9)
        fb = VGroup(mono("feedback:", 18, INK2), mono("score in [70, 80)", 20, INK)).arrange(RIGHT, buff=0.25).move_to(DOWN * 0.7)
        fb2 = mono("never the exact score", 16, GREY).next_to(fb, DOWN, buff=0.2)
        self.play(FadeIn(fb), FadeIn(fb2), run_time=0.7)
        q = serif("Will the search move inside the model?", 32, INK, slant=ITALIC).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.8)
        self.wait(0.5)
        self.pad()
        self.clear_all()

    # 8 ---------------------------------------------------------------
    def close(self):
        self.begin("s8")
        title = serif("RL learns what you pay for.", 56)
        dot = Dot(radius=0.11, color=CLAY).next_to(title, UP, buff=0.6)
        sub = mono("collective intelligence · part 2 · the wall, the compile tax, and the oracle", 16, INK2).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(dot, scale=0.4), run_time=0.6)
        self.play(Write(title), run_time=1.8)
        self.play(FadeIn(sub), run_time=0.7)
        self.wait(1.5)
        self.pad()
        self.play(FadeOut(VGroup(title, sub)), dot.animate.scale(0.6), run_time=1.0)
        self.play(FadeOut(dot), run_time=0.6)
