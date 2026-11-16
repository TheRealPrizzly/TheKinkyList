"""Hand-drawn SVG illustrations, one per game, shown on the game cards.

Unlike generator.py these are fixed pictures, not seeded art: each one shows
what its game is about at a glance (dice for a random draw, a whisper for
"Just ask!"). Everything here is a constant, so the output is safe to mark
as HTML.
"""

from .generator import HEART

STAR = "M0-10C1-3 3-1 10 0C3 1 1 3 0 10C-1 3-3 1-10 0C-3-1-1-3 0-10Z"


def _svg(label, body):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 120" class="illustration" '
        f'role="img" aria-label="{label}" focusable="false">{body}</svg>'
    )


def _star(x, y, scale, fill, opacity=0.9):
    return f'<path d="{STAR}" fill="{fill}" opacity="{opacity}" transform="translate({x} {y}) scale({scale})"/>'


def _die(x, y, angle, size, pips, face, side, pip):
    half = size / 2
    offset = size * 0.28
    dots = "".join(
        f'<circle cx="{dx * offset:.1f}" cy="{dy * offset:.1f}" r="{size * 0.085:.1f}" fill="{pip}"/>' for dx, dy in pips
    )
    return (
        f'<g transform="translate({x} {y}) rotate({angle})">'
        f'<rect x="{-half + 4}" y="{-half + 6}" width="{size}" height="{size}" rx="{size * 0.22:.1f}" fill="{side}"/>'
        f'<rect x="{-half}" y="{-half}" width="{size}" height="{size}" rx="{size * 0.22:.1f}" fill="{face}"/>'
        f"{dots}</g>"
    )


FIVE = [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)]
THREE = [(-1, -1), (0, 0), (1, 1)]

DICE = _svg(
    "Two dice mid-roll",
    '<ellipse cx="104" cy="108" rx="62" ry="6" fill="#16050f" opacity="0.45"/>'
    '<path d="M22 46h22M16 58h26M24 70h16" stroke="#fda4af" stroke-width="3" stroke-linecap="round" opacity="0.7"/>'
    + _die(84, 66, -16, 58, FIVE, "#fff5f7", "#fb7185", "#e11d48")
    + _die(146, 54, 18, 48, THREE, "#fff5f7", "#fb7185", "#e11d48")
    + _star(182, 22, 0.9, "#ffffff")
    + _star(58, 18, 0.6, "#fda4af"),
)


def _heart(x, y, scale, fill="none", stroke="none", angle=0, opacity=1):
    return (
        f'<path d="{HEART}" fill="{fill}" stroke="{stroke}" stroke-width="{1.6 / scale:.2f}" opacity="{opacity}" '
        f'stroke-linejoin="round" transform="translate({x} {y}) rotate({angle}) scale({scale})"/>'
    )


HEARTS = _svg(
    "Three hearts picked out of a row",
    _heart(18, 84, 1.2, stroke="#fecdd3", angle=-16, opacity=0.7)
    + _heart(182, 84, 1.2, stroke="#fecdd3", angle=16, opacity=0.7)
    + _heart(34, 44, 0.9, stroke="#fecdd3", angle=-10, opacity=0.55)
    + _heart(166, 44, 0.9, stroke="#fecdd3", angle=10, opacity=0.55)
    + _heart(56, 86, 2.1, fill="#fdba8c", angle=-14)
    + _heart(144, 86, 2.1, fill="#fdba8c", angle=14)
    + _heart(100, 72, 3.2, fill="#f472b6")
    + '<path d="M86 52c4-6 9-8 14-7" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" opacity="0.8"/>'
    + _star(130, 22, 0.8, "#ffffff")
    + _star(68, 30, 0.5, "#fecdd3"),
)

# A face in profile, looking right, drawn in a 100x100 box. Mouth at about (87, 64).
PROFILE = (
    "M30 100C30 86 22 76 22 56C22 31 39 15 58 15C74 15 84 26 85 40L86 45C88 49 91 52 93 56"
    "C93 58 90 58 87 58C88 60 89 62 87 63C89 65 88 68 86 69C87 74 85 77 79 78C73 79 69 84 68 100Z"
)

WHISPER = _svg(
    "Someone whispering into their partner's ear",
    # The whisperer, leaning in from the left.
    '<g transform="translate(18 4) scale(0.95)">'
    '<path d="M8 118C10 100 22 92 40 92L60 92C74 92 80 100 82 118Z" fill="#7e22ce"/>'
    f'<path d="{PROFILE}" fill="#c4b5fd"/>'
    '<path d="M23 60C17 34 33 9 60 11C76 12 86 22 86 33C74 28 58 30 50 40C44 48 40 58 36 66Z" fill="#a855f7"/>'
    '<path d="M74 41c2 1 5 1 7 0" fill="none" stroke="#3b0764" stroke-width="2" stroke-linecap="round"/>'
    "</g>"
    # The listener, facing us, eyes closed and smiling.
    '<path d="M108 120C110 100 122 92 142 92C162 92 174 100 176 120Z" fill="#db2777"/>'
    '<rect x="134" y="74" width="16" height="22" rx="6" fill="#f0abfc"/>'
    '<ellipse cx="117" cy="56" rx="5" ry="8" fill="#f0abfc"/>'
    '<path d="M118 53c-3 1-3 6 0 7" fill="none" stroke="#a21caf" stroke-width="1.6" stroke-linecap="round"/>'
    '<ellipse cx="142" cy="52" rx="24" ry="29" fill="#f5c2f7"/>'
    '<path d="M118 50C116 28 128 18 142 18C158 18 170 28 167 52C162 38 152 32 142 32C130 32 122 38 118 50Z" fill="#7e22ce"/>'
    '<path d="M130 52c2 3 6 3 8 0M148 52c2 3 6 3 8 0" fill="none" stroke="#3b0764" stroke-width="2" stroke-linecap="round"/>'
    '<path d="M136 66c4 4 9 4 12 0" fill="none" stroke="#3b0764" stroke-width="2" stroke-linecap="round"/>'
    '<circle cx="129" cy="61" r="4" fill="#fb7185" opacity="0.55"/><circle cx="157" cy="61" r="4" fill="#fb7185" opacity="0.55"/>'
    # The whisper itself.
    '<path d="M104 56c2 2 2 6 0 8M108 52c4 4 4 12 0 16" fill="none" stroke="#ffffff" stroke-width="2" '
    'stroke-linecap="round" opacity="0.85"/>'
    + _heart(116, 30, 0.7, fill="#fda4af")
    + _star(186, 20, 0.7, "#ffffff")
    + _star(20, 22, 0.5, "#c4b5fd"),
)

COMPASS = _svg(
    "A compass pointing off the map",
    '<path d="M100 84C126 92 150 86 166 62" fill="none" stroke="#f5d7a1" stroke-width="3" '
    'stroke-linecap="round" stroke-dasharray="1 9" opacity="0.9"/>'
    '<circle cx="74" cy="64" r="44" fill="#2a0f3d" stroke="#f5d7a1" stroke-width="3"/>'
    '<circle cx="74" cy="64" r="36" fill="none" stroke="#f5d7a1" stroke-width="1" opacity="0.5"/>'
    + "".join(
        f'<path d="M74 {y1}V{y2}" stroke="#f5d7a1" stroke-width="2.4" stroke-linecap="round" '
        f'transform="rotate({angle} 74 64)"/>'
        for angle in range(0, 360, 45)
        for y1, y2 in [(22, 28) if angle % 90 == 0 else (24, 27)]
    )
    + '<g transform="rotate(40 74 64)">'
    '<path d="M74 30L82 64H66Z" fill="#facc15"/><path d="M74 98L82 64H66Z" fill="#f97316"/>'
    "</g>"
    '<circle cx="74" cy="64" r="5" fill="#fff7ed"/>'
    + _star(174, 50, 1.5, "#facc15", 1)
    + _star(150, 24, 0.6, "#ffffff")
    + _star(190, 84, 0.5, "#f5d7a1"),
)

def _flame(x, y, scale):
    return (
        f'<g transform="translate({x} {y}) scale({scale})">'
        '<path d="M0-16C7-8 11-3 9 4C7 10 3 13 0 13C-3 13-7 10-9 4C-11-3-5-5-2-10C-1-6 1-5 0-16Z" fill="#f97316"/>'
        '<path d="M0-4C3 0 5 3 4 6C3 9 1 10 0 10C-1 10-3 9-4 6C-5 3-2 1 0-4Z" fill="#fde68a"/>'
        "</g>"
    )


BOTTLE = _svg(
    "A spinning bottle choosing between a question and a flame",
    '<ellipse cx="100" cy="106" rx="60" ry="6" fill="#16050f" opacity="0.45"/>'
    # Motion arcs around the spin.
    '<path d="M48 96A58 24 0 0 0 152 96M52 38A56 22 0 0 1 148 38" fill="none" stroke="#fda4af" '
    'stroke-width="2.4" stroke-linecap="round" stroke-dasharray="2 8" opacity="0.8"/>'
    # The bottle, tipped toward the flame.
    '<g transform="translate(100 68) rotate(-24)">'
    '<rect x="-48" y="-15" width="62" height="30" rx="12" fill="#e11d48"/>'
    '<path d="M10-13C22-13 24-6 32-6H46V6H32C24 6 22 13 10 13Z" fill="#e11d48"/>'
    '<rect x="44" y="-7" width="9" height="14" rx="2.5" fill="#fbbf24"/>'
    '<rect x="-36" y="-10" width="30" height="20" rx="5" fill="#fff5f7"/>'
    + _heart(-21, 1, 0.7, fill="#e11d48")
    + '<path d="M-42-9C-30-12-10-12 6-10" fill="none" stroke="#ffffff" stroke-width="2.4" '
    'stroke-linecap="round" opacity="0.5"/>'
    "</g>"
    # Truth: a speech bubble with a question mark.
    '<path d="M18 18h40a10 10 0 0 1 10 10v14a10 10 0 0 1-10 10H34l-10 9v-9h-6a10 10 0 0 1-10-10V28'
    'a10 10 0 0 1 10-10Z" fill="#fff5f7"/>'
    '<path d="M31 30c0-5 3-7 7-7s7 2.5 7 6.5c0 4.5-6 5-6 9.5" fill="none" stroke="#e11d48" stroke-width="3.6" '
    'stroke-linecap="round"/>'
    '<circle cx="39" cy="45" r="2.3" fill="#e11d48"/>'
    # Dare: a flame.
    + _flame(172, 40, 1.5)
    + _star(150, 14, 0.6, "#ffffff")
    + _star(188, 84, 0.5, "#fda4af"),
)

GAME_ILLUSTRATIONS = {
    "randomize": DICE,
    "favorite": HEARTS,
    "search": WHISPER,
    "new": COMPASS,
    "truth-or-dare": BOTTLE,
}
