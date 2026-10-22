"""Phyllotaxis Calculator -- a real window, not a web page.

Vogel's model, the way the HTML widget had it, rebuilt as a desktop app
so the spiral and its controls share one screen: no scrolling, and the
picture redraws the same frame the value changes. The bars are keyboard
bars first (that is the point of the exercise):

    Up / Down     choose the bar
    Left / Right  move it (Shift = x10 step) -- key repeat works
    G             snap to golden (137.507764...)
    L             snap to Lucas (99.501553...)
    P             cycle the presets
    T             cycle the traced arm (off, 13, 18, 21, 29, 34, ...)
    N             toggle seed numbers
    D             21-dot mode (your hand-draw check)
    Space         sweep 99.4 <-> 144 and back
    Esc           quit

The mouse still works: click a bar to choose it, drag to slide it,
click a preset to jump.

State persists to state.json next to this file, like the widget's did.
"""

import json
import math
import textwrap
from pathlib import Path

import pyglet
from pyglet import shapes
from pyglet.window import key

GOLD = 137.50776405003785
LUCAS = 99.50155281000757
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
LUC = [2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199]
STEPS = [0, 13, 18, 21, 29, 34, 47, 55, 76, 89]
PRESETS = [(90, "90 - 4 spokes"), (LUCAS, "99.502 - LUCAS"), (120, "120 - 3 spokes"),
           (135, "135 - 8 spokes"), (137.3, "137.3 - near miss"), (GOLD, "137.508 - GOLDEN"),
           (137.92, "137.92 - near miss"), (144, "144 - 5 spokes"), (180, "180 - 2 spokes")]

HERE = Path(__file__).resolve().parent
STATE_FILE = HERE / "state.json"

INK = (242, 234, 217)        # the widget's warm paper text
MUTED = (168, 154, 128)
PINK = (255, 64, 140)
HOT = (255, 105, 205)
PANEL = (24, 18, 12)
TRACK = (58, 48, 34)
DISC = (36, 23, 8)


def best_frac(x):
    """Closest p/q to x with q <= 89 -- the widget's spoke detector."""
    bp, bq, be = 0, 1, 9.0
    for q in range(1, 90):
        p = round(x * q)
        e = abs(x - p / q)
        if e < be:
            be, bp, bq = e, p, q
    return bp, bq, be


def diagnose(angle):
    """The widget's six verdicts, verbatim logic."""
    p, q, e = best_frac(angle / 360.0)
    d_g, d_l = abs(angle - GOLD), abs(angle - LUCAS)
    if d_g < 0.01:
        return ("FIBONACCI / GOLDEN. The most irrational angle there is -- no seed ever "
                "lines up behind another, no spokes, no wasted gap. Count arms both "
                "ways: consecutive Fibonacci numbers.")
    if d_l < 0.01:
        return ("LUCAS. Same phi, different starting seeds. Packing is still even, "
                "but the arm counts are Lucas numbers -- trace 29 or 47. This is the "
                "rare sunflower from your notes, not a broken Fibonacci one.")
    if e < 0.0004:
        return (f"RATIONAL -- SPOKES. This angle is (almost) {p}/{q} of a turn, so "
                f"every {q}th seed lands on the same ray. You get {q} straight spokes "
                "and big empty wedges between them. Pretty, terrible packing.")
    if d_g < 0.35:
        return (f"NEAR MISS -- IN BETWEEN. Only {angle - GOLD:+.3f} deg off golden, and "
                "it already breaks: arms bend, a dislocation seam appears, gaps open. "
                "This is why 137.3 and 137.9 pictures never look like a real sunflower.")
    if d_l < 0.5:
        return ("NEAR LUCAS. Close to the Lucas angle but off it -- arms warp toward "
                "spokes. Nudge in small steps and watch it lock in at 99.501553.")
    return ("IN BETWEEN. Neither golden nor Lucas nor a clean fraction -- curved, "
            "broken arms and uneven clumping. Move slowly: patterns flip between "
            "spoke-like and spiral-like as you pass each simple fraction.")


class Bar:
    """One keyboard-first slider."""

    def __init__(self, name, vmin, vmax, step, fmt, get, set_):
        self.name, self.vmin, self.vmax, self.step, self.fmt = name, vmin, vmax, step, fmt
        self.get, self.set = get, set_
        self.rect = None       # (x, y, w) of the track, for the mouse

    def adjust(self, direction, mult=1):
        self.set(min(self.vmax, max(self.vmin, self.get() + direction * self.step * mult)))

    def set_fraction(self, frac):
        self.set(self.vmin + frac * (self.vmax - self.vmin))


class Phyllotaxis(pyglet.window.Window):
    def __init__(self):
        super().__init__(fullscreen=True, caption="Phyllotaxis Calculator")
        self.S = {"angle": GOLD, "seeds": 400, "dot": 1.0, "step": 34, "nums": False}
        try:
            saved = json.loads(STATE_FILE.read_text())
            self.S.update({k: saved[k] for k in self.S if k in saved})
        except (OSError, ValueError):
            pass
        self.sweeping = False
        self.sweep_dir = 1
        self.focus = 1         # the zoom bar: where the interesting stuff lives
        self.dirty = True

        self.batch = pyglet.graphics.Batch()
        self.panel_batch = pyglet.graphics.Batch()
        self.disc = shapes.Circle(0, 0, 10, color=DISC, batch=self.batch)
        self.arm_segs = []
        self.dots = []
        self.num_labels = []
        self._build_panel()
        self.bars = [
            Bar("ANGLE -- FULL TURN", 0.0, 360.0, 0.05, "{:.4f} deg",
                lambda: self.S["angle"], self._set_angle),
            Bar("ANGLE -- ZOOMED 90-150", 90.0, 150.0, 0.001, "{:.6f} deg",
                lambda: self.S["angle"], self._set_angle),
            Bar("SEEDS", 21, 1000, 1, "{:.0f}",
                lambda: float(self.S["seeds"]),
                lambda v: self._set("seeds", int(round(v)))),
            Bar("DOT SIZE", 0.5, 1.7, 0.05, "{:.2f}",
                lambda: self.S["dot"], lambda v: self._set("dot", v)),
        ]
        pyglet.clock.schedule_interval(self._tick, 1 / 30.0)

    # ---- state ------------------------------------------------------------

    def _set(self, k, v):
        self.S[k] = v
        self.dirty = True
        self._persist()

    def _set_angle(self, v):
        self.S["angle"] = v % 360.0
        self.dirty = True
        self._persist()

    def _persist(self):
        try:
            STATE_FILE.write_text(json.dumps(self.S))
        except OSError:
            pass

    def _stop_sweep(self):
        self.sweeping = False

    # ---- panel ------------------------------------------------------------

    def _label(self, x, y, text, size=13, color=INK, bold=False, anchor_x="left"):
        lab = pyglet.text.Label(text, x=x, y=y, font_size=size,
                                color=color + (255,), anchor_x=anchor_x,
                                anchor_y="baseline", batch=self.panel_batch)
        lab.bold = bold      # pyglet 2.1 wants this as an attribute, not a kwarg
        return lab

    def _build_panel(self):
        w, h = self.width, self.height
        self.px = w - 512                       # panel left edge
        self.big = self._label(self.px, h - 58, "", size=30, bold=True)
        self.frac1 = self._label(self.px, h - 84, "", size=12, color=MUTED)
        self.frac2 = self._label(self.px, h - 102, "", size=12, color=MUTED)
        self.diag = [self._label(self.px, h - 132 - 17 * i, "", size=12.5)
                     for i in range(5)]
        self.chips_fib = self._chip_row(h - 252, "FIBONACCI  ", FIB)
        self.chips_luc = self._chip_row(h - 278, "LUCAS  ", LUC)
        self._label(self.px, h - 306,
                    "r = c*sqrt(n)    theta = n * angle    phi = 1.6180339887...",
                    size=11.5, color=MUTED)
        self._label(self.px, h - 324,
                    "Golden = 360/phi^2    Lucas = 360/(phi+2)", size=11.5, color=MUTED)
        self.bar_labels = []
        self.bar_tracks = []
        self.bar_fills = []
        self.bar_values = []
        for i in range(4):
            y = h - 386 - i * 62
            self.bar_labels.append(self._label(self.px, y, "", size=12, bold=True))
            self.bar_tracks.append(shapes.Rectangle(
                self.px, y - 26, 472, 10, color=TRACK, batch=self.panel_batch))
            self.bar_fills.append(shapes.Rectangle(
                self.px, y - 26, 10, 10, color=PINK, batch=self.panel_batch))
            self.bar_values.append(self._label(self.px + 472, y, "", size=13,
                                               bold=True, anchor_x="right"))
        self.preset_title_y = h - 386 - 4 * 62 - 8
        self._label(self.px, self.preset_title_y, "PRESETS  (P cycles, click jumps)",
                    size=12, bold=True, color=MUTED)
        self.preset_labels = []
        for i, (_, name) in enumerate(PRESETS):
            col, row = divmod(i, 5)
            self.preset_labels.append(self._label(
                self.px + col * 240, self.preset_title_y - 24 - row * 20, name, size=12))
        self.hint = self._label(
            self.px, 26,
            "Up/Dn bar - Left/Right move - Shift x10 - G golden - L lucas - T trace - N numbers - D 21-dot - Space sweep",
            size=11, color=MUTED)
        self.trace_label = self._label(self.px, 48, "", size=12.5, color=HOT)

    def _chip_row(self, y, title, seq):
        self._label(self.px, y, title, size=11.5, bold=True, color=MUTED)
        labels, x = [], self.px + 86
        for v in seq:
            lab = self._label(x, y, str(v), size=11.5, color=MUTED)
            labels.append(lab)
            x += 13 + 8.5 * len(str(v))
        return labels

    # ---- the spiral --------------------------------------------------------

    def _layout_spiral(self):
        w, h = self.width, self.height
        side = min(h - 24, self.px - 36)
        return (self.px - 18) / 2, h / 2, side / 2     # cx, cy, R

    def _rebuild_spiral(self):
        cx, cy, radius = self._layout_spiral()
        seeds, angle = int(self.S["seeds"]), math.radians(self.S["angle"])
        step = int(self.S["step"])
        scale = radius / math.sqrt(max(1, seeds))
        pts = []
        for n in range(seeds):
            r = scale * math.sqrt(n)
            t = n * angle
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
        self.disc.x, self.disc.y, self.disc.radius = cx, cy, radius + 6
        # traced arm: a pool of line segments, managed like the dots
        seg_pts = []
        if step > 0 and seeds > step:
            idx = list(range(step - 1, seeds, step))
            seg_pts = [(pts[idx[i]], pts[idx[i + 1]]) for i in range(len(idx) - 1)]
        while len(self.arm_segs) < len(seg_pts):
            self.arm_segs.append(shapes.Line(0, 0, 0, 0, thickness=2.5,
                                             color=PINK, batch=self.batch))
        for i, seg in enumerate(self.arm_segs):
            if i >= len(seg_pts):
                seg.visible = False
                continue
            (x1, y1), (x2, y2) = seg_pts[i]
            seg.x, seg.y, seg.x2, seg.y2 = x1, y1, x2, y2
            seg.visible = True
        # dots
        while len(self.dots) < seeds:
            self.dots.append(shapes.Circle(0, 0, 3, batch=self.batch))
        for i, dot in enumerate(self.dots):
            if i >= seeds:
                dot.visible = False
                continue
            n = seeds - 1 - i            # draw newest first, like the widget
            x, y = pts[n]
            frac = n / seeds if seeds else 0.0
            on_arm = step > 0 and n >= step - 1 and (n - (step - 1)) % step == 0
            dr = max(1.6, scale * 0.46) * self.S["dot"] * (0.6 + 0.55 * math.sqrt(frac or 0.02))
            dot.x, dot.y = x, y
            dot.radius = dr * 1.25 if on_arm else dr
            dot.color = PINK if on_arm else (int(232 - frac * 60), int(150 - frac * 62),
                                             int(28 + frac * 40))
            dot.visible = True
        # numbers
        show = self.S["nums"] and seeds <= 160
        while len(self.num_labels) < (seeds if show else 0):
            lab = pyglet.text.Label("", font_size=9, anchor_x="center",
                                    anchor_y="center", batch=self.batch)
            lab.bold = True
            self.num_labels.append(lab)
        for i, lab in enumerate(self.num_labels):
            if not show or i >= seeds:
                lab.text = ""
                continue
            x, y = pts[i]
            on_arm = step > 0 and i >= step - 1 and (i - (step - 1)) % step == 0
            lab.x, lab.y = x, y
            lab.text = str(i)
            lab.color = (255, 255, 255, 255) if on_arm else (26, 18, 6, 255)
        self.dirty = False

    # ---- panel refresh -------------------------------------------------------

    def _refresh_panel(self):
        a = self.S["angle"]
        p, q, e = best_frac(a / 360.0)
        self.big.text = f"{a:.6f} deg"
        self.big.color = HOT + (255,) if abs(a - GOLD) < 0.01 else INK + (255,)
        self.frac1.text = (f"= {a / 360:.9f} of a turn - closest fraction {p}/{q} "
                           f"({'rational: spokes' if e < 0.0006 else 'not a simple fraction'})")
        self.frac2.text = (f"{a - GOLD:+.4f} from golden    {a - LUCAS:+.3f} from Lucas    "
                           f"trace step: {self.S['step'] or 'off'}")
        wrapped = textwrap.wrap(diagnose(a), 64)[:5]
        for i, lab in enumerate(self.diag):
            lab.text = wrapped[i] if i < len(wrapped) else ""
        near_fib, near_luc = abs(a - GOLD) < 0.05, abs(a - LUCAS) < 0.05
        for lab, v in zip(self.chips_fib, FIB):
            hot = near_fib and v in (34, 55)
            lab.color = (255, 190, 40, 255) if hot else MUTED + (255,)
            lab.bold = hot
        for lab, v in zip(self.chips_luc, LUC):
            hot = near_luc and v in (29, 47)
            lab.color = (196, 132, 255, 255) if hot else MUTED + (255,)
            lab.bold = hot
        for i, bar in enumerate(self.bars):
            focused = i == self.focus
            bar.rect = (self.px, self.bar_tracks[i].y, 472)
            self.bar_labels[i].text = ("> " if focused else "  ") + bar.name
            self.bar_labels[i].color = HOT + (255,) if focused else MUTED + (255,)
            frac = (bar.get() - bar.vmin) / (bar.vmax - bar.vmin)
            self.bar_fills[i].width = max(4, 472 * min(1.0, max(0.0, frac)))
            self.bar_fills[i].color = HOT if focused else PINK
            self.bar_values[i].text = bar.fmt.format(bar.get())
        for i, (pa, _) in enumerate(PRESETS):
            self.preset_labels[i].color = HOT + (255,) if abs(a - pa) < 0.0005 \
                else MUTED + (255,)
        self.trace_label.text = ("SWEEPING 99.4 <-> 144" if self.sweeping else
                                 f"trace: every {self.S['step']}th seed" if self.S['step']
                                 else "trace: off")

    # ---- events --------------------------------------------------------------

    def _tick(self, dt):
        if self.sweeping:
            a = self.S["angle"]
            if a < 99.4 or a > 144.1:
                a = 99.4
            a += self.sweep_dir * 0.035
            if a >= 144:
                a, self.sweep_dir = 144, -1
            if a <= 99.4:
                a, self.sweep_dir = 99.4, 1
            self.S["angle"] = a
            self.dirty = True
        if self.dirty:
            self._rebuild_spiral()
            self._refresh_panel()

    def on_draw(self):
        self.clear()
        self.batch.draw()
        self.panel_batch.draw()

    def on_key_press(self, symbol, modifiers):
        mult = 10 if modifiers & key.MOD_SHIFT else 1
        if symbol == key.ESCAPE:
            self.close()
        elif symbol == key.UP:
            self.focus = (self.focus - 1) % len(self.bars)
            self.dirty = True
        elif symbol == key.DOWN:
            self.focus = (self.focus + 1) % len(self.bars)
            self.dirty = True
        elif symbol == key.LEFT:
            self._stop_sweep()
            self.bars[self.focus].adjust(-1, mult)
        elif symbol == key.RIGHT:
            self._stop_sweep()
            self.bars[self.focus].adjust(1, mult)
        elif symbol == key.G:
            self._stop_sweep()
            self.S["step"] = 34
            self._set_angle(GOLD)
        elif symbol == key.L:
            self._stop_sweep()
            self.S["step"] = 29
            self._set_angle(LUCAS)
        elif symbol == key.T:
            i = STEPS.index(int(self.S["step"]))
            self._set("step", STEPS[(i + 1) % len(STEPS)])
        elif symbol == key.N:
            self._set("nums", not self.S["nums"])
        elif symbol == key.D:
            self._stop_sweep()
            self.S["seeds"], self.S["nums"], self.S["step"] = 21, True, 13
            self._set_angle(GOLD)
        elif symbol == key.P:
            cur = min(range(len(PRESETS)), key=lambda i: abs(PRESETS[i][0] - self.S["angle"]))
            nxt = PRESETS[(cur + 1) % len(PRESETS)][0] \
                if abs(PRESETS[cur][0] - self.S["angle"]) < 0.001 else PRESETS[cur][0]
            self._stop_sweep()
            self._set_angle(nxt)
        elif symbol == key.SPACE:
            self.sweeping = not self.sweeping

    def on_mouse_press(self, x, y, button, modifiers):
        for i, bar in enumerate(self.bars):
            if bar.rect and bar.rect[0] - 6 <= x <= bar.rect[0] + bar.rect[2] + 6 \
                    and bar.rect[1] - 8 <= y <= bar.rect[1] + 20:
                self.focus = i
                self._stop_sweep()
                bar.set_fraction((x - bar.rect[0]) / bar.rect[2])
                self._dragging = i
                return
        # preset rows
        for i, lab in enumerate(self.preset_labels):
            if lab.x - 4 <= x <= lab.x + 225 and lab.y - 4 <= y <= lab.y + 16:
                self._stop_sweep()
                self._set_angle(PRESETS[i][0])
                return

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        i = getattr(self, "_dragging", None)
        if i is not None and self.bars[i].rect:
            bx, _, bw = self.bars[i].rect
            self.bars[i].set_fraction(min(1.0, max(0.0, (x - bx) / bw)))

    def on_mouse_release(self, x, y, button, modifiers):
        self._dragging = None


if __name__ == "__main__":
    Phyllotaxis()
    pyglet.app.run()
