# Phyllotaxis Calculator

Vogel's model as a desktop app: `r = c*sqrt(n)`, `theta = n * angle`.
The spiral and its controls share one fullscreen window -- no scrolling --
and the bars are keyboard-first.

    Up / Down     choose the bar
    Left / Right  move it (Shift = x10 step)
    G             snap to golden (137.507764...)
    L             snap to Lucas (99.501553...)
    P             cycle presets    T  cycle traced arm
    N             seed numbers     D  21-dot mode
    Space         sweep 99.4 <-> 144
    Esc           quit

Mouse works too: click a bar to choose it, drag to slide, click a preset.

## Run

    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
    ./venv/bin/python phyllotaxis.py

State (angle, seeds, dot size, trace step, numbers) persists to
`state.json` beside the script.
