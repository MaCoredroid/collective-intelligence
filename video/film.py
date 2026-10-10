"""The Harness Is Part of the Model: an ~80 s silent explainer.

    manim -qh --frame_rate 30 film.py Film
"""
from manim import *

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
    def construct(self):
        self.question()
        self.teammates()
        self.curve()
        self.thinking()
        self.cost()
        self.silent()
        self.close()

    # ------------------------------------------------------------------ 1
    def question(self):
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
        self.play(
            *[k.animate.move_to(ORIGIN) for k in kids],
            FadeOut(edges), FadeOut(peers), FadeOut(title), FadeOut(sub),
            run_time=1.2,
        )
        self.remove(kids)
        self.root = root

    # ------------------------------------------------------------------ 2
    def teammates(self):
        # score minus solo, per family; arms: subagents, team, collective v1, v1+submit, collective v2
        rows = [
            ("Toolathlon", [0.0, 0.125, 0.25, 0.125, 0.0]),
            ("EnterpriseOps-Gym", [0.188, 0.188, 0.188, 0.126, 0.0]),
            ("FrontierCS · 1 h", [0.047, -0.026, -0.023, 0.023, 0.018]),
            ("FrontierCS · 3 h", [None, -0.026, None, -0.013, 0.058]),
            ("NL2Repo", [-0.019, -0.031, None, 0.010, 0.011]),
            ("KernelBench", [-0.3, 0.1, None, None, 0.0]),
        ]
        cx, scale = 1.4, 9.0
        X = lambda d: cx + d * scale
        ys = [1.55 - i * 0.62 for i in range(len(rows))]
        top = serif("Untrained, a 27B model did no better with teammates.", 38).to_edge(UP, buff=0.7)
        line = Line([cx, 1.95, 0], [cx, -1.95, 0], color=CLAY, stroke_width=3)
        solo = mono("solo", 18, CLAY).next_to(line, UP, buff=0.12)
        self.play(self.root.animate.move_to([cx, 1.95, 0]), FadeIn(top, shift=DOWN * 0.1), run_time=1.0)
        self.play(Create(line), FadeIn(solo), FadeOut(self.root), run_time=0.9)
        labels = VGroup(*[mono(n, 18, INK2).move_to([-4.6, y, 0], aligned_edge=LEFT) for (n, _), y in zip(rows, ys)])
        for lab in labels:
            lab.align_to([-6.3, 0, 0], LEFT)
        ticks = VGroup()
        for d in (-0.3, -0.15, 0.0, 0.15, 0.3):
            ticks.add(Line([X(d), -2.05, 0], [X(d), -2.15, 0], color=GREY, stroke_width=1.2))
            ticks.add(mono(f"{d:+.2f}" if d else "0", 15, GREY).move_to([X(d), -2.4, 0]))
        axis_lab = mono("score − solo score", 16, GREY).move_to([cx, -2.8, 0])
        axis = Line([X(-0.33), -2.05, 0], [X(0.33), -2.05, 0], color=RULE, stroke_width=1.2)
        self.play(FadeIn(labels, lag_ratio=0.1), Create(axis), FadeIn(ticks), FadeIn(axis_lab), run_time=1.2)
        dots, targets = VGroup(), []
        for (name, ds), y in zip(rows, ys):
            for k, d in enumerate(ds):
                if d is None:
                    continue
                dot = Dot([cx, y, 0], radius=0.075, color=INK2 if k < 4 else CLAY)
                if k == 4:
                    dot.set_fill(opacity=0).set_stroke(CLAY, width=2.5)
                dots.add(dot)
                targets.append([X(d), y + (k - 2) * 0.045, 0])
        self.add(dots)
        self.play(LaggedStart(*[d.animate.move_to(t) for d, t in zip(dots, targets)], lag_ratio=0.04), run_time=2.2)
        key = VGroup(
            Dot(radius=0.06, color=INK2), mono("subagents · team · collective v1 / v1+submit", 15, INK2),
            Circle(radius=0.06, color=CLAY, stroke_width=2.5), mono("collective v2", 15, INK2),
        ).arrange(RIGHT, buff=0.18).to_edge(DOWN, buff=0.35)
        note = mono("up to 96 tasks · one attempt each · no difference is statistically significant", 16, INK2).next_to(key, UP, buff=0.18)
        self.play(FadeIn(key), FadeIn(note), run_time=0.8)
        self.wait(2.2)
        top2 = serif("Collaboration appeared only where work split.\nNew stopping rules changed more than teammates did.", 34).to_edge(UP, buff=0.55)
        self.play(FadeTransform(top, top2), run_time=1.0)
        self.wait(2.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)

    # ------------------------------------------------------------------ 3
    def curve(self):
        ax = Axes(
            x_range=[0, 80, 10], y_range=[0, 16, 4], x_length=9.2, y_length=4.4,
            axis_config={"color": RULE, "stroke_width": 1.4, "include_tip": False},
        ).shift(DOWN * 0.55 + RIGHT * 0.3)
        xl = VGroup(*[mono("base" if s == 0 else str(s), 15, GREY).next_to(ax.c2p(s, 0), DOWN, buff=0.18) for s in range(0, 81, 20)])
        yl = VGroup(*[mono(str(v), 15, GREY).next_to(ax.c2p(0, v), LEFT, buff=0.18) for v in range(0, 17, 4)])
        xt = mono("training step", 15, GREY).next_to(ax, DOWN, buff=0.6)
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
        note = mono("+6.00 [4.00, 8.33] vs base, paired · most of it by step 40, then flat", 17, INK2).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(2.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)

    # ------------------------------------------------------------------ 4
    def thinking(self):
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
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)

    # ------------------------------------------------------------------ 5
    def cost(self):
        top = serif("Agentic RL used about 8× the GPU-hours per step.", 38).to_edge(UP, buff=0.7)
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.9)
        base = -2.2
        u = 0.42
        c1 = Rectangle(width=1.1, height=1.2 * u, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([-4.6, base, 0], aligned_edge=DOWN)
        c2 = Rectangle(width=1.1, height=9.3 * u, stroke_width=0, fill_color=CLAY, fill_opacity=1).move_to([-2.9, base, 0], aligned_edge=DOWN)
        floor = Line([-5.6, base, 0], [-1.9, base, 0], color=RULE, stroke_width=1.4)
        t1 = mono("single\ncall", 15, INK2).next_to(c1, DOWN, buff=0.15)
        t2 = mono("agentic", 15, INK2).next_to(c2, DOWN, buff=0.15)
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
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)

    # ------------------------------------------------------------------ 6
    def silent(self):
        top = serif("The dangerous failures were silent.", 40).to_edge(UP, buff=0.8)
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.8)
        judge = RoundedRectangle(corner_radius=0.14, width=2.4, height=1.2, stroke_color=INK, stroke_width=2).move_to(ORIGIN)
        jl = serif("judge", 30).move_to(judge)
        inp = mono("correct\nsolution", 17, INK2).move_to(LEFT * 4.2)
        a1 = Arrow(inp.get_right(), judge.get_left(), buff=0.2, color=INK2, stroke_width=2, tip_length=0.18)
        out = mono("Wrong Answer · 0\nstatus: done", 17, INK).move_to(RIGHT * 4.2)
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
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)

    # ------------------------------------------------------------------ 7
    def close(self):
        title = serif("The harness is part of the model.", 56)
        dot = Dot(radius=0.11, color=CLAY).next_to(title, UP, buff=0.6)
        sub = mono("collective intelligence · part 1 · preliminary results", 18, INK2).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(dot, scale=0.4), run_time=0.7)
        self.play(Write(title), run_time=2.2)
        self.play(FadeIn(sub), run_time=0.8)
        self.wait(3.0)
        self.play(FadeOut(VGroup(title, sub)), dot.animate.scale(0.6), run_time=1.0)
        self.play(FadeOut(dot), run_time=0.6)
