"""Phyllotaxis Calculator -- a real window, not a web page.

Vogel's model, the way the HTML widget had it, rebuilt as a desktop app
so the spiral and its controls share one screen: no scrolling, and the
picture redraws the same frame the value changes. The bars are keyboard
bars first (that is the point of the exercise):

    Up / Down     choose the bar
    Left / Right  move it (Shift = x10 step) -- key repeat works
    G             snap to golden (137.507764...)
    L             snap to Lucas (99.501553...)
    S             cycle the shapes (Sunflower / Fibonacci / Spiral of
                  Life / Lucas -- the other one / 21-dot hand check)
    P             cycle the presets
    T             cycle the traced arm (off, 13, 18, 21, 29, 34, ...)
    N             toggle seed numbers
    D             21-dot mode (your hand-draw check)
    W             the WHY pages: what the spiral means, life, God, all that
    Space         sweep 99.4 <-> 144 and back
    Esc           quit

The mouse still works: click a bar to choose it, drag to slide it,
click a preset or a shape to jump, click WHY IT MATTERS for the pages.

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
PRESETS = [(90, "90 deg"), (LUCAS, "99.502 Lucas"), (120, "120 deg"),
           (135, "135 deg"), (137.3, "137.3 near"), (GOLD, "137.508 GOLD"),
           (137.92, "137.92 near"), (144, "144 deg"), (180, "180 deg")]

# Whole-picture presets: not just the angle, the whole state a shape wants.
SHAPES = [
    ("Sunflower",            {"angle": GOLD, "seeds": 1000, "dot": 1.1, "step": 34, "nums": False}),
    ("Fibonacci (count it)", {"angle": GOLD, "seeds": 144, "dot": 1.35, "step": 34, "nums": True}),
    ("Spiral of Life",       {"angle": GOLD, "seeds": 300, "dot": 1.3, "step": 0, "nums": False}),
    ("Lucas - the other one", {"angle": LUCAS, "seeds": 400, "dot": 1.0, "step": 29, "nums": False}),
    ("21-dot hand check",    {"angle": GOLD, "seeds": 21, "dot": 1.5, "step": 13, "nums": True}),
]

# The "why" pages (W key, or the WHY cell under the shapes). Written to be
# read on the laptop screen: short lines, no preaching, math kept honest.
INFO_PAGES = [
    ("WHAT YOU ARE LOOKING AT", [
        "Every dot is one seed. The app places seed number n at angle n times "
        "the divergence angle, pushed out from the centre by the square root "
        "of n (Vogel's model). That is the whole machine: one angle, chosen "
        "once, repeated hundreds of times. Everything else -- spirals, spokes, "
        "flowers -- is what that single number does when you let it run.",
        "If the angle is a simple fraction of a turn (90 deg = 1/4, 120 deg = "
        "1/3, 144 deg = 2/5) the seeds stack onto a few straight spokes. Seeds "
        "shade the seeds behind them, wedges of ground go empty, and the head "
        "starves its own children. Try the angle presets: the fractions are "
        "the pretty failures.",
        "If the angle is irrational, no seed ever lands exactly behind an "
        "earlier one, and the eye picks out spiral arms instead. How good the "
        "packing is depends on how irrational the number is -- and one number "
        "is the most irrational of all.",
    ]),
    ("WHY GOLDEN -- AND WHY FIBONACCI SHOWS UP", [
        "Phi (1.6180339887...) is the hardest number to approximate with "
        "fractions; Hurwitz's theorem makes that precise. So the golden angle, "
        "360/phi^2 = 137.507764... degrees, is the angle that stays furthest "
        "from every spoke pattern at every scale. No seed lines up, no gap "
        "repeats, every seed gets its share of light and room. A sunflower "
        "does not solve this equation. Heads that landed near this angle "
        "simply packed more viable seeds, and the angle is what survived.",
        "The Fibonacci numbers were never planted. Stand at any seed: its "
        "nearest neighbours sit a Fibonacci number of steps away along the "
        "spiral, forced by the angle itself. So when you count the arms of a "
        "real sunflower head, clockwise then anticlockwise, you always get "
        "consecutive Fibonacci numbers -- 34 and 55, 55 and 89. Press the "
        "Fibonacci shape and count them here.",
        "About one sunflower in fifty breaks the pattern honestly: same phi, "
        "different starting seeds, and the arm counts come out as Lucas "
        "numbers -- 29 and 47. That is the 'other one' in the shapes menu, "
        "the Lucas sunflower from the spiral notes. Same law, different "
        "family. Pinecones (8/13), pineapples (8/13/21), artichokes and "
        "Romanesco run the same packing wherever growing things compete for "
        "space and light.",
    ]),
    ("LIFE, GOD, AND ONE HONEST NUMBER", [
        "People reach for God at this number for a real reason: a law this "
        "simple should not be this fruitful. One irrational constant, no "
        "blueprint, no foreman -- and out of it falls the most efficient "
        "packing life has found, repeated in seed heads, shells, storms and "
        "spiral galaxies. Traditions call that a signature, sacred geometry, "
        "the fingerprint of a maker who hides in ratios.",
        "The math itself takes no side. It says only this: of all the angles "
        "a growing tip could turn, this is the one that never wastes, never "
        "repeats and never locks into spokes -- growth that stays open at "
        "every step, forever, without ever arriving. Whether you read that as "
        "evolution finding the optimum or as design showing through the "
        "optimum is a stance you bring to the number, not one the number "
        "proves. The spiral notebooks left 'God' as an open gap on purpose. "
        "This screen will not close it. It just shows, live, why the question "
        "keeps attaching itself to 137.507764.",
        "One last thing, because you will feel it when you sweep: near the "
        "golden angle the pattern holds; a third of a degree off, it tears. "
        "The universe's most generous packing is also a knife edge. Spiral "
        "out, keep going.",
    ]),
]

HERE = Path(__file__).resolve().parent
STATE_FILE = HERE / "state.json"

# pyglet's page-key names differ across bindings; take whichever exists.
PAGEDOWN = getattr(key, "PAGEDOWN", getattr(key, "PAGE_DOWN", None))
PAGEUP = getattr(key, "PAGEUP", getattr(key, "PAGE_UP", None))

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
        self.show_info = False
        self.info_page = 0

        self.batch = pyglet.graphics.Batch()
        self.panel_batch = pyglet.graphics.Batch()
        self.disc = shapes.Circle(0, 0, 10, color=DISC, batch=self.batch)
        self.arm_segs = []
        self.dots = []
        self.num_labels = []
        self._build_panel()
        self._build_info()
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

    def _current_shape(self):
        """The SHAPES index the live state matches, or None."""
        for i, (_, st) in enumerate(SHAPES):
            if abs(self.S["angle"] - st["angle"]) < 0.0005 \
                    and int(self.S["seeds"]) == st["seeds"] \
                    and int(self.S["step"]) == st["step"]:
                return i
        return None

    def _apply_shape(self, i):
        self._stop_sweep()
        self.S.update(SHAPES[i][1])
        self.dirty = True
        self._persist()

    # ---- panel ------------------------------------------------------------

    def _label(self, x, y, text, size=13, color=INK, bold=False, anchor_x="left"):
        lab = pyglet.text.Label(text, x=x, y=y, font_size=size,
                                color=color + (255,), anchor_x=anchor_x,
                                anchor_y="baseline", batch=self.panel_batch)
        lab.bold = bold      # pyglet 2.1 wants this as an attribute, not a kwarg
        return lab

    def _build_panel(self):
        # Laid out as a strict vertical budget from the top of the ACTUAL
        # window (the Flex reports 1300x730, not 1366x768 -- measuring off
        # the real height is what keeps the bottom sections from ever
        # landing on top of each other again).
        w, h = self.width, self.height
        self.px = w - 512                       # panel left edge
        shapes.Rectangle(self.px - 16, 0, 512 + 16, h, color=PANEL,
                         batch=self.panel_batch)
        self.big = self._label(self.px, h - 50, "", size=30, bold=True)
        self.frac1 = self._label(self.px, h - 76, "", size=12, color=MUTED)
        self.frac2 = self._label(self.px, h - 94, "", size=12, color=MUTED)
        self.diag = [self._label(self.px, h - 120 - 15 * i, "", size=12.5)
                     for i in range(5)]
        self.chips_fib = self._chip_row(h - 206, "FIBONACCI  ", FIB)
        self.chips_luc = self._chip_row(h - 226, "LUCAS  ", LUC)
        self._label(self.px, h - 248,
                    "r = c*sqrt(n)    theta = n * angle    phi = 1.6180339887...",
                    size=11.5, color=MUTED)
        self._label(self.px, h - 264,
                    "Golden = 360/phi^2    Lucas = 360/(phi+2)", size=11.5, color=MUTED)
        self.bar_labels = []
        self.bar_tracks = []
        self.bar_fills = []
        self.bar_values = []
        for i in range(4):
            y = h - 300 - i * 50
            self.bar_labels.append(self._label(self.px, y, "", size=12, bold=True))
            self.bar_tracks.append(shapes.Rectangle(
                self.px, y - 24, 472, 10, color=TRACK, batch=self.panel_batch))
            self.bar_fills.append(shapes.Rectangle(
                self.px, y - 24, 10, 10, color=PINK, batch=self.panel_batch))
            self.bar_values.append(self._label(self.px + 472, y, "", size=13,
                                               bold=True, anchor_x="right"))
        self._divider(h - 486)
        self.shape_title_y = h - 498
        self._label(self.px, self.shape_title_y, "SHAPES  (S cycles, click applies)",
                    size=12, bold=True, color=MUTED)
        self.shape_labels = []
        for i, (name, _) in enumerate(SHAPES):
            col, row = i % 2, i // 2
            self.shape_labels.append(self._label(
                self.px + col * 248, self.shape_title_y - 22 - row * 20, name, size=12.5))
        # the 6th grid cell (col 1, row 2) is the WHY door, not a shape
        self.why_label = self._label(self.px + 248, self.shape_title_y - 22 - 2 * 20,
                                     "WHY IT MATTERS  (W)", size=12.5, color=HOT)
        self.why_label.bold = True
        self._divider(h - 574)
        self.preset_title_y = h - 586
        self._label(self.px, self.preset_title_y, "ANGLE PRESETS  (P cycles, click jumps)",
                    size=12, bold=True, color=MUTED)
        self.preset_labels = []
        for i, (_, name) in enumerate(PRESETS):
            col, row = i % 3, i // 3
            self.preset_labels.append(self._label(
                self.px + col * 160, self.preset_title_y - 22 - row * 20, name, size=12))
        self._divider(h - 660)
        self.trace_label = self._label(self.px, h - 674, "", size=12.5, color=HOT)
        self.hint = self._label(
            self.px, h - 694,
            "Up/Dn pick bar - Left/Right slide - Shift x10 - G golden - L lucas",
            size=11, color=MUTED)
        self._label(self.px, h - 712,
                    "S shapes - P angles - T trace - N numbers - W why - Space sweep - Esc quit",
                    size=11, color=MUTED)

    def _divider(self, y):
        ln = shapes.Line(self.px, y, self.px + 472, y, thickness=1,
                         color=TRACK, batch=self.panel_batch)
        ln.opacity = 160

    def _build_info(self):
        """The WHY overlay: full-window pages, one pyglet Group per page."""
        w, h = self.width, self.height
        self.info_batch = pyglet.graphics.Batch()
        bg = shapes.Rectangle(0, 0, w, h, color=(16, 10, 14), batch=self.info_batch)
        bg.opacity = 252
        self.info_groups = []
        tx = 70
        wrap_at = max(60, int((w - 2 * tx) / 8.2))
        for pi, (title, paras) in enumerate(INFO_PAGES):
            grp = pyglet.graphics.Group()
            self.info_groups.append(grp)
            lines = []
            for para in paras:
                lines.extend(textwrap.wrap(para, wrap_at))
                lines.append("")
            y = h - 96
            t = pyglet.text.Label(title, x=tx, y=y, font_size=21,
                                  color=HOT + (255,), batch=self.info_batch, group=grp)
            t.bold = True
            y -= 52
            for ln in lines:
                pyglet.text.Label(ln, x=tx, y=y, font_size=14,
                                  color=INK + (255,), batch=self.info_batch, group=grp)
                y -= 23
            pyglet.text.Label(
                f"page {pi + 1} of {len(INFO_PAGES)}   -   PgDn / click = next   -   "
                f"PgUp = back   -   W or Esc = back to the spiral",
                x=tx, y=40, font_size=12, color=MUTED + (255,),
                batch=self.info_batch, group=grp)
        self._show_info_page(0)

    def _show_info_page(self, i):
        self.info_page = max(0, min(len(INFO_PAGES) - 1, i))
        for j, grp in enumerate(self.info_groups):
            grp.visible = j == self.info_page

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
        cur_shape = self._current_shape()
        for i, lab in enumerate(self.shape_labels):
            hot = i == cur_shape
            lab.color = HOT + (255,) if hot else INK + (255,)
            lab.bold = hot
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
        if self.show_info:
            self.info_batch.draw()
            return
        self.batch.draw()
        self.panel_batch.draw()

    def on_key_press(self, symbol, modifiers):
        mult = 10 if modifiers & key.MOD_SHIFT else 1
        if self.show_info:
            if symbol in (key.ESCAPE, key.W):
                self.show_info = False
            elif symbol == PAGEDOWN or symbol in (key.RIGHT, key.SPACE, key.ENTER):
                if self.info_page >= len(INFO_PAGES) - 1:
                    self.show_info = False
                else:
                    self._show_info_page(self.info_page + 1)
            elif symbol == PAGEUP or symbol == key.LEFT:
                self._show_info_page(self.info_page - 1)
            return
        if symbol == key.ESCAPE:
            self.close()
        elif symbol == key.W:
            self.show_info = True
            self._show_info_page(0)
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
        elif symbol == key.S:
            cur = self._current_shape()
            self._apply_shape(0 if cur is None else (cur + 1) % len(SHAPES))
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
        if self.show_info:
            if self.info_page >= len(INFO_PAGES) - 1:
                self.show_info = False
            else:
                self._show_info_page(self.info_page + 1)
            return
        lab = self.why_label
        if lab.x - 4 <= x <= lab.x + 240 and lab.y - 4 <= y <= lab.y + 16:
            self.show_info = True
            self._show_info_page(0)
            return
        for i, bar in enumerate(self.bars):
            if bar.rect and bar.rect[0] - 6 <= x <= bar.rect[0] + bar.rect[2] + 6 \
                    and bar.rect[1] - 8 <= y <= bar.rect[1] + 20:
                self.focus = i
                self._stop_sweep()
                bar.set_fraction((x - bar.rect[0]) / bar.rect[2])
                self._dragging = i
                return
        # shape rows: a click applies the whole bundle
        for i, lab in enumerate(self.shape_labels):
            if lab.x - 4 <= x <= lab.x + 240 and lab.y - 4 <= y <= lab.y + 16:
                self._apply_shape(i)
                return
        # preset rows
        for i, lab in enumerate(self.preset_labels):
            if lab.x - 4 <= x <= lab.x + 152 and lab.y - 4 <= y <= lab.y + 16:
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
