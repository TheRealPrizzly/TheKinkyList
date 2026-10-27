from dataclasses import dataclass


@dataclass(frozen=True)
class Game:
    slug: str
    number: int
    name: str
    tagline: str
    description: str
    palette: str
    motif: str
    max_picks: int
    # Games 1-3 may optionally re-draw items you've already completed; "Try new things!" never does.
    allows_completed: bool = True
    skips: int = 0


GAMES = {
    game.slug: game
    for game in [
        Game(
            slug="randomize",
            number=1,
            name="Randomize",
            tagline="Let fate decide",
            description="We draw one at random. Feeling brave? Draw one more.",
            palette="rose",
            motif="hearts",
            max_picks=10,
        ),
        Game(
            slug="favorite",
            number=2,
            name="Pick your favorite",
            tagline="Ten temptations, three choices",
            description="Ten options appear. Choose up to three that make your heart race.",
            palette="blush",
            motif="petals",
            max_picks=3,
        ),
        Game(
            slug="search",
            number=3,
            name="Just ask!",
            tagline="You know what you want",
            description="Search the list and pick up to ten things you're craving.",
            palette="plum",
            motif="constellation",
            max_picks=10,
        ),
        Game(
            slug="new",
            number=4,
            name="Try new things!",
            tagline="Somewhere you've never been",
            description="Only things you've never drawn before, from corners you've barely explored. "
            "Accept or skip, with three skips to spend.",
            palette="sunset",
            motif="sparks",
            max_picks=5,
            allows_completed=False,
            skips=3,
        ),
    ]
}

GAME_CHOICES = [(game.slug, game.name) for game in GAMES.values()]
