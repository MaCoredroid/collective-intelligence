"""The Harness Is Part of the Model: an ~80 s silent explainer.

    manim -qh --frame_rate 30 film.py Film
"""
import subprocess
from pathlib import Path

from manim import *

NARR = Path(__file__).parent / "narration"


def clip_len(key):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(NARR / f"{key}.mp3")],
                         capture_output=True, text=True).stdout.strip()
    return float(out)

config.background_color = "#F4F1EA"

INK = "#1F2328"
INK2 = "#5B6168"
RULE = "#D9D4C7"
CLAY = "#C8643B"
GREY = "#8E959C"
SERIF = "Charter"
MONO = "Menlo"


def serif(t, size=40, color=INK, slant=NORMAL):
    return Text(t, font=SERIF, font_size=size, color=color, slant=slant)


def mono(t, size=20, color=INK2):
    return Text(t, font=MONO, font_size=size, color=color)


class Film(Scene):
    def begin(self, key):
        """Start this scene's narration clip; pad() later holds the scene until the clip has finished."""
        self._t0 = self.renderer.time
        self._need = clip_len(key) + 0.6
        self.add_sound(str(NARR / f"{key}.mp3"))

    def pad(self):
        left = self._need - (self.renderer.time - self._t0)
        if left > 0:
            self.wait(left)

    def construct(self):
        self.wait(0.4)
        self.question()
        self.teammates()
        self.curve()
        self.thinking()
        self.cost()
        self.silent()
        self.close()

    # ------------------------------------------------------------------ 1
    def question(self):
        self.begin("s1")
        root = Dot(ORIGIN, radius=0.13, color=CLAY)
        self.play(FadeIn(root, scale=0.4), run_time=1.0)
        spots = [LEFT * 1.9 + UP * 0.9, RIGHT * 1.9 + UP * 0.9, LEFT * 1.3 + DOWN * 1.2, RIGHT * 1.3 + DOWN * 1.2]
        kids = VGroup(*[Dot(ORIGIN, radius=0.09, color=INK) for _ in spots])
        edges = VGroup(*[Line(ORIGIN, p, stroke_width=1.6, color=INK2) for p in spots])
        peers = VGroup(
            DashedLine(spots[0], spots[2], stroke_width=1.2, color=GREY, dash_length=0.08),
            DashedLine(spots[1], spots[3], stroke_width=1.2, color=GREY, dash_length=0.08),
            DashedLine(spots[2], spots[3], stroke_width=1.2, color=GREY, dash_length=0.08),
        )
        title = serif("Can one model learn to work as a team?", 46, slant=ITALIC).to_edge(UP, buff=0.9)
        sub = mono("collective intelligence · part 1", 20).to_edge(DOWN, buff=0.8)
        self.add(kids)
        self.play(
            LaggedStart(*[k.animate.move_to(p) for k, p in zip(kids, spots)], lag_ratio=0.15),
            LaggedStart(*[Create(e) for e in edges], lag_ratio=0.15),
            run_time=1.6,
        )
        self.play(LaggedStart(*[Create(p) for p in peers], lag_ratio=0.3), FadeIn(title, shift=DOWN * 0.15), run_time=1.6)
        self.play(FadeIn(sub), run_time=0.8)
        self.play(VGroup(root, kids).animate.scale(1.04), rate_func=there_and_back, run_time=1.6)
        self.wait(1.2)
        self.pad()
        self.play(
            *[k.animate.move_to(ORIGIN) for k in kids],
            FadeOut(edges), FadeOut(peers), FadeOut(title), FadeOut(sub),
            run_time=1.2,
        )
        self.remove(kids)
        self.root = root

    # ------------------------------------------------------------------ 2
    def teammates(self):
        self.begin("s2")
        # solo vs my collective harness (v2), mean score per family (0-1); KernelBench is fast_1
        rows = [
            ("Toolathlon", 0.500, 0.500),
            ("EnterpriseOps-Gym", 0.312, 0.312),
            ("FrontierCS · 1 h", 0.215, 0.233),
            ("FrontierCS · 3 h", 0.251, 0.309),
            ("NL2Repo", 0.454, 0.465),
            ("KernelBench", 0.600, 0.600),
        ]
        top = serif("Untrained, a 27B model did no better with teammates.", 38).to_edge(UP, buff=0.6)
        self.play(FadeOut(self.root), FadeIn(top, shift=DOWN * 0.1), run_time=1.0)
        x0, L = -1.9, 8.2          # bar origin and length of a 1.0 score
        y0, dy, bh = 1.75, 0.66, 0.2
        key = VGroup(
            Square(0.2, stroke_width=0, fill_color=INK2, fill_opacity=1), mono("solo", 17, INK2),
            Square(0.2, stroke_width=0, fill_color=CLAY, fill_opacity=1), mono("team (my collective harness)", 17, INK2),
        )
        key[1].next_to(key[0], RIGHT, buff=0.12); key[2].next_to(key[1], RIGHT, buff=0.5); key[3].next_to(key[2], RIGHT, buff=0.12)
        key.move_to([x0 + 2.6, y0 + 0.62, 0])
        self.play(FadeIn(key), run_time=0.5)
        solos, teams, labels, vals = VGroup(), VGroup(), VGroup(), VGroup()
        for k, (name, so, te) in enumerate(rows):
            y = y0 - k * dy
            labels.add(mono(name, 18, INK).move_to([-6.3, y - 0.12, 0], aligned_edge=LEFT))
            b1 = Rectangle(width=so * L, height=bh, stroke_width=0, fill_color=INK2, fill_opacity=1).move_to([x0, y, 0], aligned_edge=LEFT)
            b2 = Rectangle(width=te * L, height=bh, stroke_width=0, fill_color=CLAY, fill_opacity=1).move_to([x0, y - bh - 0.05, 0], aligned_edge=LEFT)
            solos.add(b1); teams.add(b2)
            vals.add(mono(f"{so:.2f}", 15, INK2).next_to(b1, RIGHT, buff=0.12))
            vals.add(mono(f"{te:.2f}", 15, CLAY).next_to(b2, RIGHT, buff=0.12))
        base = Line([x0, y0 + 0.25, 0], [x0, y0 - (len(rows) - 1) * dy - 0.5, 0], color=RULE, stroke_width=1.4)
        self.play(FadeIn(labels, lag_ratio=0.08), Create(base), run_time=0.9)
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in solos], lag_ratio=0.12), run_time=1.4)
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in teams], lag_ratio=0.12), run_time=1.4)
        self.play(FadeIn(vals), run_time=0.6)
        note = mono("built-in subagent and team modes: also within noise · one attempt per task · nothing significant", 15, INK2).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(2.4)
        bottom2 = serif("Collaboration appeared only where work split.\nNew stopping rules changed more than teammates did.", 28).to_edge(DOWN, buff=0.35)
        self.play(FadeOut(note), FadeIn(bottom2, shift=UP * 0.1), run_time=1.0)
        self.wait(2.6)
        self.pad()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)

    # ------------------------------------------------------------------ 3
    def curve(self):
        self.begin("s3")
        ax = Axes(
            x_range=[0, 80, 10], y_range=[0, 16, 4], x_length=9.2, y_length=4.0,
            axis_config={"color": RULE, "stroke_width": 1.4, "include_tip": False},
        ).shift(DOWN * 0.3 + RIGHT * 0.3)
        xl = VGroup(*[mono("base" if s == 0 else str(s), 15, GREY).next_to(ax.c2p(s, 0), DOWN, buff=0.18) for s in range(0, 81, 20)])
        yl = VGroup(*[mono(str(v), 15, GREY).next_to(ax.c2p(0, v), LEFT, buff=0.18) for v in range(0, 17, 4)])
        xt = mono("training step", 15, GREY).next_to(ax, DOWN, buff=0.55)
        pts = [(0, 6.22), (10, 7.42), (20, 8.82), (40, 11.48), (50, 11.85), (70, 12.22)]
        lo = [(0, 4.14), (10, 5.39), (20, 6.43), (40, 8.71), (50, 8.90), (70, 9.14)]
        hi = [(0, 8.66), (10, 9.67), (20, 11.48), (40, 14.77), (50, 15.27), (70, 15.68)]
        band = Polygon(*[ax.c2p(*p) for p in hi], *[ax.c2p(*p) for p in reversed(lo)], stroke_width=0, fill_color=CLAY, fill_opacity=0.12)
        path = VMobject(color=CLAY, stroke_width=4).set_points_as_corners([ax.c2p(*p) for p in pts])
        top = serif("Single-call GRPO on a 9B model", 40).to_edge(UP, buff=0.6)
        self.play(FadeIn(top, shift=DOWN * 0.1), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(xt), run_time=1.2)
        head = Dot(ax.c2p(*pts[0]), radius=0.09, color=CLAY)
        val = DecimalNumber(6.22, num_decimal_places=2, font_size=44, color=CLAY)
        val.add_updater(lambda m: m.next_to(head, UP, buff=0.22))
        unit = mono("FrontierCS, 172 problems, Avg@5", 16, INK2).next_to(top, DOWN, buff=0.25)
        self.play(FadeIn(head), FadeIn(val), FadeIn(unit), run_time=0.6)
        self.play(
            Create(path), FadeIn(band), MoveAlongPath(head, path.copy()),
            ChangeDecimalToValue(val, 12.22), run_time=4.0, rate_func=smooth,
        )
        val.clear_updaters()
        val.set_value(12.22)
        note = mono("+6.00 [4.00, 8.33] vs base, paired · most of it by step 40, then flat", 17, INK2).next_to(xt, DOWN, buff=0.22)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(2.6)
        self.pad()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)

    # ------------------------------------------------------------------ 4
    def thinking(self):
        self.begin("s4")
        top = serif("Same model, problems and judge, trained as an agent.", 36).to_edge(UP, buff=0.7)
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.9)
        x0, full = -5.2, 10.4
        l1 = mono("single call · one problem", 18, INK2).move_to([x0, 1.15, 0], aligned_edge=LEFT)
        b1 = Rectangle(width=full, height=0.42, stroke_width=0, fill_color=CLAY, fill_opacity=1).move_to([x0, 0.55, 0], aligned_edge=LEFT)
        n1 = mono("≈ 30,000 tokens of thinking", 18, INK).next_to(b1, DOWN, buff=0.15).align_to(b1, LEFT)
        l2 = mono("agent harness · per call (median)", 18, INK2).move_to([x0, -0.75, 0], aligned_edge=LEFT)
        b2 = Rectangle(width=max(full * 27 / 30000, 0.02), height=0.42, stroke_width=0, fill_color=INK, fill_opacity=1).move_to([x0, -1.35, 0], aligned_edge=LEFT)
        n2 = mono("27 tokens", 18, INK).next_to(b2, RIGHT, buff=0.2)
        self.play(FadeIn(l1), GrowFromEdge(b1, LEFT), run_time=1.6)
        self.play(FadeIn(n1), run_time=0.5)
        self.play(FadeIn(l2), GrowFromEdge(b2, LEFT), FadeIn(n2), run_time=1.0)
        self.wait(1.4)
        res = serif("No sign of learning by step 10:  −0.02 [−1.01, +0.90]", 30, INK).to_edge(DOWN, buff=0.95)
        res2 = mono("a minimal loop only raised it to 41: mostly the model's own habit", 17, INK2).next_to(res, DOWN, buff=0.18)
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.8)
        self.play(FadeIn(res2), run_time=0.6)
        self.wait(2.6)
        self.pad()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)

    # ------------------------------------------------------------------ 5
    def cost(self):
        self.begin("s5")
        top = serif("Agentic RL used about 8× the GPU-hours per step.", 38).to_edge(UP, buff=0.7)
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.9)
        base = -2.2
        u = 0.42
        c1 = Rectangle(width=1.1, height=1.2 * u, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([-4.6, base, 0], aligned_edge=DOWN)
        c2 = Rectangle(width=1.1, height=9.3 * u, stroke_width=0, fill_color=CLAY, fill_opacity=1).move_to([-2.9, base, 0], aligned_edge=DOWN)
        floor = Line([-5.6, base, 0], [-1.9, base, 0], color=RULE, stroke_width=1.4)
        t1 = mono("single call", 14, INK2).next_to(c1, DOWN, buff=0.15)
        t2 = mono("agentic", 14, INK2).next_to(c2, DOWN, buff=0.15)
        v1 = mono("1.2", 17, INK).next_to(c1, UP, buff=0.12)
        v2 = mono("9.3", 17, INK).next_to(c2, UP, buff=0.12)
        gl = mono("GPU-hours per step", 15, GREY).next_to(floor, DOWN, buff=0.75)
        self.play(Create(floor), GrowFromEdge(c1, DOWN), GrowFromEdge(c2, DOWN), run_time=1.4)
        self.play(FadeIn(VGroup(t1, t2, v1, v2, gl)), run_time=0.6)
        chips = VGroup()
        for name, eff in [
            ("admission control (serving)", "≈ 10× throughput"),
            ("feed the model its own token ids", "2.71× → 1.05× trained tokens"),
            ("speculative decoding", "1.9× agent turns / min"),
        ]:
            box = RoundedRectangle(corner_radius=0.14, width=6.4, height=0.95, stroke_color=RULE, stroke_width=1.6, fill_color="#FBF9F4", fill_opacity=1)
            a = serif(name, 26, INK).move_to(box.get_left() + RIGHT * 0.3, aligned_edge=LEFT).shift(UP * 0.16)
            b = mono(eff, 17, CLAY).move_to(box.get_left() + RIGHT * 0.3, aligned_edge=LEFT).shift(DOWN * 0.2)
            chips.add(VGroup(box, a, b))
        chips.arrange(DOWN, buff=0.28).move_to([2.6, -0.45, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.3) for c in chips], lag_ratio=0.35), run_time=2.2)
        cap = mono("only ~1.4× is extra work; the rest is idle or underfilled GPUs", 18, INK2).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap), run_time=0.7)
        self.wait(2.6)
        self.pad()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)

    # ------------------------------------------------------------------ 6
    def silent(self):
        self.begin("s6")
        top = serif("The dangerous failures were silent.", 40).to_edge(UP, buff=0.8)
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.8)
        judge = RoundedRectangle(corner_radius=0.14, width=2.4, height=1.2, stroke_color=INK, stroke_width=2).move_to(ORIGIN)
        jl = serif("judge", 30).move_to(judge)
        inp = mono("correct solution", 17, INK2).move_to(LEFT * 4.6)
        a1 = Arrow(inp.get_right(), judge.get_left(), buff=0.2, color=INK2, stroke_width=2, tip_length=0.18)
        out = VGroup(mono("Wrong Answer · 0", 17, INK), mono("status: done", 17, INK)).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to(RIGHT * 4.3)
        a2 = Arrow(judge.get_right(), out.get_left(), buff=0.2, color=INK2, stroke_width=2, tip_length=0.18)
        self.play(FadeIn(inp), Create(a1), FadeIn(judge), FadeIn(jl), run_time=1.0)
        self.play(Create(a2), FadeIn(out), run_time=0.9)
        self.wait(0.8)
        canary = Dot(DOWN * 1.9, radius=0.13, color=CLAY)
        cl = mono("canary: a known answer, graded every few minutes", 17, INK2).next_to(canary, DOWN, buff=0.25)
        self.play(FadeIn(canary, scale=0.4), FadeIn(cl), run_time=0.8)
        ring = Circle(radius=0.13, color=CLAY, stroke_width=2).move_to(canary)
        self.play(ring.animate.scale(4).set_stroke(opacity=0), run_time=1.0)
        flag = mono("canary expected 40.0, got 0  →  pause training", 17, CLAY).move_to(DOWN * 0.95)
        self.play(FadeIn(flag, shift=UP * 0.1), out.animate.set_color(GREY), run_time=0.8)
        self.wait(2.0)
        self.pad()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)

    # ------------------------------------------------------------------ 7
    def close(self):
        self.begin("s7")
        title = serif("The harness is part of the model.", 56)
        dot = Dot(radius=0.11, color=CLAY).next_to(title, UP, buff=0.6)
        sub = mono("collective intelligence · part 1 · preliminary results", 18, INK2).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(dot, scale=0.4), run_time=0.7)
        self.play(Write(title), run_time=2.2)
        self.play(FadeIn(sub), run_time=0.8)
        self.wait(3.0)
        self.pad()
        self.play(FadeOut(VGroup(title, sub)), dot.animate.scale(0.6), run_time=1.0)
        self.play(FadeOut(dot), run_time=0.6)
