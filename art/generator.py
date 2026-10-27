"""Deterministic abstract SVG art.

The same seed, palette and motif always produce the same picture, so every
game and every item keeps a stable look without storing any image files.
All values written into the SVG are numbers or hex colors from PALETTES,
never user input, so the output is safe to mark as HTML.
"""

import hashlib
import math
import random
from functools import lru_cache

PALETTES = {
    # Game palettes
    "rose": ["#e11d48", "#fb7185", "#ff8a65", "#fda4af"],
    "blush": ["#f9a8d4", "#fdba8c", "#fecdd3", "#f472b6"],
    "plum": ["#7e22ce", "#a855f7", "#c4b5fd", "#db2777"],
    "sunset": ["#db2777", "#f97316", "#f5d7a1", "#facc15"],
    # Extra palettes for items
    "wine": ["#be123c", "#9f1239", "#fb7185", "#fda4af"],
    "lilac": ["#c084fc", "#e9d5ff", "#f0abfc", "#a78bfa"],
    "coral": ["#fb7185", "#fdba74", "#fecaca", "#f43f5e"],
    "champagne": ["#f5d7a1", "#fde68a", "#fbcfe8", "#fca5a5"],
    "orchid": ["#d946ef", "#f0abfc", "#a21caf", "#fb7185"],
    "ember": ["#ea580c", "#e11d48", "#fbbf24", "#fda4af"],
}
ITEM_PALETTES = list(PALETTES)
MOTIFS = ("hearts", "petals", "constellation", "sparks")
BACKGROUND = ("#1c0718", "#2a0f3d")

HEART = "M0 9C-6 4-14-1-10-8C-7-13-1-11 0-6C1-11 7-13 10-8C14-1 6 4 0 9Z"
STAR = "M0-6L1.5-1.5L6 0L1.5 1.5L0 6L-1.5 1.5L-6 0L-1.5-1.5Z"


def _digest(*parts):
    return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()


def _n(value):
    return f"{value:.1f}"


def _hearts(rng, w, h, colors, density):
    shapes = []
    for _ in range(round(rng.randint(5, 9) * density)):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        scale, angle = rng.uniform(0.6, 2.6), rng.uniform(-35, 35)
        fill = rng.choice(["#ffffff", colors[-1], colors[2]])
        shapes.append(
            f'<path d="{HEART}" fill="{fill}" opacity="{rng.uniform(0.18, 0.55):.2f}" '
            f'transform="translate({_n(x)} {_n(y)}) rotate({_n(angle)}) scale({scale:.2f})"/>'
        )
    return shapes


def _petals(rng, w, h, colors, density):
    shapes = []
    for _ in range(rng.randint(1, 2)):
        cx, cy = rng.uniform(0.2, 0.8) * w, rng.uniform(0.25, 0.75) * h
        length = rng.uniform(0.18, 0.32) * min(w, h)
        count = rng.randint(6, 9)
        offset = rng.uniform(0, 360)
        for i in range(count):
            angle = offset + i * 360 / count
            shapes.append(
                f'<ellipse cx="{_n(length / 2)}" cy="0" rx="{_n(length / 2)}" ry="{_n(length / 5)}" '
                f'fill="{colors[i % len(colors)]}" opacity="{rng.uniform(0.25, 0.45):.2f}" '
                f'transform="translate({_n(cx)} {_n(cy)}) rotate({_n(angle)})"/>'
            )
    for _ in range(round(rng.randint(3, 6) * density)):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        size = rng.uniform(6, 16)
        shapes.append(
            f'<ellipse cx="0" cy="0" rx="{_n(size)}" ry="{_n(size / 2.6)}" fill="{rng.choice(colors)}" '
            f'opacity="{rng.uniform(0.3, 0.6):.2f}" transform="translate({_n(x)} {_n(y)}) rotate({_n(rng.uniform(0, 180))})"/>'
        )
    return shapes


def _constellation(rng, w, h, colors, density):
    points = [(rng.uniform(0, w), rng.uniform(0, h)) for _ in range(round(rng.randint(14, 22) * density))]
    shapes = []
    for i, (x, y) in enumerate(points):
        nearest = sorted(
            (math.dist((x, y), other), j) for j, other in enumerate(points) if j != i
        )[: rng.randint(1, 2)]
        for _, j in nearest:
            if j > i:
                ox, oy = points[j]
                shapes.append(
                    f'<line x1="{_n(x)}" y1="{_n(y)}" x2="{_n(ox)}" y2="{_n(oy)}" stroke="#ffffff" '
                    f'stroke-width="0.8" opacity="0.28"/>'
                )
    for x, y in points:
        shapes.append(
            f'<circle cx="{_n(x)}" cy="{_n(y)}" r="{rng.uniform(1, 2.6):.1f}" fill="#ffffff" '
            f'opacity="{rng.uniform(0.5, 0.95):.2f}"/>'
        )
    for x, y in rng.sample(points, min(3, len(points))):
        shapes.append(
            f'<path d="{STAR}" fill="{colors[2]}" opacity="0.9" '
            f'transform="translate({_n(x)} {_n(y)}) scale({rng.uniform(0.8, 1.6):.2f})"/>'
        )
    return shapes


def _sparks(rng, w, h, colors, density):
    shapes = []
    for _ in range(round(rng.randint(3, 6) * density)):
        cx, cy = rng.uniform(0, w), rng.uniform(0, h)
        inner, outer = rng.uniform(4, 10), rng.uniform(16, 38)
        color = rng.choice([colors[2], colors[3], "#ffffff"])
        rays = rng.randint(8, 12)
        for i in range(rays):
            angle = 2 * math.pi * i / rays
            reach = outer * rng.uniform(0.6, 1)
            shapes.append(
                f'<line x1="{_n(cx + inner * math.cos(angle))}" y1="{_n(cy + inner * math.sin(angle))}" '
                f'x2="{_n(cx + reach * math.cos(angle))}" y2="{_n(cy + reach * math.sin(angle))}" '
                f'stroke="{color}" stroke-width="1.6" stroke-linecap="round" opacity="0.7"/>'
            )
    for _ in range(round(rng.randint(5, 9) * density)):
        shapes.append(
            f'<path d="{STAR}" fill="{rng.choice(colors[2:])}" opacity="{rng.uniform(0.5, 0.95):.2f}" '
            f'transform="translate({_n(rng.uniform(0, w))} {_n(rng.uniform(0, h))}) scale({rng.uniform(0.5, 1.4):.2f})"/>'
        )
    return shapes


MOTIF_RENDERERS = {
    "hearts": _hearts,
    "petals": _petals,
    "constellation": _constellation,
    "sparks": _sparks,
}


@lru_cache(maxsize=1024)
def render(seed, palette="rose", motif="hearts", intensity=1.0, density=1.0, width=400, height=300):
    colors = PALETTES.get(palette, PALETTES["rose"])
    digest = _digest(seed, palette, motif, intensity, density)
    rng = random.Random(int(digest[:16], 16))
    uid = "k" + digest[:10]
    w, h = width, height

    blobs = []
    for i in range(3 + round(2 * intensity)):
        blobs.append(
            f'<circle cx="{_n(rng.uniform(-0.1, 1.1) * w)}" cy="{_n(rng.uniform(-0.1, 1.1) * h)}" '
            f'r="{_n(rng.uniform(0.22, 0.5) * min(w, h))}" fill="{colors[i % len(colors)]}" '
            f'opacity="{min(rng.uniform(0.4, 0.7) * intensity, 0.95):.2f}"/>'
        )

    ribbons = []
    for _ in range(rng.randint(2, 3)):
        y0, y1 = rng.uniform(0.1, 0.9) * h, rng.uniform(0.1, 0.9) * h
        c1 = (rng.uniform(0.15, 0.45) * w, rng.uniform(-0.2, 1.2) * h)
        c2 = (rng.uniform(0.55, 0.85) * w, rng.uniform(-0.2, 1.2) * h)
        ribbons.append(
            f'<path d="M-20 {_n(y0)}C{_n(c1[0])} {_n(c1[1])} {_n(c2[0])} {_n(c2[1])} {w + 20} {_n(y1)}" '
            f'fill="none" stroke="{rng.choice(colors)}" stroke-width="{rng.uniform(1.5, 10):.1f}" '
            f'stroke-linecap="round" opacity="{rng.uniform(0.3, 0.55):.2f}"/>'
        )

    motif_shapes = MOTIF_RENDERERS.get(motif, _hearts)(rng, w, h, colors, density)
    blur = _n(min(w, h) * 0.12)

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" '
        f'class="art" aria-hidden="true" focusable="false">'
        f"<defs>"
        f'<linearGradient id="{uid}bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{BACKGROUND[0]}"/><stop offset="1" stop-color="{BACKGROUND[1]}"/>'
        f"</linearGradient>"
        f'<filter id="{uid}blur" x="-50%" y="-50%" width="200%" height="200%">'
        f'<feGaussianBlur stdDeviation="{blur}"/></filter>'
        f"</defs>"
        f'<rect width="{w}" height="{h}" fill="url(#{uid}bg)"/>'
        f'<g filter="url(#{uid}blur)">{"".join(blobs)}</g>'
        f'<g>{"".join(ribbons)}</g>'
        f'<g>{"".join(motif_shapes)}</g>'
        f"</svg>"
    )


SPICE_INTENSITY = {1: 0.85, 2: 1.1, 3: 1.4}


def item_art(item_id, category, spice=1):
    """Art for an item: palette from its category, motif and layout from its id."""
    category_hash = int(_digest("category", (category or "").strip().lower())[:8], 16)
    palette = ITEM_PALETTES[category_hash % len(ITEM_PALETTES)]
    motif = MOTIFS[int(_digest("motif", item_id)[:8], 16) % len(MOTIFS)]
    return render(f"item-{item_id}", palette, motif, SPICE_INTENSITY.get(spice, 1.0), density=0.7)
