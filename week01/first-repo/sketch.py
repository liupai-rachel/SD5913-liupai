"""
Schotter — after Georg Nees, 1968.

A square grid that falls apart as it descends. The top row is perfectly ordered;
each row after it is rotated and displaced a little more than the one before.
Nees plotted the original on a Zuse Graphomat; you are about to do it in a
language he did not have, on a machine he would have envied.

Run it:

    python sketch.py

It writes sketch.svg next to this file. Open that in a browser (or drag it into
VS Code). Nothing to install — this uses only what ships with Python.

Then change one of the numbers below, run it again, and commit. GitHub will show
you the two images side by side.
"""

import math
import random

# ---------------------------------------------------------------------------
# The knobs. These are yours. Change them, run again, look, commit.
# ---------------------------------------------------------------------------

COLS = 12            # squares across
ROWS = 22            # squares down — the chaos builds over this many rows
SEED = 5913          # any integer. Same seed = same image, every time, forever.
CHAOS = 1.0           # how fast order collapses. 0 = perfect grid. 2 = rubble.
SQUARE = 64          # size of one star, in svg units
MARGIN = 0           # let the stars fill the whole page
STROKE = "#111111"   # line colour
BACKGROUND = "#faf8f4"
STROKE_WIDTH = 1.4

OUTPUT = "sketch.svg"

# ---------------------------------------------------------------------------
# The drawing.
# ---------------------------------------------------------------------------


def star(x, y, size, angle_deg, dx, dy, idx):
    """A 5-point star with a smooth rainbow gradient."""
    cx, cy = x + size / 2, y + size / 2
    outer = size / 2
    inner = outer * 0.45
    points = []
    for i in range(10):
        angle = math.radians(-90 + i * 36)
        radius = outer if i % 2 == 0 else inner
        px = cx + math.cos(angle) * radius
        py = cy + math.sin(angle) * radius
        points.append(f"{px:.2f},{py:.2f}")

    point_string = " ".join(points)
    gradient_id = f"star-gradient-{idx}"

    return (
        f'  <g transform="translate({dx:.2f} {dy:.2f}) '
        f'rotate({angle_deg:.2f} {cx:.2f} {cy:.2f})">\n'
        f'    <defs>\n'
        f'      <linearGradient id="{gradient_id}" x1="0%" y1="0%" '
        f'x2="100%" y2="100%">\n'
        f'        <stop offset="0%" stop-color="#f94144" />\n'
        f'        <stop offset="16%" stop-color="#f3722c" />\n'
        f'        <stop offset="32%" stop-color="#f9c74f" />\n'
        f'        <stop offset="48%" stop-color="#90be6d" />\n'
        f'        <stop offset="64%" stop-color="#00bbf9" />\n'
        f'        <stop offset="80%" stop-color="#577590" />\n'
        f'        <stop offset="100%" stop-color="#9b5de5" />\n'
        f'      </linearGradient>\n'
        f'    </defs>\n'
        f'    <polygon points="{point_string}" fill="url(#{gradient_id})" stroke="{STROKE}" '
        f'stroke-width="{STROKE_WIDTH}" />\n'
        f'  </g>'
    )


def draw():
    rng = random.Random(SEED)
    parts = []

    for row in range(ROWS):
        # Disorder grows with depth. Squaring it keeps the top calm and lets the
        # bottom really come apart — the whole point of the piece.
        damage = CHAOS * (row / ROWS) ** 2

        for col in range(COLS):
            x = MARGIN + col * SQUARE
            y = MARGIN + row * SQUARE
            angle = rng.uniform(-1, 1) * damage * 45
            dx = rng.uniform(-1, 1) * damage * SQUARE * 0.5
            dy = rng.uniform(-1, 1) * damage * SQUARE * 0.5
            parts.append(star(x, y, SQUARE, angle, dx, dy, row * COLS + col))

    width = COLS * SQUARE + MARGIN * 2
    height = ROWS * SQUARE + MARGIN * 2

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}">',
            f'  <rect width="100%" height="100%" fill="{BACKGROUND}" />',
            *parts,
            "</svg>",
        ]
    )


if __name__ == "__main__":
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(draw())
    print(f"wrote {OUTPUT} — {COLS}x{ROWS} squares, seed {SEED}, chaos {CHAOS}")
    print("open it in a browser, then change a number and run me again")
