"""Hand-drawn SVG illustrations, one per game, shown on the game cards.

Unlike generator.py these are fixed pictures, not seeded art: each one shows
what its game is about at a glance (dice for a random draw, a whisper for
"Just ask!", a secret in the ear for "Try new things!"). Everything here is a constant, so the output is safe to mark
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
    "A man with a beard and a man bun whispering into a woman's ear",
    # The whisperer, leaning in from the left: the same guy as on "Try new things!", in profile.
    '<g transform="translate(18 4) scale(0.95)">'
    '<path d="M8 118C10 100 22 92 40 92L60 92C74 92 80 100 82 118Z" fill="#f97316"/>'
    f'<path d="{PROFILE}" fill="#f8d3b0"/>'
    # Hair slicked back into a bun, with a hair tie.
    '<circle cx="30" cy="16" r="10" fill="#5b2c14"/>'
    '<path d="M22 62C16 36 30 12 56 12C70 12 80 18 84 28C72 24 60 26 52 32C44 38 40 48 36 64Z" fill="#5b2c14"/>'
    '<rect x="30" y="20" width="12" height="4.2" rx="2.1" fill="#f5d7a1" transform="rotate(38 36 22)"/>'
    '<ellipse cx="44" cy="54" rx="5" ry="7" fill="#e6a982"/>'
    '<path d="M43 50c3 1 3 6 0 8" fill="none" stroke="#c97f58" stroke-width="1.6" stroke-linecap="round"/>'
    # Brow and an eye on her ear.
    '<path d="M70 35C73 33 77 33 80 34.5" fill="none" stroke="#5b2c14" stroke-width="2.6" stroke-linecap="round"/>'
    '<ellipse cx="76" cy="41.5" rx="3.2" ry="2.5" fill="#ffffff"/><circle cx="77.6" cy="41.6" r="1.7" fill="#3b0764"/>'
    # Full beard along the jaw and chin, and a moustache over his lips.
    '<path d="M48 46C47 60 50 72 57 80C63 86 72 89 80 87C86 85 89 80 88 72C86 70 84 69.5 82 70C79 67 75 66 71 66'
    'C64 65 58 60 55 54C53 50 51 47 48 46Z" fill="#5b2c14"/>'
    '<path d="M72 61.5C77 58 84 57.5 88.5 59.5C87 62.5 81 63.6 72 63Z" fill="#5b2c14"/>'
    "</g>"
    # The listener, facing us, eyes closed and smiling.
    '<path d="M108 120C110 100 122 92 142 92C162 92 174 100 176 120Z" fill="#db2777"/>'
    '<rect x="134" y="74" width="16" height="22" rx="6" fill="#f0abfc"/>'
    '<ellipse cx="117" cy="56" rx="5" ry="8" fill="#f0abfc"/>'
    '<path d="M118 53c-3 1-3 6 0 7" fill="none" stroke="#a21caf" stroke-width="1.6" stroke-linecap="round"/>'
    '<ellipse cx="167" cy="56" rx="5" ry="8" fill="#f0abfc"/>'
    '<path d="M166 53c3 1 3 6 0 7" fill="none" stroke="#a21caf" stroke-width="1.6" stroke-linecap="round"/>'
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
HIS_HAIR = "#5b2c14"
# She faces left in profile, lips at his ear, smiling as she talks. Same look as the listener on "Just ask!".
HER = (
    '<path d="M170 122C170 104 160 94 146 90C138 88 126 88 118 92C110 96 106 104 106 122Z" fill="#db2777"/>'
    '<rect x="122" y="66" width="15" height="26" rx="6" fill="#f0abfc"/>'
    '<path d="M136 28C122 27 113 33 111.5 41C110.5 45 106 49 104.2 52.2C103.6 53.6 105 55 107.6 55.4'
    'C106.4 56.8 106 58.4 106.4 60L106.6 64.4C106.2 66.6 106.8 69.6 109.6 71.6C113 75 121 77 127 74.5'
    'C134 72 142 66 146 56C149 46 146 30 136 28Z" fill="#f5c2f7"/>'
    # Purple hair pulled back into a ponytail, with a hair tie.
    '<path d="M152 30C167 27 177 38 175 55C173 70 167 81 159 89C162 76 162 63 156 52C154 46 152 40 152 30Z" '
    'fill="#7e22ce"/>'
    '<path d="M163 38C168 46 168 60 164 72" fill="none" stroke="#a855f7" stroke-width="1.8" stroke-linecap="round"/>'
    '<path d="M110 42C108 26 122 16 138 17C154 18 162 32 158 52C156 60 152 64 148 66C147 56 142 48 134 44'
    'C126 38 118 38 110 42Z" fill="#7e22ce"/>'
    '<ellipse cx="158.5" cy="35" rx="2.8" ry="4.6" fill="#facc15" transform="rotate(-25 158.5 35)"/>'
    '<ellipse cx="136" cy="54" rx="4.5" ry="7" fill="#f0abfc"/>'
    '<path d="M135 51c2.6 1 2.6 5.4 0 6.4" fill="none" stroke="#a21caf" stroke-width="1.5" stroke-linecap="round"/>'
    # Closed, happy eye; rosy cheek; a smile, open mid-sentence.
    '<path d="M113.5 46.5c2 2.8 6 2.8 8 0" fill="none" stroke="#3b0764" stroke-width="2" stroke-linecap="round"/>'
    '<circle cx="121" cy="58" r="4.5" fill="#fb7185" opacity="0.55"/>'
    '<path d="M106.4 60L112.4 60.8C111.6 63.6 109 65.2 106.6 64.4Z" fill="#3b0764"/>'
    '<path d="M107.6 63.2C108.8 62.4 110.4 62.6 111 63.4C109.8 64.4 108.4 64.4 107.6 63.2Z" fill="#fb7185"/>'
    '<path d="M112.6 58.6C114.6 59.6 115.2 61.8 114.2 63.6" fill="none" stroke="#e879f9" stroke-width="1.4" '
    'stroke-linecap="round"/>'
)

HIM = (
    f'<rect x="70" y="78" width="16" height="22" rx="7" fill="{SKIN_SHADE}"/>'
    '<path d="M30 122C32 104 50 95 70 95C72 100 84 100 86 95C106 95 122 104 124 122Z" fill="#f97316"/>'
    f'<ellipse cx="56" cy="60" rx="4" ry="6" fill="{SKIN_SHADE}"/><ellipse cx="100" cy="60" rx="4" ry="6" fill="{SKIN_SHADE}"/>'
    f'<ellipse cx="78" cy="58" rx="22" ry="26" fill="{SKIN}"/>'
    # Hair pulled back into a bun, with a hair tie.
    f'<circle cx="78" cy="22" r="9" fill="{HIS_HAIR}"/>'
    '<rect x="72" y="28.5" width="12" height="3.5" rx="1.75" fill="#f5d7a1"/>'
    f'<path d="M56 56C54 40 64 32 78 32C92 32 102 40 100 56C97 46 90 41 78 41C66 41 59 46 56 56Z" fill="{HIS_HAIR}"/>'
    # Raised brows, wide eyes glancing her way.
    f'<path d="M63 43C66 39 71 39 75 41M81 41C85 39 90 39 93 43" fill="none" stroke="{HIS_HAIR}" stroke-width="3" '
    'stroke-linecap="round"/>'
    '<circle cx="70" cy="53" r="5.5" fill="#ffffff"/><circle cx="86" cy="53" r="5.5" fill="#ffffff"/>'
    '<circle cx="71.6" cy="53.5" r="2.8" fill="#3b0764"/><circle cx="87.6" cy="53.5" r="2.8" fill="#3b0764"/>'
    '<circle cx="72.6" cy="52.4" r="1" fill="#ffffff"/><circle cx="88.6" cy="52.4" r="1" fill="#ffffff"/>'
    '<circle cx="63" cy="62" r="3.5" fill="#fb7185" opacity="0.45"/><circle cx="93" cy="62" r="3.5" fill="#fb7185" opacity="0.45"/>'
    '<path d="M78 56C76.5 60 74.5 63 75.5 65C76.5 67 80 67 81 65.5" fill="none" stroke="#c97f58" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    # Full beard and moustache around a delighted open smile.
    f'<path d="M57 54C56 75 64 93 78 94C92 93 100 75 99 54C96 64 92 70 86 72C82 69 74 69 70 72C64 70 60 64 57 54Z" '
    f'fill="{HIS_HAIR}"/>'
    '<path d="M69 74C69 84 87 84 87 74Z" fill="#3b0764"/>'
    '<path d="M73 80C75 77 81 77 83 80C80 82 76 82 73 80Z" fill="#fb7185"/>'
    f'<path d="M67 72C71 67 76 68 78 70C80 68 85 67 89 72C85 73 81 73 78 71.5C75 73 71 73 67 72Z" fill="{HIS_HAIR}"/>'
)

WHISPERED = _svg(
    "A smiling woman talking into the ear of a pleasantly surprised man with a beard and a man bun",
    HIM
    + HER
    # His surprise, and the hearts her secret sets loose.
    + '<path d="M44 30L37 23M40 44H31" stroke="#facc15" stroke-width="2.6" stroke-linecap="round"/>'
    + _heart(103, 30, 0.5, fill="#fda4af")
    + _heart(113, 14, 0.38, fill="#fb7185")
    + _star(186, 92, 0.6, "#facc15", 1)
    + _star(20, 84, 0.55, "#f5d7a1")
    + _star(150, 8, 0.45, "#ffffff"),
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
    "new": WHISPERED,
    "truth-or-dare": BOTTLE,
    "would-you-rather": CONTRASTS,
}
