"""Hand-drawn SVG illustrations, one per game, shown on the game cards.

Unlike generator.py these are fixed pictures, not seeded art: each one shows
what its game is about at a glance (dice for a random draw, a whisper for
"Just ask!", a delighted gasp for "Try new things!"). Everything here is a constant, so the output is safe to mark
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

SKIN = "#f8d3b0"
SKIN_SHADE = "#e6a982"
HAIR = "#9d174d"


def _hand(x, y, angle):
    """A hand held upright, fingertips at the top, its palm centered on (x, y)."""
    return (
        f'<g transform="translate({x} {y}) rotate({angle})">'
        f'<rect x="-9" y="-14" width="18" height="28" rx="9" fill="{SKIN}" stroke="{SKIN_SHADE}" stroke-width="1.2"/>'
        f'<path d="M-4.5-13V-3M0-14V-3M4.5-13V-3" stroke="{SKIN_SHADE}" stroke-width="1.2" stroke-linecap="round"/>'
        "</g>"
    )


SURPRISED = _svg(
    "A woman with her hands over her mouth, wide-eyed with surprise",
    # Long hair falling behind her shoulders.
    f'<path d="M100 8C74 8 64 28 64 52C64 76 60 94 54 120H146C140 94 136 76 136 52C136 28 126 8 100 8Z" fill="{HAIR}"/>'
    # Neck, then the sweater over it.
    f'<rect x="92" y="72" width="16" height="26" rx="7" fill="{SKIN_SHADE}"/>'
    '<path d="M58 120C60 101 76 93 92 93C94 98 106 98 108 93C124 93 140 101 142 120Z" fill="#f97316"/>'
    # Ears and face.
    f'<ellipse cx="77" cy="54" rx="4" ry="6" fill="{SKIN_SHADE}"/><ellipse cx="123" cy="54" rx="4" ry="6" fill="{SKIN_SHADE}"/>'
    f'<ellipse cx="100" cy="52" rx="23" ry="27" fill="{SKIN}"/>'
    # Wide eyes, raised brows, blushing cheeks.
    '<circle cx="91" cy="49" r="5.5" fill="#ffffff"/><circle cx="109" cy="49" r="5.5" fill="#ffffff"/>'
    '<circle cx="91" cy="49.5" r="2.8" fill="#3b0764"/><circle cx="109" cy="49.5" r="2.8" fill="#3b0764"/>'
    '<circle cx="92.2" cy="48.3" r="1" fill="#ffffff"/><circle cx="110.2" cy="48.3" r="1" fill="#ffffff"/>'
    f'<path d="M84 42C87 38.5 92 38 96 39.5M104 39.5C108 38 113 38.5 116 42" fill="none" stroke="{HAIR}" stroke-width="2.4" '
    'stroke-linecap="round"/>'
    '<circle cx="84" cy="61" r="4.5" fill="#fb7185" opacity="0.5"/><circle cx="116" cy="61" r="4.5" fill="#fb7185" opacity="0.5"/>'
    # The top of her hair, with a side-swept fringe.
    f'<path d="M77 54C76 42 83 35 92 34C100 33 105 35 110 31C116 33 122 41 123 54C128 30 117 13 100 13'
    f'C83 13 72 30 77 54Z" fill="{HAIR}"/>'
    # Forearms rising from the sweater, hands over her mouth.
    '<path d="M76 118L91 84M124 118L109 84" stroke="#ea580c" stroke-width="12" stroke-linecap="round"/>'
    + _hand(94, 72, -14)
    + _hand(106, 72, 14)
    # Surprise lines and sparkles.
    + '<path d="M62 20L55 13M57 34H48M138 20L145 13M143 34H152" stroke="#facc15" stroke-width="2.6" '
    'stroke-linecap="round"/>'
    + _star(36, 64, 0.8, "#facc15", 1)
    + _star(166, 60, 0.9, "#f5d7a1")
    + _star(156, 96, 0.5, "#facc15"),
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

def _ice_cube(x, y, size):
    """An ice cube seen from above a corner, its top corner at (x, y)."""
    h = size / 2
    return (
        f'<g stroke-linejoin="round" stroke-width="1.5">'
        f'<path d="M{x} {y}L{x + size} {y + h}L{x} {y + size}L{x - size} {y + h}Z" fill="#e0f2fe" stroke="#e0f2fe"/>'
        f'<path d="M{x - size} {y + h}L{x} {y + size}V{y + size * 1.8}L{x - size} {y + size * 1.3}Z" '
        'fill="#7dd3fc" stroke="#7dd3fc"/>'
        f'<path d="M{x} {y + size}L{x + size} {y + h}V{y + size * 1.3}L{x} {y + size * 1.8}Z" '
        'fill="#38bdf8" stroke="#38bdf8"/>'
        f'<path d="M{x - size * 0.45} {y + h}L{x} {y + size * 0.28}" stroke="#ffffff" stroke-width="2.4" '
        'stroke-linecap="round" opacity="0.9"/>'
        "</g>"
    )


def _snowflake(x, y, r):
    arms = "".join(
        f'<path d="M0 {-r}V{r}M-{r * 0.3:.1f} {-r * 0.7:.1f}L0 {-r * 0.45:.1f}L{r * 0.3:.1f} {-r * 0.7:.1f}'
        f'M-{r * 0.3:.1f} {r * 0.7:.1f}L0 {r * 0.45:.1f}L{r * 0.3:.1f} {r * 0.7:.1f}" transform="rotate({angle})"/>'
        for angle in (0, 60, 120)
    )
    return (
        f'<g transform="translate({x} {y})" stroke="#e0f2fe" stroke-width="1.6" stroke-linecap="round" '
        f'fill="none">{arms}</g>'
    )


ROSE = (
    '<path d="M70 104C68 92 72 82 70 66" fill="none" stroke="#86efac" stroke-width="2.6" stroke-linecap="round"/>'
    '<path d="M70 88C76 82 83 83 87 88C81 93 75 92 70 88Z" fill="#86efac"/>'
    '<path d="M70 96C65 91 58 92 55 96C60 100 66 99 70 96Z" fill="#4ade80"/>'
    '<path d="M57 52C58 62 63 67 70 67C77 67 82 62 83 52C78 56 74 56 70 53C66 56 62 56 57 52Z" fill="#e11d48"/>'
    '<circle cx="70" cy="50" r="11" fill="#fb7185"/>'
    '<path d="M64 51C63 45 68 42 72 43C76 45 76 50 73 52C70 54 67 51 69 49" fill="none" stroke="#be123c" '
    'stroke-width="1.8" stroke-linecap="round"/>'
)

# Two cuffs joined by a short chain, drawn in steel.
HANDCUFFS = (
    '<g fill="none" stroke-linecap="round">'
    '<circle cx="150" cy="84" r="12" stroke="#e5e7eb" stroke-width="4.5"/>'
    '<circle cx="178" cy="62" r="12" stroke="#e5e7eb" stroke-width="4.5"/>'
    '<path d="M141 77C145 74 150 74 154 76M169 55C173 52 178 52 182 54" stroke="#ffffff" stroke-width="1.6" '
    'opacity="0.8"/>'
    '<rect x="157" y="69" width="5" height="9" rx="2.5" stroke="#cbd5e1" stroke-width="2.2" '
    'transform="rotate(-38 159.5 73.5)"/>'
    '<rect x="164" y="64" width="5" height="9" rx="2.5" stroke="#cbd5e1" stroke-width="2.2" '
    'transform="rotate(-38 166.5 68.5)"/>'
    "</g>"
)

CONTRASTS = _svg(
    "Cold and romantic on one side, hot and kinky on the other: an ice cube and a rose, or a flame and handcuffs",
    # Two panels split on a slant: cool on the left, warm on the right.
    '<path d="M16 6H106L90 114H16A10 10 0 0 1 6 104V16A10 10 0 0 1 16 6Z" fill="#38bdf8" fill-opacity="0.16" '
    'stroke="#bae6fd" stroke-opacity="0.35" stroke-width="1.5"/>'
    '<path d="M110 6H184A10 10 0 0 1 194 16V104A10 10 0 0 1 184 114H94Z" fill="#f43f5e" fill-opacity="0.2" '
    'stroke="#fda4af" stroke-opacity="0.4" stroke-width="1.5"/>'
    # Cold and romantic.
    + _ice_cube(30, 46, 19)
    + _snowflake(24, 22, 8)
    + _snowflake(40, 102, 5)
    + f'<g transform="translate(-6 0)">{ROSE}</g>'
    + _heart(80, 24, 0.75, stroke="#fecdd3", opacity=0.9)
    # Hot and kinky.
    + _flame(136, 44, 1.6)
    + f'<g transform="translate(2 10)">{HANDCUFFS}</g>'
    + _star(182, 24, 0.7, "#fbbf24", 1)
    + _star(122, 96, 0.45, "#fde68a")
    # The choice.
    + '<circle cx="98" cy="60" r="15" fill="#2a0f3d" stroke="#f0abfc" stroke-width="2"/>'
    '<text x="98" y="65" text-anchor="middle" font-family="Georgia, serif" font-style="italic" font-size="15" '
    'fill="#fdba8c">or</text>',
)

GAME_ILLUSTRATIONS = {
    "randomize": DICE,
    "favorite": HEARTS,
    "search": WHISPER,
    "new": SURPRISED,
    "truth-or-dare": BOTTLE,
    "would-you-rather": CONTRASTS,
}
