"""The lists a space keeps, one per kind of game, as shown in the tabs of "Our lists"."""

from dataclasses import dataclass
from typing import Callable

from games.dares import BUILT_IN_DARES
from games.truths import BUILT_IN_TRUTHS
from games.would_you_rather import BUILT_IN_QUESTIONS

from . import starter


@dataclass(frozen=True)
class GameList:
    slug: str
    name: str
    # The page that shows it, as an "items:" URL name.
    url_name: str
    played_with: str
    # What one entry is called, and several.
    one: str
    many: str
    # Each takes a space: how many entries it has, how many of ours it's missing, and emptying it.
    count: Callable
    missing: Callable
    clear: Callable
    # Takes (space, user): adds whatever of ours is missing and returns how many.
    generate: Callable
    # How many entries "Generate a list" has to offer in all.
    ours: int

    def describe(self, count):
        return f"{count} {self.one if count == 1 else self.many}"


def _clear_kinky_list(space):
    # Deleting wishes cascades to their assignments; drop the now-empty game sessions too.
    space.items.all().delete()
    space.categories.all().delete()
    space.game_sessions.all().delete()


def _clear_truth_or_dare(space):
    space.truths.all().delete()
    space.dares.all().delete()


KINKY_LIST = GameList(
    slug="kinky-list",
    name="The Kinky List",
    url_name="list",
    played_with="Kinky List: Randomize, Pick your favorite, Just ask! and Try new things!",
    one="wish",
    many="wishes",
    count=lambda space: space.items.count(),
    missing=lambda space: len(starter.missing_wishes(space)),
    clear=_clear_kinky_list,
    generate=starter.add_starter_list,
    ours=len(starter.STARTER_WISHES),
)

TRUTH_OR_DARE = GameList(
    slug="truth-or-dare",
    name="Truth or Dare",
    url_name="truth_or_dare",
    played_with="Truth or Dare",
    one="truth or dare",
    many="truths and dares",
    count=lambda space: space.truths.count() + space.dares.count(),
    missing=lambda space: sum(len(cards) for cards in starter.missing_truths_and_dares(space)),
    clear=_clear_truth_or_dare,
    generate=starter.add_truth_or_dare_list,
    ours=len(BUILT_IN_TRUTHS) + len(BUILT_IN_DARES),
)

WOULD_YOU_RATHER = GameList(
    slug="would-you-rather",
    name="Would you rather",
    url_name="would_you_rather",
    played_with="Would you rather",
    one="question",
    many="questions",
    count=lambda space: space.questions.count(),
    missing=lambda space: len(starter.missing_questions(space)),
    clear=lambda space: space.questions.all().delete(),
    generate=starter.add_would_you_rather_list,
    ours=len(BUILT_IN_QUESTIONS),
)

LISTS = {game_list.slug: game_list for game_list in (KINKY_LIST, TRUTH_OR_DARE, WOULD_YOU_RATHER)}
