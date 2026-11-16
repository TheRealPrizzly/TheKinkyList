from dataclasses import dataclass


@dataclass(frozen=True)
class Game:
    slug: str
    name: str
    tagline: str
    description: str
    palette: str
    motif: str
    max_picks: int
    # Whether the game may optionally re-draw items you've already completed ("Try new things!" never does).
    allows_completed: bool = True
    skips: int = 0
    # Played live on one screen, turn by turn, instead of ending with the assign step.
    live: bool = False
    # The game this is a mode of. Modes are reached through that game rather than the menu.
    mode_of: str = ""
    # A game you play by first choosing one of its modes; it has no play screen of its own.
    has_modes: bool = False


KINKY_LIST_GAME = "kinky-list"


GAMES = {
    game.slug: game
    for game in [
        Game(
            slug=KINKY_LIST_GAME,
            name="Kinky List",
            tagline="Four ways to pick your next wish",
            description="Draw from The Kinky List: let fate decide, pick favorites, ask for exactly what you "
            "want, or explore something brand new. Then choose who each wish is for.",
            palette="rose",
            motif="hearts",
            max_picks=0,
            has_modes=True,
        ),
        Game(
            slug="randomize",
            name="Randomize",
            tagline="Let fate decide",
            description="Set the mood with an intensity or a few categories, then hit Randomize. Feeling brave? Add one more.",
            palette="rose",
            motif="hearts",
            max_picks=8,
            mode_of=KINKY_LIST_GAME,
        ),
        Game(
            slug="favorite",
            name="Pick your favorite",
            tagline="Eight temptations, three choices",
            description="Eight options appear. Choose up to three that make your heart race.",
            palette="blush",
            motif="petals",
            max_picks=3,
            mode_of=KINKY_LIST_GAME,
        ),
        Game(
            slug="search",
            name="Just ask!",
            tagline="You know what you want",
            description="Search the list and pick up to ten things you're craving.",
            palette="plum",
            motif="constellation",
            max_picks=10,
            mode_of=KINKY_LIST_GAME,
        ),
        Game(
            slug="new",
            name="Try new things!",
            tagline="Somewhere you've never been",
            description="Only things you've never drawn before, from corners you've barely explored. "
            "Accept or skip, with three skips to spend.",
            palette="sunset",
            motif="sparks",
            max_picks=5,
            allows_completed=False,
            skips=3,
            mode_of=KINKY_LIST_GAME,
        ),
        Game(
            slug="truth-or-dare",
            name="Truth or Dare",
            tagline="Tell all, or dare it",
            description="Take turns choosing: answer a question honestly, or take on a dare, all from your "
            "Truth or Dare list. Do the dare on the spot, or save it for later.",
            palette="ember",
            motif="sparks",
            max_picks=0,
            live=True,
        ),
        Game(
            slug="would-you-rather",
            name="Would you rather",
            tagline="Choose your temptation",
            description="Two tempting choices, one answer each. Pick an intensity, draw a question, "
            "and find out where your fantasies meet.",
            palette="orchid",
            motif="petals",
            max_picks=0,
            live=True,
        ),
    ]
}

GAME_CHOICES = [(game.slug, game.name) for game in GAMES.values() if not game.has_modes]

# What the Play page offers: every game, with modes tucked inside the game they belong to.
MENU = [game for game in GAMES.values() if not game.mode_of]


def modes_of(game):
    return [mode for mode in GAMES.values() if mode.mode_of == game.slug]
